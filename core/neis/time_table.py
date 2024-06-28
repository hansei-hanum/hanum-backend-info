from collections import defaultdict
from datetime import date, datetime, timedelta

from aiocache import Cache, cached
from aiocache.serializers import PickleSerializer
from aiohttp import ClientSession
from pydantic import BaseModel, Field
import certifi
import ssl

from env import NeisEnv
from utils import timeutil

DEPARTMANT_BINDING = {
    "CLOUD_SECURITY": "클라우드보안과",
    "NETWORK_SECURITY": "네트워크보안과",
    "HACKING_SECURITY": "해킹보안과",
    "METAVERSE_GAME": "메타버스게임과",
    "GAME": "게임과",
}


class TimeTableItem(BaseModel):
    time: datetime = Field(..., alias="date")
    items: list[str] = Field(..., alias="data")


class TimeTable:
    @staticmethod
    @cached(ttl=86400, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def fetch(
        department: str,
        grade: int,
        classroom: int,
        start_date: date,
        end_date: date,
    ) -> list[TimeTableItem]:
        if department not in DEPARTMANT_BINDING:
            return None
        
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        async with ClientSession() as session:
            response = await session.get(
                "https://open.neis.go.kr/hub/hisTimetable",
                ssl=ssl_context,
                params={
                    "KEY": NeisEnv.API_KEY,
                    "Type": "json",
                    "ATPT_OFCDC_SC_CODE": NeisEnv.SC_CODE,
                    "SD_SCHUL_CODE": NeisEnv.SCHOOL_CODE,
                    "DDDEP_NM": DEPARTMANT_BINDING[department],
                    "GRADE": grade,
                    "CLASS_NM": classroom,
                    "TI_FROM_YMD": start_date.strftime("%Y%m%d"),
                    "TI_TO_YMD": end_date.strftime("%Y%m%d"),
                },
            )

            content = await response.json(content_type=None)
            timetable = content.get("hisTimetable", [None, None])[1]

            if not timetable:
                return None

            timetables = timetable.get("row", [])
            grouped_data = defaultdict(list)

            for timetable in timetables:
                date = timetable["ALL_TI_YMD"]
                grouped_data[date].append(timetable["ITRT_CNTNT"])

            for date in [
                (start_date + timedelta(days=i)).strftime("%Y%m%d")
                for i in range((end_date - start_date).days + 1)
            ]:
                grouped_data.setdefault(date, [])

            return [
                TimeTableItem(
                    date=datetime.strptime(time, "%Y%m%d"),
                    data=items,
                )
                for time, items in grouped_data.items()
            ]

    @staticmethod
    async def get(department: str, grade: int, classroom: int) -> list[TimeTableItem]:
        start_date, end_date = await timeutil.timetable_range()
        
        if department not in DEPARTMANT_BINDING:
            raise ValueError("INVALID_DEPARTMENT")
        
        return await TimeTable.fetch(
            department=department,
            grade=grade,
            classroom=classroom,
            start_date=start_date,
            end_date=end_date,
        )
