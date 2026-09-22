
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import Base, engine

from routers.auth import router as auth_router
from routers.gmail import router as gmail_router
from routers.analysis import router as analysis_router


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="CyberShield AI",
    description="AI-Powered Cybersecurity Platform",
    version="1.0.0"
)


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cybershiledai.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(auth_router)
app.include_router(gmail_router)
app.include_router(analysis_router)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def home():

    return {
        "success": True,
        "message": "CyberShield AI Backend is running",
        "version": "1.0.0"
    }


# =========================================================
# HEALTH CHECK ENDPOINT
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "CyberShield AI"
    }


# =========================================================
# SERVER START COMMAND
# =========================================================

# Run using:
# uvicorn main:app --host 0.0.0.0 --port $PORT