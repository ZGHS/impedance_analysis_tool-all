from fastapi import FastAPI
from routers import analysis
import os, uvicorn
import logging, sys
from fastapi.middleware.cors import CORSMiddleware
import io

# 配置标准输出和标准错误输出的编码为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# 配置基本日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = FastAPI(title="Data-Analysis-Service")
# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者指定你的前端地址，如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，包括 OPTIONS
    allow_headers=["*"],
)
app.include_router(analysis.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1",log_config=None, port=8000, reload=False)