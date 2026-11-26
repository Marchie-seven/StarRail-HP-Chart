from fastapi import APIRouter, Depends

from config.star import AsyncSession, get_db
from crud.mode import get_charts
from schemas.periods import Periods

router=APIRouter(prefix="/api/modes",tags=["mode"])

@router.get("/{mode}/chart")
async def get_chart(mode:str,major_version:int,version:str,db:AsyncSession=Depends(get_db)):
    minor_version = int(version.split(".")[1])
    periods = await get_charts(db,mode,major_version,minor_version)
    return Periods(mode=mode,periods=periods)














