import json
import os
import re
from typing import Optional, Tuple, Dict
from DrissionPage._base.chromium import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions
from concurrent.futures import ThreadPoolExecutor
from utils import singleton, logger


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
    谷歌浏览器136版本后不支持自动化指定默认用户目录启动
    """
    def __init__(self, user_path_on_off, headless_on_off):
        self.user_path_on_off: bool = user_path_on_off
        self.co: Optional[ChromiumOptions] = None
        self.headless_on_off = headless_on_off
        self.browser: Optional[Chromium] = None
        self.process_id: Optional[int] = None
        self._all_cookies_dicts: dict = {}
        self.executor = ThreadPoolExecutor(max_workers=10)

    def _init_browser(self) -> None:
        logger.info('<SingletonDrissionPage Class init>: Initialization Chromium Browser.')
        self.co = ChromiumOptions()
        self.co.set_argument("--start-maximized")
        self.co.set_local_port(port=9223)
        self.co.use_system_user_path(on_off=self.user_path_on_off)
        self.co.set_user_data_path(self.get_browser_by_user_dir_path())
        self.co.headless(on_off=self.headless_on_off)
        self.browser = Chromium(addr_or_opts=self.co)
        self.process_id = self.browser.process_id
        self.refresh_cookies()

    def _destroy_browser(self) -> None:
        logger.info('<SingletonDrissionPage Class destroy>: Destroy Chromium Browser.')
        self.co = None
        self.headless = False
        self.browser and self.browser.quit()
        self.browser = None
        self.process_id = None

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

    def init_browser_process(self):
        self._init_browser()
        return self

    def destroy_browser_process(self):
        self._destroy_browser()
        return self

    def get_current_browser_states(self):
        return self.browser and self.browser.states

    def get_cookies_from_chromium(self, cookies_key: str) -> Dict[str, str]:
        return self._all_cookies_dicts.get(cookies_key)

    def get_chromium_browser_signal(self) -> Tuple[Chromium, ThreadPoolExecutor]:
        return self.browser, self.executor

    @staticmethod
    def _process_domain(domain: str) -> str:
        parts = domain.split('.')
        if domain.endswith('.com.cn') and len(parts) >= 3:
            return '.' + '.'.join(parts[-3:])
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain):
            return domain
        if len(parts) >= 2:
            return '.' + '.'.join(parts[-2:])

    @staticmethod
    def get_browser_by_user_dir_path() -> str:
        browser_by_user_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "browser_user_dir")
        os.makedirs(browser_by_user_dir_path, exist_ok=True)
        return browser_by_user_dir_path
