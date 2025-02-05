from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db_url: str
    redis_host: str
    redis_port: int


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        db_url=env("DB_URL"),
        redis_host=env("REDIS_HOST"),
        redis_port=env("REDIS_PORT"),
    )

