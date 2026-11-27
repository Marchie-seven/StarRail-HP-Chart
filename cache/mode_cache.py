from typing import Any,Dict,List,Optional
from config.cache_config import get_json_cache, set_cache

d_key="charts:list"
async def get_mode(mode,major_version,minor_version):
    return await get_json_cache(f"{d_key}:{mode}:{major_version}:{minor_version}")
async def set_mode(mode,major_version,minor_version,data:List[Dict[str,Any]],expire:int=3600):
    return await set_cache(f"{d_key}:{mode}:{major_version}:{minor_version}",data,expire)
