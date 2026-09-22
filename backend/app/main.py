from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.evaluation import router as evaluation_router
from app.api.routes.chat import router as chat_router
from app.api.routes.auth import router as auth_router


app = FastAPI(
    title="Evaluated Guardrail Agent",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": "openai"
    }


# Chat API
app.include_router(
    chat_router,
    prefix="/api/v1"
)


# Authentication API
app.include_router(
    auth_router,
    prefix="/api/v1"
)
app.include_router(evaluation_router, prefix="/api/v1")