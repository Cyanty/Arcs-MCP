from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi import UploadFile, File, HTTPException

from extension.start_crawler import crawlers_start
from web.app import templates

router = APIRouter(prefix="/uploader", tags=["用户文章文件上传"])


# pip install python-multipart
@router.post("/mdfile", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are allowed")
    contents = await file.read()
    result_dict = await crawlers_start(file_name=file.filename, md_content=contents.decode("utf-8"))
    return templates.TemplateResponse("index.html", {"request": request, "result_dict": result_dict})
