from fastapi import FastAPI
from .database import engine, Base
from .admin.views import setup_admin
from .api.v1 import auth, users # Import your new router files

# Base.metadata.create_all(bind=engine)

# Alembic Migrations Workflow
''' 
Summary of Workflow
Whenever you change a model (e.g., adding a new column to User in app/models/accounts.py):

Run: alembic revision --autogenerate -m "added new column"
Run: alembic upgrade head
'''

# --- APP SETUP ---
app = FastAPI()

# --- API ROUTERS ---
app.include_router(auth.router, prefix="/user", tags=["Authentication"])
app.include_router(users.router, prefix="/user", tags=["Users"])

# --- ADMIN SETUP ---
setup_admin(app, engine)

