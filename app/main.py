from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import Base, engine
from app.models import Item, Category, Order, IdempotencyKey

import webbrowser
import threading

def create_app():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.include_router(api_router, prefix="/router")

    @app.on_event("startup")
    async def on_startup():
        Base.metadata.create_all(bind=engine)
        # Abrir docs en el navegador después de 1 segundo
        threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8000/docs")).start()

    return app

app = create_app()