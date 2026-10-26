import time

from app.config import BACKEND_DIR, load_config
from app.index import load_index, search
from app.llm import get_chat_model, get_embedding_model
from app.log import log_hits, log_usage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import numpy as np

def ask_question(model: ChatOpenAI, embed_model: OpenAIEmbeddings,chunks: list[dict], matrix: np.ndarray, config: dict, question: str)-> str:
    """ Search chunks, add hit to prompts, ask model, log hits and usage. and return answer """
    hits = search(question, embed_model, chunks, matrix, config)
    log_hits(hits)
    # Empty list joins to "", then "or" picks the fallback
    sources = "\n\n".join(f"Källa: {hit['url']}\n{hit['text']}" for hit in hits) or config["no_source"]
    messages = [
        ("system", config["system_prompt"]),
        ("human", f"{sources}\n\nFråga: {question}"),
    ]
    start = time.perf_counter()
    response = model.invoke(messages)
    seconds = time.perf_counter() - start

    usage = response.usage_metadata
    log_usage(usage["input_tokens"], usage["output_tokens"], seconds, config)
    return response.content


def main() -> None:
    """ Get config, index and models. Start loop for questions """
    config = load_config()
    model = get_chat_model(config)
    embed_model = get_embedding_model(config)
    chunks, matrix = load_index(BACKEND_DIR / "data")
    while True:
        question = input("Fråga: ")
        if question == "exit":
            break
        print(ask_question(model, embed_model, chunks, matrix, config, question))
    
if __name__ == "__main__":
    
    main()