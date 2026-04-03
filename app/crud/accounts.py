from sqlalchemy.orm import Session
from ..models.accounts import User, Profile, UserRole
from ..utils.security import hash_password

# --- USER GETTERS ---
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# --- USER ACTIONS ---
def create_user(db: Session, username: str, email: str, password: str):
    new_user = User(
        username=username, 
        email=email, 
        hashed_password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- PROFILE ACTIONS ---
def create_profile(db: Session, user_id: int):
    new_profile = Profile(user_id=user_id)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile