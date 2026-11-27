import json
from typing import Any

import redis.asyncio as redis
from sqlalchemy.util import await_

REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0



redis_config = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                           db=REDIS_DB,
                           decode_responses=True,
                           protocol=2)
async def get_json_cache(key:str):
    try:
        result=await redis_config.get(key)
        if result:
            return json.loads(result)
        return None
    except Exception as e:
        print(f"获取缓存失败:{e}")
        return None
async def set_cache(key:str,value:Any,expire:int=3600):
    try:
        value=json.dumps(value,ensure_ascii=False)
        await redis_config.setex(key,expire,value)
        return True
    except Exception as e:
        print(f"设置缓存失败:{e}")
        return False
















