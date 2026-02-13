from typing import Any

import logging
from uuid import uuid4

import aiohttp
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

INDEX_NAME = ""
EMBEDDINGS_URL = "http://localhost:8001"

logger = logging.getLogger(__name__)

client = chromadb.PersistentClient()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50, length_function=len)


async def embed_text(text: str) -> list[float]:
    async with aiohttp.ClientSession(base_url=EMBEDDINGS_URL) as session, session.post(
        url="/embeddings", json={"text": text}, headers={"Content-Type": "application/json"}
    ) as response:
        data = await response.json()
    return data["embeddings"]


async def indexing(text: str, metadata: dict[str, Any] | None = None) -> list[str]:
    if not text.strip():
        logger.warning("Attempted to index empty text!")
        return []
    collection = client.get_or_create_collection(INDEX_NAME)
    chunks = splitter.split_text(text)
    ids = [str(uuid4()) for _ in range(len(chunks))]
    embeddings = []
    for chunk in chunks:
        embedding = await embed_text(chunk)
        embeddings.append(embedding)
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[metadata.copy() for _ in range(len(chunks))],
    )
    return ids


def retrieve(
        query: str,
        metadata_filter: dict[str, Any] | None = None,
        search_string: str | None = None,
        n_results: int = 10
) -> list[str]:
    collection = client.get_collection(INDEX_NAME)
    logger.info("Retrieving for query: '%s...'", query[:50])
    params = {}
    query_vector = ...
    params["query_embeddings"] = [query_vector]
    if metadata_filter is not None:
        params["where"] = metadata_filter
    if search_string is not None:
        params["where_document"] = {"$contains": search_string}
    params["n_results"] = n_results
    result = collection.query(**params, include=["documents", "metadatas", "distances"])
    return [
        f"""\
        **Document-ID:** {id_}
        **Relevance score:** {round(distance, 2)}
        **Document:**
        {document}
        """
        for id_, document, distance in zip(
            result["documents"][0], result["distances"][0], strict=False
        )
    ]
