import ssl
from datetime import date as date_
from datetime import datetime
from urllib.parse import urljoin

from aiocache import Cache, cached
from aiocache.serializers import PickleSerializer
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field


class MealItem(BaseModel):
    date: date_ = Field(..., alias="date")
    menus: list[str] = Field(..., alias="menus")
    kcal: int | None = Field(..., alias="kcal")
    picture: str | None = Field(..., alias="picture")


ssl_context = ssl.create_default_context()
ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")


class Meal:
    @staticmethod
    async def fetch_menus(year: int, month: int, page: int):
        async with ClientSession() as session:
            return await (
                await session.post(
                    url="https://hansei.sen.hs.kr/197900/subMenu.do",
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                    },
                    data={
                        "viewType": "list",
                        "siteId": "SEI_00000617",
                        "pageIndex": page,
                        "arrMlsvId": "0",
                        "srhMlsvYear": year,
                        "srhMlsvMonth": month,
                    },
                    ssl=ssl_context,
                )
            ).text()

    @staticmethod
    async def parse_menus(page_content: str):
        soup = BeautifulSoup(page_content, "html.parser")

        board = soup.find("table", {"class": "board_type01_tb_list"})
        entries = board.find("tbody").find_all("tr")

        meals = []

        for entry in entries:
            all_attrs = entry.find_all("td")
            date = all_attrs[0].text.strip().replace(".", "")
            meal_id = all_attrs[2].find("a")["onclick"].split("'")[1].split("'")[0]

            meals.append({"date": date, "meal_id": meal_id})

        return meals

    @staticmethod
    async def get_menu_ids(year: int, month: int):
        first_page = await Meal.fetch_menus(year, month, 1)
        soup = BeautifulSoup(first_page, "html.parser")

        page_button_area = soup.find("div", {"class": "board_type01_pagenate"})

        if page_button_area is None:
            return []

        page_buttons = page_button_area.find_all("a")
        page_count = int(page_buttons[-1].text)

        meals = [meal for meal in await Meal.parse_menus(first_page)]

        for page in range(2, page_count + 1):
            meals += await Meal.parse_menus(await Meal.fetch_menus(year, month, page))

        return meals

    @staticmethod
    async def get_menu(meal_id: int, date: date_) -> MealItem:
        async with ClientSession() as session:
            soup = BeautifulSoup(
                await (
                    await session.post(
                        url="https://hansei.sen.hs.kr/dggb/module/mlsv/selectMlsvDetailPopup.do",
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                        },
                        data={"mlsvId": meal_id},
                        ssl=ssl_context,
                    )
                ).text(),
                "html.parser",
            )

            try:
                kcal = int(
                    soup.find("th", {"scope": "row"}, text="칼로리")
                    .find_next_sibling("td")
                    .text.split("kcal")[0]
                    .strip()
                )
            except:
                kcal = 0

            picture = soup.find("th", {"scope": "row"}, text="식단이미지")

            if picture is not None:
                picture = picture.find_next_sibling("td").find("img")["src"]
                picture = urljoin("https://hansei.sen.hs.kr", picture)

            return MealItem(
                date=date,
                menus=[
                    menu
                    for menu in (
                        item.strip()
                        for item in soup.find("th", {"scope": "row"}, text="식단")
                        .find_next_sibling("td")
                        .text.split(",")
                    )
                    if menu
                ],
                kcal=kcal,
                picture=picture,
            )

    @staticmethod
    @cached(ttl=86400, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def get(year: int, month: int):
        meals = []

        for data in await Meal.get_menu_ids(year, month):
            try:
                meals.append(
                    await Meal.get_menu(
                        meal_id=data["meal_id"],
                        date=datetime.strptime(data["date"], "%Y%m%d").date(),
                    )
                )
            except:
                pass

        return meals
