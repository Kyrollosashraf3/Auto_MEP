from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.deps import get_current_user, RoleChecker
from app.config.settings import settings
from app.config.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Register attempt for email: {user_in.email}")
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        logger.warning(f"Registration failed - email already exists: {user_in.email}")
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user_db = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    logger.info(f"User registered successfully: {user_in.email} (id={user_db.id})")
    return user_db

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    logger.info(f"Login attempt for email: {form_data.username}")
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        logger.warning(f"Login failed for email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    logger.info(f"Login successful for email: {form_data.username} (id={user.id})")
    return {"access_token": access_token, "token_type": "bearer"}


# Example of a protected route using RBAC
# Only users with 'admin' or 'manager' roles can access this
allow_admins_only = RoleChecker(["admin", "manager"])

@router.get("/me", response_model=UserResponse)
def get_user_me(
    current_user: User = Depends(get_current_user)
):
    logger.debug(f"Token validated for user: {current_user.email}")
    return current_user

@router.get("/admin-only", response_model=dict)
def admin_only_route(
    current_user: User = Depends(allow_admins_only)
):
    """
    This route can only be accessed by 'admin' and 'manager' roles.
    """
    return {"message": f"Hello {current_user.name}, you have administrative access!"}
