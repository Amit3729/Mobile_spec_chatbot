from fastapi import FastAPI
from app.api.routes import router

def create_app():
    app = FastAPI(
        title='Mobile specs RAG API',
        description='Ask anythings  about smartphone specification',
        version='1.0.0'
  

    )
        
    app.include_router(router)
    return app

app = create_app()

