from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pathlib import Path
import numpy as np

from app.config import BACKEND_DIR, load_config
from app.index import load_index, search
from app.llm import get_chat_model, get_embedding_model

def make_search_tool(embed_model: OpenAIEmbeddings, chunks: list[dict], matrix: np.ndarray, config:dict) -> BaseTool:
    """Return search_tool, text to model and hits as artifact"""

    @tool(response_format="content_and_artifact")
    def search_knowledge_base(query: str) -> tuple[str, list[dict]]:
        """Search knowledge base built from compileit.com"""
        hits = search(query, embed_model, chunks, matrix, config)
        # Empty list joins to "", then "or" picks the fallback
        content = "\n\n".join(f"Källa: {hit['url']}\n{hit['text']}" for hit in hits) or config["no_source"]
        return content, hits

    return search_knowledge_base


def build_agent(model: ChatOpenAI, search_tool:BaseTool, config: dict) -> CompiledStateGraph:
    """Graph with agents and tool nodes. First call always search"""

    def agent(state: MessagesState) -> dict:
        has_searched = any(isinstance(m, ToolMessage) for m in state["messages"])
        if has_searched:
            bound = model.bind_tools([search_tool])
        else:
            bound = model.bind_tools([search_tool], tool_choice="required")
        messages = [SystemMessage(config["system_prompt"])] + state["messages"]
        return {"messages": [bound.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode([search_tool]))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile()


def save_graph(agent: CompiledStateGraph, path: Path) -> None:
    """Write Mermaid graph from agent"""
    mermaid = agent.get_graph().draw_mermaid()
    path.write_text(f"```mermaid\n{mermaid}\n```\n", encoding="utf-8")


if __name__ == "__main__":
    config = load_config()
    model = get_chat_model(config)
    embed_model = get_embedding_model(config)
    chunks, matrix = load_index(BACKEND_DIR / "data")
    search_tool = make_search_tool(embed_model, chunks, matrix, config)
    agent = build_agent(model, search_tool, config)
    save_graph(agent, BACKEND_DIR.parent / "docs" / "agent-graph.md")