# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import re
from typing import Optional, List, Dict, Any
from DrissionPage._functions.keys import Keys
from DrissionPage._pages.mix_tab import MixTab
from base import AbstractCrawler
from config import WECHAT_PUBLIC_ACCOUNT, WECHAT_AUTHOR, WECHAT_MARKDOWN2HTML, WECHAT_ARTICLE_PUBLISH_MODE, \
    WECHAT_COVER_IMAGE
from environment import get_chromium_browser_signal
from extension.crawler_factory import get_crawler_setup_source
from extension.wechat.client import WeChatClient

from utils import request, logger, pyperclip_paste


class WeChatCrawler(AbstractCrawler):

    def __init__(self):
        self.type_crawler = "WeChat Crawler"
        self.domain_crawler = ".weixin.qq.com"
        self._weChatClient = WeChatClient()

    async def article_path_proc(self, file_name: str, md_content: str):
        # html_content = markdown2.markdown(md_content, extras=AbstractCrawler.extensions2)  # 已作废
        browser, executor = get_chromium_browser_signal()
        loop = asyncio.get_running_loop()
        html_content = await loop.run_in_executor(executor, self.tab_md2html_actions, browser, md_content)
        if html_content:
            return {
                'TITLE': file_name,
                'AUTHOR': WECHAT_AUTHOR,  # 自定义作者名称
                'DIGEST': None,
                'CONTENT': html_content,
                'CONTENT_SOURCE_URL': None,
                'THUMB_MEDIA_ID': WECHAT_COVER_IMAGE,  # 文章封面（必须为永久素材id）
                'X1_Y1_X2_Y2': None,
            }

    async def init_config(self, file_name: str, md_content: str, image_results: Optional[List[Dict[str, Any]]]):
        logger.info(f"[{self.type_crawler}] Start initializing and processing image links.")
        status_code, access_token_json = await request(method="POST",
                                                       url="https://api.weixin.qq.com/cgi-bin/stable_token",
                                                       json_data=WECHAT_PUBLIC_ACCOUNT,
                                                       timeout=10)
        self._weChatClient.access_token = access_token_json["access_token"]
        results = await self.image_process(image_results)
        if results:
            for image_path in results:
                if image_path and "old_image_url" in image_path and "new_image_url" in image_path:
                    md_content = md_content.replace(image_path["old_image_url"], image_path["new_image_url"])
        self._weChatClient.pre_json_data = await self.article_path_proc(file_name, md_content)

    async def run(self):
        logger.info(f'[{self.type_crawler}] Start publishing articles.')
        json_data = json.dumps(self._weChatClient.pre_json_data, ensure_ascii=False).encode('utf-8')
        status_code, result_json = await request("POST",
                                                   url=self._weChatClient.pre_publish_url,
                                                   content=json_data,
                                                   headers=self._weChatClient.headers,
                                                   timeout=10)
        if 200 <= status_code < 300:
            self._weChatClient.json_data = result_json["media_id"]
            self._weChatClient.mp_json_data = result_json["media_id"]

        if WECHAT_ARTICLE_PUBLISH_MODE == "1":
            if 200 <= status_code < 300 and result_json["media_id"] is not None:
                return {'result': AbstractCrawler.SUCCESS_RESULT}
            else:
                logging.error(f"[{self.type_crawler}] Failure to pre-publish the article! Cause of error:{str(result_json)}")
                return {'result': AbstractCrawler.FAILURE_RESULT}

        if WECHAT_ARTICLE_PUBLISH_MODE == "2":
            status_code, result_json = await self.request_post(self._weChatClient.publish_url, self._weChatClient.json_data)

        if WECHAT_ARTICLE_PUBLISH_MODE == "3":
            status_code, result_json = await self.request_post(self._weChatClient.mp_publish_url, self._weChatClient.mp_json_data)

        if 200 <= status_code < 300 and result_json.get("errcode") == 0:
            return {'result': AbstractCrawler.SUCCESS_RESULT}
        else:
            logging.error(f"[{self.type_crawler}] Failure to publish the article! Cause of error:{str(result_json)}")
            return {'result': AbstractCrawler.FAILURE_RESULT}

    async def request_post(self, url_type: str, json_data_type: Optional[Dict]):
        return await request("POST",
                             url=url_type,
                             json_data=json_data_type,
                             headers=self._weChatClient.headers,
                             timeout=10)

    async def image_process(self, image_results):
        if image_results:
            tasks = [self.image_upload(image_result) for image_result in image_results if image_result]
            results = await asyncio.gather(*tasks)
            return results

    async def image_upload(self, image_result):
        pattern = r'[^/]+\.(png|jpg|jpeg|gif|bmp|svg|webp)(?=\?|$)'  # 正则表达式匹配文件名
        match = re.search(pattern, image_result["image_url"])
        if match:
            image_filename = match.group(0)
            image_filenames = image_filename.split(".")
            files = {
                "media": (image_filenames[0] + ".png", image_result["image_content"], 'image/png'),
            }
            status_code, response_json = await request(method="POST",
                                                       url=self._weChatClient.uploadimg_url,
                                                       files=files,
                                                       timeout=10
                                                       )
            if 200 <= status_code < 300:
                return {"old_image_url": image_result["image_url"], "new_image_url": response_json["url"]}

    def tab_md2html_actions(self, browser, md_content):
        tab: MixTab = browser.new_tab()
        try:
            tab.get(WECHAT_MARKDOWN2HTML)  # 跳转md2html格式转换页面
            tab.refresh()

            tab.actions\
                .click(on_ele=tab.ele(self._weChatClient.loc_code_mirror_scroll_editor))\
                .type(Keys.CTRL_A).key_down(Keys.BACKSPACE)\
                .input(md_content).wait(0.15)
            tab.wait.load_start()

            paste_adapt = lambda: tab.actions.click(on_ele=tab.ele(self._weChatClient.loc_nice_sidebar_wechat_copy))
            html_content = pyperclip_paste(post_action=paste_adapt)
            return html_content
        except Exception as e:
            logger.error(f'[{self.type_crawler}] Failure to md2html conversion of the article! Cause of error:{e}')
        finally:
            tab.close()

    async def login_as(self):
        try:
            status_code, access_token_json = await request(method="POST",
                                                           url="https://api.weixin.qq.com/cgi-bin/stable_token",
                                                           json_data=WECHAT_PUBLIC_ACCOUNT,
                                                           timeout=3)
            get_crawler_setup_source().update({"wechat": "access_token" in access_token_json})
        except Exception as e:
            logger.error(f'[{self.type_crawler}] Failure to login as the account! Cause of error:{e}')
