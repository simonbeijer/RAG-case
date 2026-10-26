import time
import uuid

from app.agent import load_agent
from app.config import load_config
from app.log import log_messages
from langgraph.graph.state import CompiledStateGraph

def ask_question(agent: CompiledStateGraph, config: dict, question: str, thread_id: str)-> str:
    """ Run agent with question in thread, log hits and usage. Return answer"""
    start = time.perf_counter()
    # LangGraph's config, not the app's config
    result = agent.invoke(
        {"messages": [("human", question)]},
        config={"configurable": {"thread_id": thread_id}},
    )
    seconds = time.perf_counter() - start

    log_messages(result["messages"], seconds, config)
    return result["messages"][-1].content


def main() -> None:
    """ Get config, index and models. Start loop for questions """
    config = load_config()
    agent = load_agent(config)
    # One terminal chat is one session
    thread_id = str(uuid.uuid4())
    while True:
        question = input("Fråga: ")
        if question == "exit":
            break
        print(ask_question(agent, config, question, thread_id))
    
if __name__ == "__main__":
    
    main()