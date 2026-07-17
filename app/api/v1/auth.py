from app.repositories.user_repository import user_repository
from app.schemas.token import ForgotPasswordRequest, ResetPasswordRequest
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.services.email_service import EmailService
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, get_password_hash
from app.services.auth_service import AuthService
from app.schemas.token import Token, LoginData, LoginRequest
from app.schemas.response import StandardResponse

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthService.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=StandardResponse[LoginData])
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, email=login_req.email, password=login_req.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}, expires_delta=refresh_token_expires
    )
    
    login_data = LoginData(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user
    )
    
    return StandardResponse(
        success=True,
        message="Login successful",
        data=login_data
    )


@router.post("/forgot-password", response_model=StandardResponse)
def forgot_password(req: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = user_repository.get_by_email(db, email=req.email)
    if not user:
        # Don't reveal if user exists for security reasons
        return StandardResponse(
            success=True,
            message="If an account exists, a password reset link has been sent.",
            data=None
        )
    
    expires = timedelta(minutes=5)
    reset_token = create_access_token(
        data={"sub": f"reset:{user.email}"},
        expires_delta=expires
    )

    magic_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    user.reset_token_expires = datetime.utcnow() + expires
    db.add(user)
    db.commit()
    
    # Send email in the background so API responds instantly
    background_tasks.add_task(EmailService.send_reset_password_email, req.email, magic_link)
    
    return StandardResponse(
        success=True,
        message="If an account exists, a password reset link has been sent.",
        data=None
    )

@router.post("/reset-password", response_model=StandardResponse)
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(req.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject: str = payload.get("sub")
        if not subject or not subject.startswith("reset:"):
            raise HTTPException(status_code=400, detail="Invalid token type")
        email = subject.split("reset:")[1]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Reset token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    user = user_repository.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.hashed_password = get_password_hash(req.new_password)
    db.add(user)
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Password reset successfully",
        data=None
    )