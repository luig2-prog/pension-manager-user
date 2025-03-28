from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.routers import funds, transactions, notifications

app = FastAPI(
    title="Fondos API",
    description="API para gestión de fondos de inversión y pensiones",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(funds.router)
app.include_router(transactions.router)
app.include_router(notifications.router)

@app.get("/", tags=["health"])
async def health_check():
    return {"status": "healthy"}

# AWS Lambda handler
handler = Mangum(app) 