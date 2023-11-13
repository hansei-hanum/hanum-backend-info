from fastapi import APIRouter, Depends
from depends import RequireAuth
from fastapi import HTTPException
from micro import auth
from neis import Meal
from datetime import datetime

router = APIRouter()


@router.get("/{month}")
async def get_meal_month(month: int, userid: int = Depends(RequireAuth)):
    user = await auth.get_user(userid)

    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    meal = await Meal.get(datetime.now().year, month)

    return {"message": "SUCCESS", "data": meal}
