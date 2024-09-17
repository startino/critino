from pydantic import SecretStr
from langchain_openai import OpenAIEmbeddings
import numpy as np
import requests
import json


def get_embedding(text, api_key, model="text-embedding-3-small"):
    embeddings = OpenAIEmbeddings(api_key=api_key)

    print(embeddings.__json__)
    return embeddings


class InMemoryVectorStore:
    def __init__(self, api_key: SecretStr):
        self.api_key = api_key
        self.documents = []
        self.embeddings = []

    def add_document(self, doc):
        embedding = get_embedding(doc, self.api_key)  # Generate embedding using OpenAI
        self.documents.append(doc)
        self.embeddings.append(embedding)

    def add_documents(self, docs):
        for doc in docs:
            self.add_document(doc)

    def similarity_search(self, query_embedding, k=3):
        similarities = np.dot(self.embeddings, query_embedding)  # Compute dot product
        top_k_indices = np.argsort(similarities)[-k:][
            ::-1
        ]  # Get indices of top k similarities
        return [(self.documents[i], similarities[i]) for i in top_k_indices]
