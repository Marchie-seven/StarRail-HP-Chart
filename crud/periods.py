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
    return {
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

async def get_period_id(db:AsyncSession,id:str):
    stmt = select(Period).options(
        selectinload(Period.monsters).selectinload(Monster.weaknesses),
        selectinload(Period.rewards)
    ).where(Period.id == id)
    period = await db.execute(stmt)
    period =period.scalar_one_or_none()
    if period is None:
        return None
    return {
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

async def get_latests(db:AsyncSession):
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
    return item
























