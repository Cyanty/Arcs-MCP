import asyncio
import logging
from typing import Dict
from DrissionPage._functions.keys import Keys
from base import AbstractCrawler
from config import ZHIHU_ARIA_LABEL, ZHIHU_MARKDOWN2HTML
from environment import get_chromium_browser_signal
from extension.crawler_factory import get_crawler_setup_source
from extension.zhihu.client import ZhiHuClient
from utils import logger, pyperclip_paste


class ZhiHuCrawler(AbstractCrawler):

    def __init__(self):
        self.type_crawler = "ZhiHu Crawler"
        self.domain_crawler = ".zhihu.com"
        self._zhiHuClient = ZhiHuClient()

    async def article_path_proc(self, file_name: str, md_content: str):
        self._zhiHuClient.title_name = file_name
        self._zhiHuClient.md_content = md_content

    async def init_config(self, file_name: str, md_content: str, image_results=None):
        logger.info(f"[{self.type_crawler}] Start initializing the article operation.")
        await self.article_path_proc(file_name, md_content)

    async def run(self):
        logger.info(f'[{self.type_crawler}] Start publishing articles.')
        browser, executor = get_chromium_browser_signal()
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, self.tab_publish_actions, browser)

    def tab_publish_actions(self, browser) -> Dict:
        tab = browser.new_tab()
        try:
            tab.get(ZHIHU_MARKDOWN2HTML)  # 跳转md2html格式转换页面
            tab.refresh()
            tab.actions \
                .click(on_ele=tab.ele(self._zhiHuClient.loc_code_mirror_scroll_editor)) \
                .type(Keys.CTRL_A).key_down(Keys.BACKSPACE) \
                .input(self._zhiHuClient.md_content)
            tab.wait.load_start()

            def paste_adapt():
                tab.actions.click(on_ele=tab.ele(self._zhiHuClient.loc_nice_sidebar_zhihu_copy))
                tab.get(self._zhiHuClient.edit_url)
                tab.actions \
                    .click(on_ele=tab.ele(self._zhiHuClient.loc_title)).input(self._zhiHuClient.title_name) \
                    .click(on_ele=tab.ele(self._zhiHuClient.loc_content)).type(Keys.CTRL_V)

            pyperclip_paste(post_action=paste_adapt)
            tab.wait.load_start()

            tab.actions \
                .click(on_ele=tab.ele(self._zhiHuClient.loc_send_button)).wait(0.15) \
                .click(on_ele=tab.ele(self._zhiHuClient.loc_add_tag)).wait(0.15) \
                .click(on_ele=tab.ele(self._zhiHuClient.loc_tag_input)).input(ZHIHU_ARIA_LABEL).wait(0.25) \
                .click(on_ele=tab.ele(self._zhiHuClient.loc_select_button)).wait(0.15) \
                .click(on_ele=tab.ele(self._zhiHuClient.loc_publish_button))
            tab.wait.load_start()
            return {'result': AbstractCrawler.SUCCESS_RESULT}
        except Exception as e:
            logging.error(f'[{self.type_crawler}] Failure to publish the article! Cause of error:{e}')
            return {'result': AbstractCrawler.FAILURE_RESULT}
        finally:
            tab.close()

    async def login_as(self):
        browser, executor = get_chromium_browser_signal()
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(executor, self.login_as_sync, browser)

    def login_as_sync(self, browser):
        tab = browser.new_tab()
        try:
            tab.get(self._zhiHuClient.verify_login_url)
            tab.wait.load_start()
            get_crawler_setup_source().update({"zhihu": tab.url != self._zhiHuClient.login_url})
        except Exception as e:
            logger.error(f'[{self.type_crawler}] Login page failed to validate! Cause of error:{e}')
        finally:
            tab.close()


