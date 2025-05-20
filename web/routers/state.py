from fastapi import APIRouter
from extension.crawler_factory import get_crawler_setup_source
from extension.start_crawler import crawler_verify_login
from web.schemas.response import BaseResponse
from web.schemas.state import ToggleState

router = APIRouter(prefix="/state", tags=["发布源状态管理"])


@router.get("/")
async def state():
    return await crawler_verify_login()


@router.post("/toggle")
async def toggle_switch(toggle_state: ToggleState):
    if toggle_state.type in get_crawler_setup_source():
        get_crawler_setup_source()[toggle_state.type] = toggle_state.new_state
    return BaseResponse()
