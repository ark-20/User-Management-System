from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Import StaticFiles
import os

from .models import Base
from .database import engine
from .routes import router

app = FastAPI()

# CORS Configuration (Important):
origins = [
    "http://localhost",  # For local development
    "http://127.0.0.1",  # For local development
    "http://127.0.0.1:8080",  # If you're running your HTML on a different port
    "null"  # Only needed if you're opening the HTML file directly from the file system (less secure)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Important if you're using cookies or sessions
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Ensure Static Directory Exists
static_directory = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_directory):
    os.makedirs(static_directory)  # Ensure the directory exists

# Mount Static Files (Crucial):
app.mount("/static", StaticFiles(directory=static_directory), name="static")

# Initialize Database
Base.metadata.create_all(bind=engine)

# Include Routes
app.include_router(router)

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}

# Database Connection Events
@app.on_event("startup")
async def startup_db():
    print("Database connection successful!")  # Replace with actual DB connection logic

@app.on_event("shutdown")
async def shutdown_db():
    print("Database connection closed!")  # Replace with actual DB disconnect logic

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
