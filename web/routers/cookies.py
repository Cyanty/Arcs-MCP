from fastapi import APIRouter
from environment import browser_refresh_cookies

router = APIRouter(prefix="/cookies", tags=["浏览器cookies管理"])


@router.get("/refresh")
async def read_root_post():
    browser_refresh_cookies()
    return {"response": 200}
