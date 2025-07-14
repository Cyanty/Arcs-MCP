# -*- coding: utf-8 -*-
import os
import contextlib
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from environment import get_sync_browser_destroy
from extension.crawler_factory import get_crawler_setup_source
from utils import logger, load_single_router_from_source
from web.llm.mcp import submit
from web.schemas.home import HomePageData


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    app_startup()
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(submit.mcp.session_manager.run())
        yield
    app_shutdown()

app = FastAPI(lifespan=lifespan)

# 使用 http://127.0.0.1:8001/submit/mcp 连接 mcp server
app.mount("/submit", submit.mcp.streamable_http_app())
# 挂载静态文件
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")),
          name="static")
# pip install Jinja2
# 创建一个templates（模板）对象，templates可以重用。
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    home_page_data = HomePageData(result_dict={source: {'result': '还没有要发布文章~'} for source in get_crawler_setup_source()})
    return templates.TemplateResponse("index.html", {"request": request, "data": home_page_data.model_dump()})


def app_startup():
    router_module_init()
    get_crawler_setup_source()


def app_shutdown():
    get_sync_browser_destroy()


def router_module_init():
    router_module_path = os.path.join(os.path.dirname(__file__), "routers")

    router_module_dir_paths = [
        os.path.join(router_module_path, router_module_dir)
        for router_module_dir in os.listdir(router_module_path)
        if
        not router_module_dir.startswith("__") and os.path.isfile(os.path.join(router_module_path, router_module_dir))
    ]

    for router_module_dir_path in router_module_dir_paths:
        router_module_file = os.path.basename(router_module_dir_path)
        router_module_name, ext = os.path.splitext(router_module_file)
        if ext != ".py":
            logger.info(f"{router_module_file} is not a python file, Skip.")
            continue

        module = load_single_router_from_source(module_name=f"web.routers.{router_module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router)
