from datetime import datetime
import json

from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class HospNameFilter(BaseFilter):

    async def __call__(self, message: Message) -> dict | None:
        with open("database/hospitals.json", "r", encoding="UTF-8") as file:
            data = json.load(file)
            try:
                hosp_name = data[message.text]
                return {"hosp_name": hosp_name}
            except KeyError:
                return None


