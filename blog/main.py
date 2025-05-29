from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from blog.database.database import engine, Base
from blog.routes import user, blog, auth, camera

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    description="API for managing users with authentication",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "useBasicAuthenticationWithAccessCodeGrant": True
    }
)

# Configure templates
templates = Jinja2Templates(directory="blog/templates")

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(camera.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}