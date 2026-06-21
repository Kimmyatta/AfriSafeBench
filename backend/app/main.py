from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
from backend.app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title="AfriSafeBench API",
    description="API for evaluating LLM recognition of AI safety and governance risks in African healthcare AI deployments.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "service": "AfriSafeBench API",
        "docs": "/docs",
        "health": "/api/health",
    }
