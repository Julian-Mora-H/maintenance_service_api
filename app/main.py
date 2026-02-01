from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import Base, engine
from app.models import Item, Category, Order, IdempotencyKey

import webbrowser
import threading

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Open docs in the browser after 1 second
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8000/docs")).start()
    yield


def create_app():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)
    app.include_router(api_router, prefix="/router")
    return app

app = create_app()