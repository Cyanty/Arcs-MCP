from dataclasses import dataclass
from typing import Annotated
from DrissionPage._functions.by import By
from base import AbstractBrowserClient
from config import ZHIHU_ARIA_LABEL
from utils.field_metadata_util import Description, ExampleValue


@dataclass
class ZhiHuClient(AbstractBrowserClient):

    _title_name: Annotated[
        str,
        Description("zhihu 发布文章标题"),
        ExampleValue("ZHIHU 测试发布文章标题")
    ] = None

    _md_content: Annotated[
        str,
        Description("zhihu 发布文章内容"),
        ExampleValue("ZHIHU 测试发布文章内容 ...")
    ] = None

    @property
    def edit_url(self) -> str:
        return 'https://zhuanlan.zhihu.com/write'

    @property
    def loc_title(self):  # 标题
        return By.XPATH, '//textarea[contains(@placeholder,"请输入标题")]'

    @property
    def loc_content(self):  # 内容
        return By.XPATH, '//div[@class="DraftEditor-root"]'

    @property
    def loc_send_button(self):  # 发布设置按钮
        return By.XPATH, '//svg[@class="Zi Zi--ArrowDown" and @fill="currentColor"]'

    @property
    def loc_add_tag(self):  # 添加话题按钮
        return By.XPATH, '//button[contains(text(),"添加话题")]'

    @property
    def loc_tag_input(self):  # 搜索话题输入框
        return By.XPATH, '//input[contains(@placeholder,"搜索话题")]'

    @property
    def loc_select_button(self):  # 选中文章话题标签
        return By.XPATH, f'//button[contains(text(),"{ZHIHU_ARIA_LABEL}")]'

    @property
    def loc_publish_button(self):  # 发布按钮
        return By.XPATH, '//button[contains(@class, "Button") and contains(text(),"发布")]'

    @property
    def title_name(self):
        return self._title_name

    @title_name.setter
    def title_name(self, value: str):
        self._title_name = value

    @property
    def md_content(self):
        return self._md_content

    @md_content.setter
    def md_content(self, value: str):
        self._md_content = value

    # md2html格式转换页面元素
    @property
    def loc_code_mirror_scroll_editor(self):
        return By.XPATH, '//div[@class="CodeMirror-scroll"]'

    @property
    def loc_nice_sidebar_zhihu_copy(self):
        return By.XPATH, '//*[@id="nice-sidebar-zhihu"]'

    @property
    def verify_login_url(self) -> str:
        return 'https://www.zhihu.com/creator'

    @property
    def login_url(self) -> str:
        return 'https://www.zhihu.com/signin?next=%2Fcreator'
