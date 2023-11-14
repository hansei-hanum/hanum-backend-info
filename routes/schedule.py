from fastapi import APIRouter, Depends, HTTPException

from core.auth.client import get_user
from core.neis.schedule import Schedule
from depends.require_auth import RequireAuth

router = APIRouter(prefix="/schedule")


@router.get("/{month}")
async def get_schedule_calender(month: int, userid: int = Depends(RequireAuth)):
    user = await get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    schedule = await Schedule.get(month)

    return {
        "message": "SUCCESS",
        "data": schedule,
    }


@router.get("/")
async def get_schedule(userid: int = Depends(RequireAuth)):
    user = await get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    schedule = await Schedule.get()

    return {
        "message": "SUCCESS",
        "data": schedule,
    }
