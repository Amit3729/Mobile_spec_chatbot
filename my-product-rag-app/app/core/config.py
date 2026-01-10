import os

REQUIRED_VARS = [
    "MONGO_URI",
    "QDRANT_URI",
    "Qdrant_API_KEY",
    "GROQ_API_KEY",
    "REDIS_HOST",
    "REDIS_PORT",
]

def validate_env():
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        raise RuntimeError(f'Missing evc vars: {missing}')
    