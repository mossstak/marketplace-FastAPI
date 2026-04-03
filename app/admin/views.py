from fastapi import Request
from sqlalchemy import Enum as SqlEnum
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from ..database import Base, SessionLocal, engine
from ..models.accounts import User, Profile, UserRole
from ..core.config import settings
from ..utils.security import verify_password, hash_password, create_access_token, SECRET_KEY, ALGORITHM, oauth2_scheme, get_current_user

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")

        with SessionLocal() as db:
            user = db.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.hashed_password):
                if user.role == UserRole.ADMIN:
                    request.session.update({"token": "admin-session-granted"})
                    return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "token" in request.session

class UserAdmin(ModelView, model=User):
    # column_list usually works best as strings
    column_list = ["id", "username", "email", "role", "is_active"]
    
    # Try reverting these to the Model attributes (not strings)
    column_searchable_list = [User.username, User.email]
    # column_filters = [User.is_active]
    
    name = "User"
    category = "Accounts"
    icon = "fa-solid fa-user"


class ProfileAdmin(ModelView, model=Profile):
    column_list = ["id", "bio", "user_id"]
    name = "Profile"
    category = "Accounts"
    icon = "fa-solid fa-address-card"

# SQLAdmin
def setup_admin(app, engine):
    # Initialize the Admin interface
    authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    
    # Add all your views here
    admin.add_view(UserAdmin)
    admin.add_view(ProfileAdmin)
    
    return admin