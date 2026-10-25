import time

from app.config import load_config
from app.llm import get_chat_model
from app.log import log_usage
from langchain_openai import ChatOpenAI

def ask_question(model: ChatOpenAI, config: dict, question: str)-> str:
    """ Ask question with systemprompt, measure time, log and return answer """
    messages = [
        ("system", config["system_prompt"]),
        ("human", question),
    ]
    start = time.perf_counter()
    response = model.invoke(messages)
    seconds = time.perf_counter() - start

    usage = response.usage_metadata
    log_usage(usage["input_tokens"], usage["output_tokens"], seconds, config)
    return response.content


def main() -> None:
    """ Get config, create model and start loop for questions """
    config = load_config()
    model = get_chat_model(config)
    while True:
        question = input("Fråga: ")
        if question == "exit":
            break
        print(ask_question(model, config, question))
    
if __name__ == "__main__":
    
    main()