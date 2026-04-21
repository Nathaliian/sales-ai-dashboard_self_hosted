from fastapi import FastAPI
from app.routes import router

app = FastAPI(...)
app.include_router(router)

# Add this 👇 — stops the 404 in Render logs
@app.get("/")
def root():
    return {"status": "Sales AI Dashboard is running"}