from collections import defaultdict
from datetime import date
from datetime import date as date_
from datetime import datetime

from aiocache import Cache, cached
from aiocache.serializers import PickleSerializer
from aiohttp import ClientSession
from pydantic import BaseModel, Field

from env import NeisEnv
from utils import timeutil

EXCLUDED_SCHEDULE_NAMES = [
    "휴업일",
    # "토요휴업일",
    # "일요휴업일",
    # "토요휴업일(대체)",
    # "일요휴업일(대체)",
    # "토요휴업일(대체공휴일)",
    # "일요휴업일(대체공휴일)",
]


class ScheduleItem(BaseModel):
    date: date_ = Field(..., alias="date")
    items: list[str] = Field(..., alias="data")


class Schedule:
    @staticmethod
    @cached(ttl=3600, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def fetch(start: date, end: date) -> list[ScheduleItem]:
        async with ClientSession() as session:
            response = await session.get(
                "https://open.neis.go.kr/hub/SchoolSchedule",
                params={
                    "KEY": NeisEnv.API_KEY,
                    "Type": "json",
                    "ATPT_OFCDC_SC_CODE": NeisEnv.SC_CODE,
                    "SD_SCHUL_CODE": NeisEnv.SCHOOL_CODE,
                    "AA_FROM_YMD": start.strftime("%Y%m%d"),
                    "AA_TO_YMD": end.strftime("%Y%m%d"),
                },
            )

            content = await response.json(content_type=None)

            schedule = content.get("SchoolSchedule", [None, None])[1]

            if not schedule:
                return None

            schedule = schedule.get("row", [])

            # group by AA_YMD
            grouped_schedule = defaultdict(list)

            for item in schedule:
                grouped_schedule[item.get("AA_YMD")].append(item)

            return [
                ScheduleItem(
                    date=datetime.strptime(date, "%Y%m%d").date(),
                    data=[
                        item.get("EVENT_NM")
                        for item in items
                        if item.get("EVENT_NM") not in EXCLUDED_SCHEDULE_NAMES
                    ],
                )
                for date, items in grouped_schedule.items()
            ]

    @staticmethod
    async def get(month: int = None) -> list[ScheduleItem]:
        start_date, end_date = await timeutil.month_range(month)

        return await Schedule.fetch(start_date, end_date)
