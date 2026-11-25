import inspect

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from crud.periods import get_periods as get_periodss, get_period_id, get_latests
from config.star import get_db

router = APIRouter(prefix="/api/periods",tags=["periods"])

@router.get("")
async def get_periods(
        mode:str,
        major_version:int|None = None,
        version:str|None = None,
        half:str|None = None,
        db:AsyncSession=Depends(get_db),
        page:int=Query(1,description="页码"),
        page_size:int=Query(20,le=100,ge=1,description="每页数量"),
):
    skip = (page - 1) * page_size
    result = await get_periodss(db,mode,major_version,skip=skip,limit=page_size,version=version,half=half)
    return result

@router.get("/latest")
async def get_latest(
        db:AsyncSession=Depends(get_db),
):
    result = await get_latests(db)
    return result

@router.get("/{id}")
async def get_period(
        id:str,
        db:AsyncSession=Depends(get_db),
):
    result = await get_period_id(db,id)
    return result






























