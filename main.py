from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Facilitating agent",
    version="1.0.0"
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)