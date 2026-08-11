
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import get_db
from models import User
from auth import SECRET_KEY, ALGORITHM




security = HTTPBearer(auto_error=False)




def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
   
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please login again."
        )

    token = credentials.credentials


    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token."
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token."
        )

  

    try:

        user_id = int(user_id)

    except (TypeError, ValueError):

        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in authentication token."
        )

    

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found. Please login again."
        )

   

    return user
