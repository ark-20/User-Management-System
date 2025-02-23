from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Optional
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import UserCreate, UserResponse
from .crud import create_user, get_user_by_email, get_users
from .models import User
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query # Add Query here
# ... other imports

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def basic_auth(request: Request, db: Session = Depends(get_db)):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        import base64
        decoded_auth = base64.b64decode(auth[6:]).decode("utf-8")
        username, password = decoded_auth.split(":")
        user = db.query(User).filter(User.username == username).first()
        if user and pwd_context.verify(password, user.password):
            return user
        else:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        created_user = create_user(db, user)
        return created_user
    except HTTPException as http_exc:  # Re-raise HTTPExceptions for FastAPI's handling
        raise http_exc
    except Exception as e: # Catch other exceptions
        db.rollback()
        print(f"Unexpected error during registration: {e}") # Log the error for debugging
        raise HTTPException(status_code=500, detail="Internal server error") # Return a JSON error response


@router.get("/users/", response_model=List[UserResponse], dependencies=[Depends(basic_auth)])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/search/", response_model=List[UserResponse], dependencies=[Depends(basic_auth)])
def search_users(db: Session = Depends(get_db),
                 user_id: Optional[int] = Query(None),
                 first_name: Optional[str] = Query(None),
                 last_name: Optional[str] = Query(None),
                 email: Optional[str] = Query(None),
                 username: Optional[str] = Query(None)):

    users = db.query(User)

    if user_id is not None:
        users = users.filter(User.id == user_id)
    if first_name is not None:
        users = users.filter(User.first_name == first_name)
    if last_name is not None:
        users = users.filter(User.last_name == last_name)
    if email is not None:
        users = users.filter(User.email == email)
    if username is not None:
        users = users.filter(User.username == username)

    found_users = users.all()
    return found_users