from sqlalchemy.orm import selectinload
from config.star import AsyncSession
from sqlalchemy import select, func

from models import Period, Monster
from schemas.periods import Periods


async def get_charts(db:AsyncSession,mode:str,major_version:int,minor_version:int):
    stmt = (select(Period).options(
    selectinload(Period.monsters).selectinload(Monster.weaknesses))
            .where(Period.mode == mode,
            Period.major_version == major_version,Period.minor_version == minor_version)
    .order_by(Period.start_time.asc()))
    result=await db.execute(stmt)
    periods=result.scalars().all()
    return periods












