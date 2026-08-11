
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel
from pydantic import EmailStr

from sqlalchemy.orm import Session

from database import get_db
from models import User

from auth import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)




class SignupRequest(BaseModel):

    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):

    email: EmailStr
    password: str




@router.post("/signup")
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db)
):

    name = data.name.strip()
    email = str(data.email).strip().lower()
    password = data.password


    if not name:

        raise HTTPException(
            status_code=400,
            detail="Name is required."
        )


    if len(password) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters."
        )


    existing_user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered. Please login."
        )


    try:

        hashed_password = hash_password(
            password
        )

    except Exception as error:

        print(
            "PASSWORD HASH ERROR:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to securely create password."
        )


    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password
    )


    db.add(user)
    db.commit()
    db.refresh(user)


    token = create_access_token(
        user.id
    )


    return {

        "success": True,

        "message": "Account created successfully.",

        "access_token": token,

        "token_type": "bearer",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email

        }

    }




@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    email = str(data.email).strip().lower()


    user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    password_valid = verify_password(
        data.password,
        user.hashed_password
    )


    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    token = create_access_token(
        user.id
    )


    return {

        "success": True,

        "message": "Login successful.",

        "access_token": token,

        "token_type": "bearer",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email

        }

    }
