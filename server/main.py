from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.facility_endpoints import router as facilities_router
from app.api.data_endpoints import router as data_endpoints
from app.api.user_endpoints import router as user_endpoints
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Onus",
    version="1.0.0"
)

# Cors middleware to only allow the client to access the backend with any method and any header
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # client server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(facilities_router)
app.include_router(data_endpoints)
app.include_router(user_endpoints)

# Default GET endpoint
@app.get("/")
async def root():
    return {"message": "Onus server up and running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)