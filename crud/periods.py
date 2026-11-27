from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from models.periods import Period
from config.star import AsyncSession
from sqlalchemy.orm import selectinload
from models.monsters import Monster
from cache.periods_cache import get_period_list, set_period_list, get_period_latest, set_period_latest, get_periods_id, \
    set_periods_id


async def get_periods(db:AsyncSession,mode:str,major_version:int|None = None,skip:int = 0,limit:int = 10,
                      version:str|None = None,half:str|None = None,
                      ):
    result = await get_period_list(mode,major_version,version,half,(skip // limit) + 1,limit)
    if result is not None:
        print("Redis缓存命中")
        return result
    print("redis缓存未命中")
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
    result = {
        "total": total,
        "items": [
            {
                **period.__dict__,
                "version": period.version,
                "monsters": [
                    {
                        "id": monster.id,
                        "name": monster.name,
                        "hp": monster.hp,
                        "room": monster.room,
                        "floor": monster.floor,
                        "note": monster.note,
                        "weakness": [
                            w.element for w in monster.weaknesses
                        ]
                    }
                    for monster in period.monsters
                ]
            }
            for period in periods.scalars().all()
        ],
        "page": (skip // limit) + 1,
        "page_size": limit
    }

    result=jsonable_encoder(result)
    await set_period_list(mode,major_version,version,half,(skip // limit) + 1,limit,result)
    return result


async def get_period_id(db:AsyncSession,id:str):
    result = await get_periods_id(id)
    if result is not None:
        return result
    stmt = select(Period).options(
        selectinload(Period.monsters).selectinload(Monster.weaknesses),
        selectinload(Period.rewards)
    ).where(Period.id == id)
    period = await db.execute(stmt)
    period =period.scalar_one_or_none()
    if period is None:
        return None
    result = {
            "id": id,
            "mode": period.mode,
            "major_version": period.major_version,
            "half": period.half,
            "version": f"{period.major_version}.{period.minor_version}",
            "rewards": period.rewards,
            "monsters":[{
        "id": monster.id,
        "name": monster.name,
        "hp": monster.hp,
        "room": monster.room,
        "floor": monster.floor,
        "note": monster.note,
        "weakness": [
            w.element for w in monster.weaknesses
        ]
    }
    for monster in period.monsters
],
            "start_time": period.start_time,
            "end_time": period.end_time,
            "total_hp": period.total_hp,
        }
    result=jsonable_encoder(result)
    await set_periods_id(id,result)
    return result



async def get_latests(db:AsyncSession):
    result = await get_period_latest()
    if result is not None:
        return result
    modes = [
        "forgotten",
        "fiction",
        "apocalypse",
        "arbitration"
    ]
    item=[]
    for mode in modes:
        stmt = select(Period).options(
            selectinload(Period.monsters).selectinload(Monster.weaknesses),
            selectinload(Period.rewards)
        ).where(Period.mode == mode).order_by(Period.start_time.desc()).limit(1)
        period = await db.execute(stmt)
        period = period.scalar_one_or_none()
        item.append({
            "id": period.id,
            "mode": period.mode,
            "major_version": period.major_version,
            "half": period.half,
            "version": f"{period.major_version}.{period.minor_version}",
            "rewards": period.rewards,
            "monsters": [{
                "id": monster.id,
                "name": monster.name,
                "hp": monster.hp,
                "room": monster.room,
                "floor": monster.floor,
                "note": monster.note,
                "weakness": [
                    w.element for w in monster.weaknesses
                ]
            }
                for monster in period.monsters
            ],
            "start_time": period.start_time,
            "end_time": period.end_time,
            "total_hp": period.total_hp,
        })
    item=jsonable_encoder(item)
    await set_period_latest(item)
    return item
























