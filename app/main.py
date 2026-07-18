"""
Mega AI Agent - Main FastAPI Application
Production-ready AI agent with RAG, memory, and chat history.
"""
from fastapi import FastAPI, Request, status
#from fastapi.middleware.cors import CORSMiddleware
#from fastapi.responses import JSONResponse
#from fastapi.exceptions import RequestValidationError


from app.routes.base import router as home_router
from app.routes.chat import router as chat_router
from app.routes.auth import router as auth_router
from app.routes.projects import router as project_router
from app.routes.files import router as file_router
from app.routes.dashboard import router as dashboard_router




from app.config import get_logger
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Auto_MEP" ,
    version="0.0.1",
    description="Auto MEP using AI"
)


# DataBase
from app.db.database import Base
from app.db.database import engine

from app.models.user import User
from app.models.project import Project
from app.models.file import File

Base.metadata.create_all(bind=engine)


app.include_router(home_router) # Health check, usually kept public
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(file_router) 
app.include_router(dashboard_router)