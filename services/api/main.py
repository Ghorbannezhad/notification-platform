from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.database.migrations import run_pending_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_pending_migrations()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "healthy"}
