# submit.py
from typing import Dict
from mcp.server.fastmcp import FastMCP
from extension.crawler_factory import get_crawler_setup_source
from web.routers.browsers import open_browser
from web.routers.state import state
from web.schemas.state import ToggleState

mcp = FastMCP(name="SubmitServer", stateless_http=True)

@mcp.tool()
async def help_open_browser() -> str:
    """
    - 帮助用户打开一次浏览器
    - 告知用户浏览器是否已成功打开，然后结束对话
    """
    baseResponse = await open_browser()
    if baseResponse.code == 200:
        return "浏览器已成功打开。"
    else:
        return "浏览器打开失败。"

@mcp.tool()
async def submit_verify_login() -> dict[str, bool]:
    """
    - 校验所有发布源平台的账号登录状态
    - 告知用户当前各发布源的账号登录状态的情况，然后结束对话
    """
    return await state()

@mcp.tool()
async def update_submit_toggle_switch(toggle_state: ToggleState) -> dict[str, bool]:
    """
    - 更改指定发布源平台的发布开关状态
    - 已知目前有如下发布源平台：cnblogs（博客园）、csdn（CSDN）、halo（Halo博客）、juejin（稀土掘金）、wechat（微信公众号）、zhihu（知乎）
    - 要求根据用户输入的发布源匹配对应的平台及开关状态，更新指定发布源平台的发布开关状态
    - 告知用户当前各发布源的发布开关状态的情况，然后结束对话
    """
    if toggle_state.type in get_crawler_setup_source():
        get_crawler_setup_source()[toggle_state.type] = toggle_state.new_state
    return get_crawler_setup_source()

@mcp.tool()
def get_submit_toggle_switch() -> Dict[str, bool]:
    """
    - 获取当前各发布源的发布开关状态
    - 告知用户当前各发布源的发布开关状态的情况，然后结束对话
    """
    return get_crawler_setup_source()

