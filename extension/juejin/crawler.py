import asyncio
from typing import Dict
from DrissionPage._functions.keys import Keys
from base import AbstractCrawler
from environment import get_chromium_browser_signal
from extension.crawler_factory import get_crawler_setup_source
from extension.juejin.client import JueJinClient
from utils import logger, request, pyperclip_copy


class JueJinCrawler(AbstractCrawler):

    def __init__(self):
        self.type_crawler = "JueJin Crawler"
        self.domain_crawler = ".juejin.cn"
        self._jueJinClient = JueJinClient()

    async def article_path_proc(self, file_name: str, md_content: str) -> Dict:
        return {
            'title': file_name,
            'id': None,
            'content': md_content,
            'encrypted_word_count': None,
            'origin_word_count': len(md_content),
        }

    async def init_config(self, file_name: str, md_content: str, image_results=None):
        logger.info(f"[{self.type_crawler}] Start initializing the article operation.")
        value: dict = await self.article_path_proc(file_name, md_content)
        self._jueJinClient.cookies = self.domain_crawler
        self._jueJinClient.create_json_data = value
        code, result = await self.request_post(
            url_type=self._jueJinClient.create_publish_url,
            json_data_type=self._jueJinClient.create_json_data
        )
        if 200 <= code < 300 and result['err_msg'] == 'success':
            value.update({'id': result['data']['id']})
            self._jueJinClient.host = value.get('id')
            self._jueJinClient.pre_json_data = value
            self._jueJinClient.json_data = value
            self._jueJinClient.md_content = md_content

    async def run(self):
        logger.info(f'[{self.type_crawler}] Start publishing articles.')
        code, result = await self.request_post(
            url_type=self._jueJinClient.pre_publish_url,
            json_data_type=self._jueJinClient.pre_json_data
        )
        if 200 <= code < 300 and result['err_msg'] == 'success':
            browser, executor = get_chromium_browser_signal()
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(executor, self.tab_publish_actions, browser)
        else:
            logger.error(f'[{self.type_crawler}] Failure to publish the article! Cause of error: Http Response Text -> {str(result)}')
            return {'result': AbstractCrawler.FAILURE_RESULT}

    async def request_post(self, url_type, json_data_type):
        return await request(method="POST",
                             url=url_type,
                             cookies=self._jueJinClient.cookies,
                             headers=self._jueJinClient.headers,
                             json_data=json_data_type,
                             params=self._jueJinClient.params,
                             timeout=10
                             )

    def tab_publish_actions(self, browser) -> Dict:
        tab = browser.new_tab()
        try:
            tab.get(self._jueJinClient.edit_url + self._jueJinClient.host)
            copy_adapt = lambda: tab.actions \
                .click(on_ele=tab.ele(self._jueJinClient.loc_content)).type(Keys.CTRL_V).wait(0.25)
            pyperclip_copy(self._jueJinClient.md_content, post_action=copy_adapt)
            tab.wait.load_start()
            tab.actions \
                .click(on_ele=tab.ele(self._jueJinClient.loc_publish_button)).wait(0.5) \
                .click(on_ele=tab.ele(self._jueJinClient.loc_confirm_publish_button)).wait(0.5)
            tab.wait.load_start()
            return {'result': AbstractCrawler.SUCCESS_RESULT}
        except Exception as e:
            logger.error(f'[{self.type_crawler}] Failure to publish the article! Cause of error:{e}')
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
            tab.get(self._jueJinClient.verify_login_url)
            tab.wait.load_start()
            get_crawler_setup_source().update({"juejin": tab.url != self._jueJinClient.login_url})
        except Exception as e:
            logger.error(f'[{self.type_crawler}] Login page failed to validate! Cause of error:{e}')
        finally:
            tab.close()
