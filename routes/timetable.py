from fastapi import APIRouter, Depends, HTTPException

from core.auth.client import get_user
from core.neis.time_table import TimeTable
from depends.require_auth import RequireAuth

router = APIRouter(prefix="/timetable")


@router.get("/")
async def get_timetable(userid: int = Depends(RequireAuth)):
    user = await get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    if (
        not user.verification.department
        or not user.verification.grade
        or not user.verification.classroom
    ):
        raise HTTPException(status_code=403, detail="USER_NOT_VERIFIED")

    timetable = await TimeTable.get(
        user.verification.department,
        user.verification.grade,
        user.verification.classroom,
    )

    return {
        "message": "SUCCESS",
        "data": timetable,
    }
