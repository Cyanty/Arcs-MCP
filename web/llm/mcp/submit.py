# submit.py
import os
from typing import Dict, List, Any
from mcp.server.fastmcp import FastMCP
from extension.crawler_factory import get_crawler_setup_source, get_crawler_reset_source
from extension.start_crawler import crawlers_start
from web.routers.browsers import open_browser
from web.routers.state import state
from web.schemas.state import ToggleState

mcp = FastMCP(name="SubmitArticleServer", stateless_http=True)

# Tool
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
async def submit_verify_login() -> Dict[str, bool]:
    """
    - 校验所有发布源平台的账号登录状态
    - 告知用户当前各发布源的账号登录状态的情况，然后结束对话
    """
    return await state()

@mcp.tool()
def get_submit_toggle_switch() -> Dict[str, bool]:
    """
    - 获取当前各发布源的发布开关状态
    - 告知用户当前各发布源的发布开关状态的情况，然后结束对话
    """
    return get_crawler_setup_source()

@mcp.tool()
async def update_submit_toggle_switch(toggle_state_list: List[ToggleState]) -> Dict[str, bool]:
    """
    - 更改一个或多个发布源平台的发布开关状态
    - 已知目前有如下发布源平台：cnblogs（博客园）、csdn（CSDN）、halo（Halo博客）、juejin（稀土掘金）、wechat（微信公众号）、zhihu（知乎）
    - 要求根据用户输入的发布源匹配对应的平台及开关状态，更新指定发布源平台的发布开关状态
    - 告知用户当前各发布源的发布开关状态的情况，然后结束对话
    """
    for toggle_state in toggle_state_list:
        if toggle_state.type in get_crawler_setup_source():
            get_crawler_setup_source()[toggle_state.type] = toggle_state.new_state
    return get_crawler_setup_source()

@mcp.tool()
async def submit_article_content_to_platforms(toggle_state_list: List[ToggleState],
                                              article_name: str,
                                              md_content: str) -> Dict[str, Any]:
    """
    - 将文章的文本内容作为参数（markdown格式），发送该文本至多个发布源平台上
    - 已知目前有如下发布源平台：cnblogs（博客园）、csdn（CSDN）、halo（Halo博客）、juejin（稀土掘金）、wechat（微信公众号）、zhihu（知乎）
    - 要求根据用户的输入判断需要发布的平台，并更新匹配的发布源平台的发布开关状态为true，其余未匹配的发布源平台的发布开关状态为false
    - 要求根据用户的输入提取出文章标题和文章内容，如果用户输入中未提及文章标题，需要你根据文章内容重新总结出一个合理的文章标题并替换
    - 此过程会请求接口或调用浏览器自动化操作，需等待程序执行完成
    - 发送完成后，根据返回结果告知用户当前各发布源的发布文章的情况，然后结束对话
    """
    await update_submit_toggle_switch(toggle_state_list)
    result_dict = await crawlers_start(file_name=article_name, md_content=md_content)
    get_crawler_reset_source()
    return result_dict

@mcp.tool()
async def submit_article_file_to_platforms(toggle_state_list: List[ToggleState],
                                           article_file_path: str) -> str | Dict[str, Any]:
    """
    - 将本地文件路径作为参数，以此读取文章的文本内容（markdown格式），并发送该文本至多个发布源平台上
    - 已知目前有如下发布源平台：cnblogs（博客园）、csdn（CSDN）、halo（Halo博客）、juejin（稀土掘金）、wechat（微信公众号）、zhihu（知乎）
    - 要求根据用户的输入判断需要发布的平台，并更新匹配的发布源平台的发布开关状态为true，其余未匹配的发布源平台的发布开关状态为false
    - 要求根据用户的输入提取出本地文件路径，以文件名作为文章标题
    - 此过程会请求接口或调用浏览器自动化操作，需等待程序执行完成
    - 发送完成后，根据返回结果告知用户当前各发布源的发布文章的情况，然后结束对话
    """
    if not os.path.exists(article_file_path):
        raise FileNotFoundError(f"文件不存在: {article_file_path}")
    await update_submit_toggle_switch(toggle_state_list)
    base_file_name = os.path.basename(article_file_path)
    # file_name, file_ext = os.path.splitext(base_file_name)
    # if file_ext != ".md":
    #     return "请上传一个 Markdown 文件。"
    with open(article_file_path, 'r', encoding='utf-8', newline='') as f:
        md_content = f.read()
    result_dict = await crawlers_start(file_name=base_file_name, md_content=md_content)
    get_crawler_reset_source()
    return result_dict

# Prompt
@mcp.prompt()
def help_open_browser_prompt() -> str:
    """帮助用户打开浏览器 提示词"""
    return "请帮我打开浏览器"

@mcp.prompt()
def verify_login_prompt() -> str:
    """验证所有平台登录状态 提示词"""
    return "请帮我验证所有平台的登录状态"

@mcp.prompt()
def get_toggle_switch_prompt() -> str:
    """获取发布开关状态 提示词"""
    return "请告诉我当前各平台的发布开关状态"

@mcp.prompt()
def update_toggle_switch_prompt(toggle_states: List[ToggleState]) -> str:
    """更新发布开关状态 提示词"""
    platforms = ", ".join([f"{state.type}({'开启' if state.new_state else '关闭'})"
                           for state in toggle_states])
    return f"请将以下平台的发布状态更新为: {platforms}"

@mcp.prompt()
def submit_article_content_prompt(platforms: List[str], title: str, content: str) -> str:
    """提交文章内容到平台 提示词"""
    platform_list = ", ".join(platforms)
    return (f"请将这篇文章发布到: {platform_list}\n"
            f"文章标题: {title}\n"
            f"文章内容: {content}...")

@mcp.prompt()
def submit_article_file_prompt(platforms: List[str], file_path: str) -> str:
    """提交文章文件到平台 提示词"""
    platform_list = ", ".join(platforms)
    return (f"请将文件发布到: {platform_list}\n"
            f"文件路径: {file_path}")
