import os

from langchain_openai import ChatOpenAI


def get_chat_model(config: dict) -> ChatOpenAI:
    """ Get chat model for config """
    return ChatOpenAI(
        model=config["chat_model"],
        base_url=config["base_url"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
