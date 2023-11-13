from aiohttp import ClientSession
from datetime import datetime
from bs4 import BeautifulSoup
from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer


class Meal:
    @staticmethod
    async def _fetch(year: int, month: int, page: int):
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
                )
            ).text()

    @staticmethod
    async def _parse(page_content: str):
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
    async def _get_ids(year: int, month: int):
        first_page = await Meal._fetch(year, month, 1)
        soup = BeautifulSoup(first_page, "html.parser")

        page_button_area = soup.find("div", {"class": "board_type01_pagenate"})

        if page_button_area is None:
            return []

        page_buttons = page_button_area.find_all("a")
        page_count = int(page_buttons[-1].text)

        meals = [meal for meal in await Meal._parse(first_page)]

        for page in range(2, page_count + 1):
            meals += await Meal._parse(await Meal._fetch(year, month, page))

        return meals

    @staticmethod
    async def _get_menu(meal_id: int):
        async with ClientSession() as session:
            data = await (
                await session.post(
                    url="https://hansei.sen.hs.kr/dggb/module/mlsv/selectMlsvDetailPopup.do",
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                    },
                    data={"mlsvId": meal_id},
                )
            ).text()

            meal_data = (
                data.split('<th scope="row">식단</th>')[1]
                .split('<td class="ta_l">')[1]
                .split("</td>")[0]
                .strip()
                .split(",")
            )

            return meal_data

    @staticmethod
    @cached(ttl=86400, cache=Cache.MEMORY, serializer=PickleSerializer())
    async def get(year: int, month: int):
        meal_ids = await Meal._get_ids(year, month)

        meals = []

        for meal_id in meal_ids:
            meals.append(
                {
                    "date": datetime.strptime(meal_id["date"], "%Y%m%d").strftime(
                        "%Y-%m-%dT00:00:00"
                    ),
                    "data": await Meal._get_menu(meal_id["meal_id"]),
                }
            )

        return meals
