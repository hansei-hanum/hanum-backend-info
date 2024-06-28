from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Param

from core.auth.client import get_user
from core.neis.time_table import TimeTable
from depends.require_auth import RequireAuth

from pydantic import BaseModel

router = APIRouter(prefix="/timetable")

class TimetableDTO(BaseModel):
    department: str
    grade: int
    class_num: int

@router.get("/")
async def teacher_timetable(
    department: str = Param(...),
    grade:int = Param(...),
    classroom:int = Param(...),
    userid: int = Depends(RequireAuth)
    ):
    user = await get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    if user.verification.type != "TEACHER":
        raise HTTPException(status_code=403, detail="UNAUTHORIZED")

    timetable = await TimeTable.get(
        department,
        grade,
        classroom,
    )

    if not timetable:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    return {
        "message": "SUCCESS",
        "data": timetable,
    }