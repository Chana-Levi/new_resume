import openai
from config import Config
from llama_index.core import VectorStoreIndex, Document
import json


def query(text, q):
    openai.api_key = Config.api_key
    if not text.strip():
        raise ValueError("The text provided is empty.")
    document = Document(text=text)
    index = VectorStoreIndex.from_documents([document])
    query_engine = index.as_query_engine()
    query_response = query_engine.query(q)
    return query_response.response


def parse_response_to_dict(query_response):
    if isinstance(query_response, str):
        query_response_dict = json.loads(query_response)
    else:
        query_response_dict = query_response
    return query_response_dict
