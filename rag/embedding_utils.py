from openai import AzureOpenAI
from config.azure_openai_config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_MODEL,
    AZURE_OPENAI_API_VERSION
)

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def get_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model=AZURE_OPENAI_MODEL
    )
    return response.data[0].embedding
