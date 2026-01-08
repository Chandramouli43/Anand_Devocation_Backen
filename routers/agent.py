# app/routers/agent.py
from fastapi import APIRouter, Depends
from core.dependencies import require_agent

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)

@router.get("/assigned-trips")
def get_assigned_trips(agent=Depends(require_agent)):
    return {"message": "Trips visible to this agent only"}
