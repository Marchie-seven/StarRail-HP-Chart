from sqlalchemy import select, func
from models.periods import Period
from config.star import AsyncSession
from sqlalchemy.orm import selectinload
from models.monsters import Monster

async def get_periods(db:AsyncSession,mode:str,major_version:int|None = None,skip:int = 0,limit:int = 10,
                      version:str|None = None,half:str|None = None,
                      ):
    stmt = select(Period).options(
        selectinload(Period.monsters).selectinload(Monster.weaknesses),
        selectinload(Period.rewards)
    ).where(Period.mode == mode)
    if major_version is not None:
        stmt = stmt.where(Period.major_version == major_version)
    if version is not None:
        major,minor=map(int,version.split("."))
        stmt = stmt.where(Period.major_version == major).where(Period.minor_version == minor)
    if half is not None:
        stmt = stmt.where(Period.half == half)
    count_stmt=select(func.count()).select_from(stmt.subquery())
    stem=stmt.order_by(Period.major_version,Period.minor_version,Period.half,Period.id).offset(skip).limit(limit)
    periods = await db.execute(stem)
    count = await db.execute(count_stmt)
    total = count.scalar()
    return {"total":total,"items": [
    {
        **period.__dict__,
        "version": period.version
    }
    for period in periods.scalars().all()
],
            "page":(skip//limit)+1,
            "page_size":limit,
            }
























