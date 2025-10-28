from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

# Create globale server settings
class ServerSettings(BaseSettings):
    DATABASE_URL: str
    PINECONE_API_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    GEMINI_API_KEY: str
    EMBEDDING_MODEL: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRY: int

    class Config:
        env_file = ".env"

server_settings = ServerSettings()