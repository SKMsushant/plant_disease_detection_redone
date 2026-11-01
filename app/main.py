# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.model_service import predictor
from app.routers import predict
from .database import Base, engine
from .db_models import user, prediction
from app.routers import auth
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the model once
    print("[SYSTEM] Starting server: Loading deep learning model...")
    predictor.load_model()
    yield
    # Shutdown: Clean up if needed
    print("[SYSTEM] Shutting down server...")

app = FastAPI(
    title="BioShield AI - Plant Disease Detection API",
    description="Custom YOLOv8-Nano + 4-Head Transformer Model Serving API",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS (so web frontends, Streamlit, or mobile apps can talk to it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include prediction router
app.include_router(predict.router)
app.include_router(auth.router)

#Base.metadata.create_all(bind=engine)

app.mount('/uploads',StaticFiles(directory='uploads'),name='uploads')

@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "service": "BioShield AI",
        "model_loaded": predictor.model is not None
    }