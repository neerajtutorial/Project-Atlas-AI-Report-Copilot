import os
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://atlas_app:atlas_dev_password@localhost:3307/atlas')
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
API_KEY = os.getenv('API_KEY', 'local-dev-key-change-me')
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'none').lower()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
COLLECTION = 'atlas_chunks'