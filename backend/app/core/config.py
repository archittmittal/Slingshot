import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Model Configuration
    MODEL_PATH: str = "microsoft/phi-4"  # Default SLM
    INFERENCE_ENGINE: str = "vllm"        # vllm | transformers
    DEVICE: str = "cuda"                  # Use 'cuda' for ROCm/CUDA
    
    # RAG Configuration
    QDRANT_URL: str = "http://localhost:6333"
    COLLECTION_NAME: str = "vidya_sovereign"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Database
    DATABASE_URL: str = "sqlite:///./vidya_os.db"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
