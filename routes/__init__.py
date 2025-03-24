from fastapi import FastAPI
from .schedule import router as schedule_router
from .meal import router as meal_router
from .timetable import router as timetable_router


def include_router(app: FastAPI):
    app.include_router(timetable_router)
    app.include_router(schedule_router)
    app.include_router(meal_router)
