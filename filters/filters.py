import json
import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message
from dateutil.parser import parse

logger = logging.getLogger(__name__)


class HospNameFilter(BaseFilter):

    async def __call__(self, message: Message) -> dict | None:
        with open("database/hospitals.json", "r", encoding="UTF-8") as file:
            data = json.load(file)
            try:
                hosp_name = data[message.text]
                return {"hosp_name": hosp_name}
            except KeyError:
                return None


class DateTimeFilter(BaseFilter):

    async def __call__(self, message: Message) -> dict | None:
        try:
            time = parse(fix_message, dayfirst=True)

            return {"time": time.strftime("%d.%m.%Y %H:%M:%S")}
        except:
            return None


class IsAdmin(BaseFilter):

    async def __call__(self, message: Message, admin_ids) -> bool:
        return message.from_user.id in admin_ids
