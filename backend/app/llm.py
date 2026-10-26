import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def get_chat_model(config: dict) -> ChatOpenAI:
    """ Get chat model for config """
    return ChatOpenAI(
        model=config["chat_model"],
        base_url=config["base_url"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        api_key=os.environ["OPENROUTER_API_KEY"],
    )

def get_embedding_model(config: dict) -> OpenAIEmbeddings:
    """Get embedding model from config"""
    return OpenAIEmbeddings(
        model=config["embedding_model"],
        base_url=config["base_url"],
        api_key=os.environ["OPENROUTER_API_KEY"],
        check_embedding_ctx_length=False,
    )