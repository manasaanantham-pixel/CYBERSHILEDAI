
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# =========================================================
# ROUTERS
# =========================================================

from routers.auth import router as auth_router
from routers.gmail import router as gmail_router
from routers.analysis import router as analysis_router
from routers.malware import router as malware_router


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="CyberShield AI",
    description="AI-Powered Cybersecurity Platform for Email and Malware Detection",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        # React / Vite
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        # Your current frontend
        "http://localhost:5174",
        "http://127.0.0.1:5174",

        # Other possible frontend ports
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# INCLUDE ROUTERS
# =========================================================

# Authentication
app.include_router(auth_router)

# Gmail
app.include_router(gmail_router)

# Email + Gmail Analysis
app.include_router(analysis_router)

# Malware Analysis
app.include_router(malware_router)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "success": True,
        "message": "CyberShield AI Backend is running",
        "version": "1.0.0",
        "services": {
            "authentication": True,
            "gmail_integration": True,
            "email_analysis": True,
            "malware_detection": True
        },
        "docs": "/docs"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "CyberShield AI"
    }

