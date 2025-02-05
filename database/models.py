from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    hosp_name: Mapped[int] = mapped_column(String, nullable=False)
    inc_number: Mapped[str] = mapped_column(String, nullable=False)
    inc_child_number: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    resolution: Mapped[str] = mapped_column(String, nullable=False)
    sti_res: Mapped[bool] = mapped_column(Boolean, nullable=False)
    creator: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id"))
