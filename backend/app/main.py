from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auths, chats, completions

app = FastAPI(title="Travel AI Chat", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auths.router)
app.include_router(chats.router)
app.include_router(completions.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
