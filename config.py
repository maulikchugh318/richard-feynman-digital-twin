from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    GEMINI_API_KEY: str

    MODEL_NAME: str = "gemini-2.5-flash"

    CHROMA_DB_PATH: str = "data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "feynman_knowledge"

    MEMORY_DB_PATH: str = "data/memory.db"
    MEMORY_COLLECTION_NAME: str = "feynman_memory"

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    TOP_K_RETRIEVAL: int = 5

    APP_ENV: str = "development"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()