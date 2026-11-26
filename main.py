from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.periods import router as period
from router.mode import router as mode
import models
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#允许的源，开发阶段允许所有，生产环境需要指定源
    allow_credentials=True,#允许携带cookie
    allow_methods=["*"],#允许的请求方法
    allow_headers=["*"],#允许的请求头
)
app.include_router(period)
app.include_router(mode)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)













