import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config.config import Config, load_config
from handlers import user, admin
from keyboards.set_menu import set_admin_menu, set_user_menu
from middlewares.i18n import TranslatorRunnerMiddleware
from middlewares.session import DbSessionMiddleware
from utils.i18n import create_translator_hub

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.WARNING,
    filename="logging.log",
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
    "%(lineno)d - %(name)s:%(funcName)s - %(message)s",
    encoding="utf-8",
    filemode="w",
)


async def main():

    logger.info("Start Bot")
    config: Config = load_config()

    engine = create_async_engine(config.db_url)

    bot = Bot(
        config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    redis = Redis(host=config.redis_host, port=config.redis_port)
    storage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    dp = Dispatcher(storage=storage)
    dp.workflow_data.update(admin_ids=config.admin_ids)

    translator_hub: TranslatorHub = create_translator_hub()

    await set_user_menu(bot)
    await set_admin_menu(dp.workflow_data.get("admin_ids"), bot)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))

    dp.update.middleware(TranslatorRunnerMiddleware())

    dp.include_router(admin.admin_dialog)
    dp.include_router(user.router)
    setup_dialogs(dp)

    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stop Bot")
