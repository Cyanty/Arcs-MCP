from fastapi import APIRouter
from environment import browser_refresh_cookies, get_browser_by_reconnect
from web.schemas.response import BaseResponse

router = APIRouter(prefix="/browser", tags=["浏览器对象管理"])


@router.get("/handle_confirm")
async def read_root_post():
    get_browser_by_reconnect()
    return BaseResponse()


@router.get("/cookies/refresh")
async def read_root_post():
    browser_refresh_cookies()
    return BaseResponse()
