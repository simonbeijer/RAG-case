import json
from pathlib import Path

import numpy as np
from langchain_openai import OpenAIEmbeddings

def embed_chunks(chunks: list[dict], model: OpenAIEmbeddings) -> np.ndarray:
    """Embed the text in every chunk. Row index to chunk index"""
    vectors = model.embed_documents([chunk["text"] for chunk in chunks])
    return np.array(vectors)


def save_embeddings(matrix: np.ndarray, path: Path) -> None:
    """Save matrix to embeddings.npy"""
    np.save(path, matrix)

def load_index(data_dir: Path) -> tuple[list[dict], np.ndarray]:
    """Load chunks.json and embeddings.npy"""
    chunks = json.loads((data_dir / "chunks.json").read_text(encoding="utf-8"))
    matrix = np.load(data_dir / "embeddings.npy")
    return chunks, matrix


def search(query: str, model: OpenAIEmbeddings, chunks: list[dict], matrix: np.ndarray, config: dict) -> list[dict]:
    """Return top k-NN with score above score_threshold. Hit got url, title, text and score"""
    query_vec = np.array(model.embed_query(query))
    # Vectors have length 1, so dot product is cosine similarity
    scores = matrix @ query_vec
    top = np.argsort(scores)[::-1][: config["k"]]
    return [
        {
            "url": chunks[i]["url"],
            "title": chunks[i]["title"],
            "text": chunks[i]["text"],
            "score": float(scores[i]),
        }
        for i in top
        if scores[i] >= config["score_threshold"]
    ]