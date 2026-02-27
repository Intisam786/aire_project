from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from rag.embedding_utils import get_embedding
from config.azure_openai_config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_KEY,
    AZURE_SEARCH_INDEX
)

# Function to query Azure Cognitive Search using embedding

def search_knowledge_base(query_text, top_k=3):
    """
    Given a query, generate its embedding and retrieve top_k relevant documents from Azure Cognitive Search.
    """
    try:
        query_vector = get_embedding(query_text)
        client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY)
        )
        results = client.search(
            search_text=None,  # For pure vector search
            vectors=[{"value": query_vector, "fields": "snippet_vector", "k": top_k}],
            top=top_k
        )
        return [doc for doc in results]
    except Exception as e:
        import traceback
        print("Azure Search error:", e)
        traceback.print_exc()
        return []
