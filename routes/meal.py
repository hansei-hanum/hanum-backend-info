from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from core.auth.client import get_user
from core.neis.meal import Meal
from depends.require_auth import RequireAuth

router = APIRouter(prefix="/meal")


@router.get("/{month}")
async def get_meal_month(month: int, userid: int = Depends(RequireAuth)):
    user = await get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    meal = await Meal.get(datetime.now().year, str(month).zfill(2))

    return {
        "message": "SUCCESS",
        "data": meal,
    }
