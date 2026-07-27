"""
Mega AI Agent - Main FastAPI Application
Production-ready AI agent with RAG, memory, and chat history.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from app.routes.base import router as home_router
from app.routes.chat import router as chat_router
from app.routes.auth import router as auth_router
from app.routes.projects import router as project_router
from app.routes.analyser import router as analyser_router

from app.routes.files import router as file_router
from app.routes.dashboard import router as dashboard_router
from app.routes.portal import router as portal_router
from app.routes.logs import router as logs_router


from app.config import get_logger , settings
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title= settings.APP_NAME ,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)   


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


# DataBase
from app.db.database import Base
from app.db.database import engine

from app.models.user import User
from app.models.project import Project
from app.models.file import File
from app.models.analysis_result import AnalysisResult

Base.metadata.create_all(bind=engine)


logger.info("Starting Auto MEP application...")
logger.info(f"App: {settings.APP_NAME} v{settings.APP_VERSION}")

app.include_router(home_router) # Health check, usually kept public
app.include_router(auth_router)

#app.include_router(chat_router)
app.include_router(project_router)
app.include_router(file_router) 
app.include_router(analyser_router)
app.include_router(dashboard_router)
app.include_router(portal_router)
app.include_router(logs_router)

logger.info("All routes registered successfully")