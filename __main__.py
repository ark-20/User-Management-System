import uvicorn

if __name__ == "__main__":
    uvicorn.run("user_management.main:app", reload=True)  # <-- Corrected line