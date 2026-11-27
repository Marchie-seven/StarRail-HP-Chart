from typing import Any,Dict,List,Optional
from config.cache_config import get_json_cache, set_cache

a_key="periods:list"
c_key="periods:latest"
b_key="periods:id"



def get_period(mode,major_version,version,half,page,page_size):
    return f"periods:list:{mode}:{major_version}:{version}:{half}:{page}:{page_size}"

async def get_period_list(mode,major_version,version,half,page,page_size):
    return await get_json_cache(get_period(mode,major_version,version,half,page,page_size))
async def set_period_list(mode,major_version,version,half,page,page_size,data:Dict[str,Any],expire:int=3600):
    return await set_cache(get_period(mode,major_version,version,half,page,page_size),data,expire)

async def get_period_latest():
    return await get_json_cache(c_key)
async def set_period_latest(data:Dict[str,Any],expire:int=3600):
    return await set_cache(c_key,data,expire)

async def get_periods_id(id):
    return await get_json_cache(f"{b_key}:{id}")
async def set_periods_id(id,data:Dict[str,Any],expire:int=3600):
    return await set_cache(f"{b_key}:{id}",data,expire)







