from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ...models.accounts import User, UserRole
from ...utils.security import get_current_user, RoleChecker

router = APIRouter()

@router.get("/me")
def get_user_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "profile": {
            "bio": current_user.profile.bio if current_user.profile else ""
        }
    }

@router.get("/admin-only", dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def get_admin_only():
    return {"message": "This is an admin-only endpoint"}