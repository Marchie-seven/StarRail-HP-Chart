from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload
from schemas.periods import Period as PeriodSchema
from cache.mode_cache import set_mode, get_mode
from config.star import AsyncSession
from sqlalchemy import select, func

from models import Period, Monster
from schemas.periods import Periods


async def get_charts(db:AsyncSession,mode:str,major_version:int,minor_version:int):
    result = await get_mode(mode,major_version,minor_version)
    if result is not None:
        return result
    stmt = (select(Period).options(
    selectinload(Period.monsters).selectinload(Monster.weaknesses))
            .where(Period.mode == mode,
            Period.major_version == major_version,Period.minor_version == minor_version)
    .order_by(Period.start_time.asc()))
    result=await db.execute(stmt)
    periods=result.scalars().all()
    result=[PeriodSchema.model_validate(period).model_dump(mode="json") for period in periods]
    await set_mode(mode,major_version,minor_version,result)
    return result












