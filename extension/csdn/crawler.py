import asyncio
import logging
from typing import Dict
from DrissionPage._functions.keys import Keys
from base import AbstractCrawler
from config import CSDN_LOC_TAG
from environment import get_chromium_browser_signal
from extension.crawler_factory import get_crawler_setup_source
from extension.csdn.client import CsdnClient
from utils import logger, github_proxy_url


class CsdnCrawler(AbstractCrawler):

    def __init__(self):
        self.type_crawler = "CSDN Crawler"
        self.domain_crawler = ".csdn.net"
        self._csdnClient = CsdnClient()

    async def article_path_proc(self, file_name: str, md_content: str):
        for old_str in github_proxy_url():
            md_content = md_content.replace(old_str, '')
        self._csdnClient.title_name = file_name
        self._csdnClient.md_content = md_content

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
            tab.get("https://editor.csdn.net/md/")  # "https://mp.csdn.net/mp_blog/creation/editor"
            tab.actions \
                .click(on_ele=tab.ele(self._csdnClient.loc_title)).input(self._csdnClient.title_name) \
                .click(on_ele=tab.ele(self._csdnClient.loc_content)).input(self._csdnClient.md_content).wait(0.25)
            tab.wait.load_start()
            tab.actions \
                .click(on_ele=tab.ele(self._csdnClient.loc_send_button)).wait(0.25) \
                .move_to(ele_or_loc=tab.ele(self._csdnClient.loc_add_tag)).wait(0.25) \
                .click(on_ele=tab.ele(self._csdnClient.loc_tag_input)).input(CSDN_LOC_TAG).wait(1) \
                .key_down(Keys.ENTER).wait(0.25) \
                .click(on_ele=tab.ele(self._csdnClient.loc_close_button)) \
                .click(on_ele=tab.ele(self._csdnClient.loc_publish_button))
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
            tab.get(self._csdnClient.verify_login_url)
            tab.wait.load_start()
            get_crawler_setup_source().update({"csdn": tab.url != self._csdnClient.login_url})
        except Exception as e:
            logger.error(f'[{self.type_crawler}] Login page failed to validate! Cause of error:{e}')
        finally:
            tab.close()


