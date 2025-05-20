from fastapi import APIRouter
from environment import get_browser_by_reconnect, get_sync_browser_init
from web.schemas.response import BaseResponse

router = APIRouter(prefix="/browser", tags=["浏览器对象管理"])


@router.get("/handle_confirm")
async def handle_confirm_post():
    get_browser_by_reconnect()
    return BaseResponse()


@router.get("/open")
async def open_browser():
    get_sync_browser_init()
    return BaseResponse()
