# routers/analysis.py
from fastapi import APIRouter, UploadFile, HTTPException, Body, Request
from pydantic import BaseModel
from utils.analyzer import analyze
from utils.plotter import plot_to_plotly
import pandas as pd
import os
from typing import List
from fastapi.responses import JSONResponse
from utils.impedance_analysis_tool import plot_fun
from pathlib import Path

router = APIRouter()
# 2. 请求体模型
class FilePathsRequest(BaseModel):
    file_paths: List[str]
    pos_flow: int
@router.post("/api/analyze")
async def analyze_file(payload: FilePathsRequest):
    file_paths=payload.file_paths
    pos_flow=payload.pos_flow
    plotly_json_list=plot_fun(file_paths,pos_flow)
    
    for f in file_paths:
        delete_file(f)
    
    print("后端收到的文件路径数量：", len(file_paths))  # ✅ 用 len()
    return {
        "message": "成功接收文件路径数组",
        "count": len(file_paths),
        "plotly_jsons": plotly_json_list  # 或者后续返回真实的图表数据
    }
    
    
    
def delete_file(file_path: str | Path, *, missing_ok: bool = True) -> None:
    """
    安全删除单个文件。

    Parameters
    ----------
    file_path : str | Path
        待删除文件的路径。
    missing_ok : bool, default True
        True  -> 文件不存在时静默返回；
        False -> 文件不存在时抛出 FileNotFoundError。
    """
    p = Path(file_path).expanduser().resolve()

    if not p.exists():
        if missing_ok:
            print(f"文件不存在，已跳过：{p}")
            return
        raise FileNotFoundError(p)

    if not p.is_file():
        raise IsADirectoryError(f"路径指向的不是文件（或是一个目录）：{p}")

    p.unlink()          # 真正删除
    print(f"已删除文件：{p}")
# @router.post("/api/analyze2")
# async def analyze_file2(request: Request):
#     raw_body = await request.body()
#     print("🔥 原始请求体 bytes:", raw_body)
#     try:
#         body_text = raw_body.decode()
#         print("🔥 原始请求体文本:", body_text)
#     except:
#         body_text = "[无法解码]"
#     return JSONResponse({
#         "msg": "已收到请求，但未处理",
#         "raw_body": body_text  # 打印原始 JSON 文本
#     })

# 定义一个固定的保存上传文件的目录，比如当前项目下的 uploads/
UPLOAD_DIR = "uploads"  # 直接放在项目根目录下
os.makedirs(UPLOAD_DIR, exist_ok=True)  # 如果目录不存在则创建它
@router.post("/api/upload")
async def upload_file(file: UploadFile):
    try:
        # 构造保存的文件路径，比如 uploads/uploaded_file.csv
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # 将上传的文件内容保存到本地
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return {
            "message": "文件已成功上传并保存",
            "filename": file.filename,
            "saved_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件时出错: {str(e)}")


@router.post("/api/test")
async def test():
    return {
            "message": "文件已成功上传并保存",
            "filename": "test.csv",
            "saved_path": "test/test.csv"
        }