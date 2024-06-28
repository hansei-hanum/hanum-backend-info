from fastapi import APIRouter, Depends, HTTPException, Query
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
    department: str = Query(None, description="Department name"),
    grade: int = Query(None, description="Grade of the class"),
    classroom: int = Query(None, description="Classroom number"),
    userid: int = Depends(RequireAuth)
    ):
    user = await get_user(userid)

    if (
        not user.verification.department
        or not user.verification.grade
        or not user.verification.classroom
    ):
        raise HTTPException(status_code=403, detail="USER_NOT_VERIFIED")
    
    if (
        not department
        or not grade
        or not classroom
    ):
        timetable = await TimeTable.get(
            user.verification.department,
            user.verification.grade,
            user.verification.classroom,
        )
    else:
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