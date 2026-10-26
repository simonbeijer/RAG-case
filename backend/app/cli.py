import time

from app.agent import build_agent, make_search_tool
from app.config import BACKEND_DIR, load_config
from app.index import load_index
from app.llm import get_chat_model, get_embedding_model
from app.log import log_messages
from langgraph.graph.state import CompiledStateGraph

def ask_question(agent: CompiledStateGraph, config: dict, question: str)-> str:
    """ Run agent with question, log hits and usage. Return answer """
    start = time.perf_counter()
    result = agent.invoke({"messages": [("human", question)]})
    seconds = time.perf_counter() - start

    log_messages(result["messages"], seconds, config)
    return result["messages"][-1].content


def main() -> None:
    """ Get config, index and models. Start loop for questions """
    config = load_config()
    model = get_chat_model(config)
    embed_model = get_embedding_model(config)
    chunks, matrix = load_index(BACKEND_DIR / "data")
    search_tool = make_search_tool(embed_model, chunks, matrix, config)
    agent = build_agent(model, search_tool, config)
    while True:
        question = input("Fråga: ")
        if question == "exit":
            break
        print(ask_question(agent, config, question))
    
if __name__ == "__main__":
    
    main()