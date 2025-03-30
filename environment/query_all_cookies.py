# -*- coding: utf-8 -*-
import re
import platform
import subprocess
import time
import json
from typing import Dict, Optional, Tuple
from DrissionPage._base.chromium import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
from concurrent.futures import ThreadPoolExecutor
from utils import logger
from utils.decorator_util import singleton


@singleton
class SingletonDrissionPage:
    """
    from DrissionPage import ChromiumOptions
    co = ChromiumOptions()
    co.use_system_user_path()
    co.headless(True)
    co.save('environment/config1.ini')  # 把这个配置记录到 ini 文件

    from DrissionPage.common import configs_to_here
    configs_to_here()  # 项目文件夹会多出一个'dp_configs.ini'文件,页面对象初始化时会优先读取这个文件

    调式模式要求一个端口绑定一个用户文件目录，
    反之，默认系统用户目录不能绑定多个浏览器（默认双击打开浏览器时，再启动dp指定系统用户目录会报错）
    """
    def __init__(self):
        self.co: ChromiumOptions = ChromiumOptions()
        self.headless = False
        self.browser: Optional[Chromium] = None
        self._all_cookies_dicts: dict = {}
        self.executor = ThreadPoolExecutor(max_workers=20)
        self._init_browser()

    def _init_browser(self) -> None:
        logger.info('SingletonDrissionPage: Start Chromium Browser.')
        self.co.set_local_port(port=9222)
        self.co.use_system_user_path(on_off=True)
        self.co.headless(on_off=self.headless)
        self.browser = Chromium(addr_or_opts=self.co)
        self.refresh_cookies()

    def refresh_cookies(self):
        brower_cookies_as_json = self.browser.cookies(all_info=False).as_json()
        brower_cookies_list = json.loads(brower_cookies_as_json)
        self._tab_cookies_to_dict(brower_cookies_list)

    def _tab_cookies_to_dict(self, brower_cookies_list):
        for tab_cookies in brower_cookies_list:
            domain = self._process_domain(tab_cookies['domain'])
            if domain not in self._all_cookies_dicts:
                self._all_cookies_dicts[domain] = {}
            self._all_cookies_dicts[domain].update({tab_cookies['name']: tab_cookies['value']})

    @staticmethod
    def _process_domain(domain: str) -> str:
        parts = domain.split('.')
        if domain.endswith('.com.cn') and len(parts) >= 3:
            return '.' + '.'.join(parts[-3:])
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain):
            return domain
        if len(parts) >= 2:
            return '.' + '.'.join(parts[-2:])

    def get_cookies_from_chromium(self, cookies_key: str) -> Dict[str, str]:
        return self._all_cookies_dicts.get(cookies_key)

    def get_chromium_browser_signal(self) -> Tuple[Chromium, ThreadPoolExecutor]:
        return self.browser, self.executor


def _kill_browsers(browsers: list):
    """
      browsers = [
        "chrome",  # Google Chrome
        "firefox",  # Mozilla Firefox
        "msedge",  # Microsoft Edge
        "opera",  # Opera
        "safari",  # Safari (macOS)
        "brave",  # Brave Browser
        "chromium-browser"  # Chromium (Linux)
    ]

     chrome_names = {
        "Windows": ["chrome.exe"],  # chrome - Windows常见进程名
        "Linux": ["chrome", "google-chrome", "chromium"],  # chrome - Linux常见进程名变体
        "Darwin": ["Google Chrome"]  # chrome - macOS常见应用名
    }
    """
    system = platform.system()
    try:
        if system == "Windows":
            # Windows: 使用taskkill强制终止进程
            for browser in browsers:
                subprocess.run(
                    ["taskkill", "/F", "/IM", f"{browser}.exe", "/T"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True
                )
        elif system == "Linux":
            # Linux: 使用pkill终止进程
            for browser in browsers:
                subprocess.run(
                    ["pkill", "-f", browser],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
        elif system == "Darwin":
            # macOS: 使用killall终止进程
            for browser in browsers:
                subprocess.run(
                    ["killall", "-9", browser],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
        logger.info("已关闭所有浏览器进程")
        time.sleep(2)  # 等待进程终止完成
    except Exception as e:
        logger.error(f"操作失败: {str(e)}")


def _close_all_browsers():
    confirm = input("警告：这将强制关闭浏览器，未保存的数据会丢失！\n确认继续？(y/n): ").lower()
    if confirm == 'y':
        _kill_browsers(["chrome", ])  # 默认关闭谷歌浏览器
    else:
        logger.info("关闭浏览器操作已取消！")


def get_sync_browser_init():
    _close_all_browsers()
    SingletonDrissionPage()


def get_cookies_from_chromium(cookies_key: str) -> Dict[str, str]:
    return SingletonDrissionPage().get_cookies_from_chromium(cookies_key)


def get_chromium_browser_signal() -> Tuple[Chromium, ThreadPoolExecutor]:
    return SingletonDrissionPage().get_chromium_browser_signal()


def browser_refresh_cookies():
    SingletonDrissionPage().refresh_cookies()

