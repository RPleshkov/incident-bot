from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Incident, User
from sqlalchemy.dialects.postgresql import insert as upsert


async def upsert_user(
    session: AsyncSession,
    tg_id: int,
    first_name: str,
    last_name: str | None = None,
):

    stmt = upsert(User).values(
        {
            "tg_id": tg_id,
            "first_name": first_name,
            "last_name": last_name,
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["tg_id"],
        set_=dict(
            first_name=first_name,
            last_name=last_name,
        ),
    )
    await session.execute(stmt)
    await session.commit()


async def set_incident(
    session,
    time,
    hosp_name,
    inc_number,
    inc_child_number,
    description,
    resolution,
    sti_res,
    creator,
):
    session.add(
        Incident(
            time=time,
            hosp_name=hosp_name,
            inc_number=inc_number,
            description=description,
            inc_child_number=inc_child_number,
            resolution=resolution,
            sti_res=sti_res,
            creator=creator,
        )
    )

    await session.commit()
