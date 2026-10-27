import json
import time
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, ToolMessage
from pydantic import BaseModel
from rich.console import Console

from app.agent import load_agent
from app.config import load_config
from app.log import log_messages

config = load_config()
agent = load_agent(config)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config["frontend_url"]],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class ChatQuestion(BaseModel):
    """Question and thread id from frontend"""
    question: str
    thread_id: str
    
async def stream_answer(question: str, thread_id: str) -> AsyncIterator[str]:
    """Streams answer as SSE events: token, source, error. Log after answer"""
    # LangGraph's config, not the app's config
    graph_config = {"configurable": {"thread_id": thread_id}}
    start = time.perf_counter()
    try:
        async for chunk, metadata in agent.astream(
            {"messages": [("human", question)]},
            config=graph_config,
            stream_mode="messages",
        ):
            # Only answer text from the agent node, not tool calls or tool output
            if metadata["langgraph_node"] == "agent" and chunk.content:
                yield f"event: token\ndata: {json.dumps({'text': chunk.content})}\n\n"
        seconds = time.perf_counter() - start

        state = await agent.aget_state(graph_config)
        messages = state.values["messages"]
        last_human = max(i for i, m in enumerate(messages) if isinstance(m, HumanMessage))
        sent_urls = set()
        for message in messages[last_human + 1:]:
            if isinstance(message, ToolMessage):
                for hit in message.artifact:
                    if hit["url"] not in sent_urls:
                        sent_urls.add(hit["url"])
                        source = {"url": hit["url"], "title": hit["title"]}
                        yield f"event: source\ndata: {json.dumps(source)}\n\n"

        log_messages(messages, seconds, config)
    except Exception as error:
        Console().print(f"[red]Fel: {error}[/red]")
        yield f"event: error\ndata: {json.dumps({'message': 'Något gick fel. Försök igen.'})}\n\n"


@app.post("/chat")
async def chat(request: ChatQuestion) -> StreamingResponse:
    """Stop empty question. Return streamed answer"""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Frågan är tom.")
    return StreamingResponse(stream_answer(question, request.thread_id), media_type="text/event-stream")