from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routers.auth import router as auth_router
from routers.gmail import router as gmail_router
from routers.analysis import router as analysis_router


Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="CyberShield AI",
    description="AI-Powered Cybersecurity Platform",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cybershiledai.vercel.app",
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



app.include_router(auth_router)
app.include_router(gmail_router)
app.include_router(analysis_router)



@app.get("/")
def home():
    return {
        "success": True,
        "message": "CyberShield AI Backend is running",
        "version": "1.0.0"
    }



@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CyberShield AI"
    }


@app.get("/debug/routes")
def debug_routes():
    return {
        "routes": [
            {
                "path": route.path,
                "methods": list(route.methods or [])
            }
            for route in app.routes
        ]
    }