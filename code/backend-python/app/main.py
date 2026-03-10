import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

# Initialize FastAPI application
# This is equivalent to @SpringBootApplication in Java
app = FastAPI(
    title="TechWatch AI - Worker Service",
    description="Python Microservice for Scraping and RAG/AI processing",
    version="1.0.0"
)

# CORS Configuration (Cross-Origin Resource Sharing)
# Essential to allow the Next.js Frontend (port 3000) to communicate with this API (port 8000)
# We allow everything for development (*) but in production, we should restrict origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Health Check endpoint.
    Used to verify if the Python service is running correctly.
    """
    return {
        "status": "online",
        "service": "techwatch-ai-python",
        "version": "1.0.0"
    }

# Entry point for debugging within the IDE
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)