import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config.config import Config, load_config
from handlers import user
from middlewares.session import DbSessionMiddleware

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():

    logger.info("Start Bot")
    config: Config = load_config()

    engine = create_async_engine(config.db_url)

    bot = Bot(
        config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    redis = Redis(host=config.redis_host, port=config.redis_port)
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))

    dp.include_router(user.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stop Bot")
