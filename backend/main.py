from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routers.auth import router as auth_router
from routers.gmail import router as gmail_router
from routers.analysis import router as analysis_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="CyberShield AI",
    description="AI-Powered Cybersecurity Platform",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        # Vercel frontend
        "https://cybershiledai.vercel.app",

        # Local frontend
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        "http://localhost:5174",
        "http://127.0.0.1:5174",

        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(auth_router)
app.include_router(gmail_router)
app.include_router(analysis_router)


# Home / status endpoint
@app.get("/")
def home():
    return {
        "success": True,
        "message": "CyberShield AI Backend is running",
        "version": "1.0.0"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CyberShield AI"
    }
    