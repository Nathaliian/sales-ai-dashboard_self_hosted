from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Sales AI Dashboard",
    description="Ask natural language questions about sales data",
    version="1.0.0",
)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "Sales AI Dashboard is running"}