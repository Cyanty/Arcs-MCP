from dataclasses import dataclass
from typing import Annotated, Dict, Any
from DrissionPage._functions.by import By
from base import AbstractClient
from utils.field_metadata_util import Description, ExampleValue


@dataclass
class WeChatClient(AbstractClient):
    """
    微信公众号开发者API文档：https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Access_Overview.html
    """
    _access_token: Annotated[
        str,
        Description("wechat access token（默认每次请求时获取）"),
        ExampleValue("Ad4fgK1ef6c20dff4b")
    ] = None

    _pre_json_data: Annotated[
        Dict[str, Any],
        Description("wechat 发布草稿API请求json data格式")
    ] = None

    _json_data: Annotated[
        Dict[str, Any],
        Description("wechat 发布文章API请求json data格式（25年7月后即将作废）")
    ] = None

    _mp_json_data: Annotated[
        Dict[str, Any],
        Description("wechat 群发文章API请求json data格式（需开启微信认证）")
    ] = None

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value: str):
        self._access_token = value

    @property
    def uploadimg_url(self):
        return "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=" + self._access_token

    @property
    def pre_publish_url(self):
        return "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=" + self._access_token

    @property
    def publish_url(self):
        return "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=" + self._access_token

    @property
    def mp_publish_url(self):
        return "https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=" + self._access_token

    @property
    def cookies(self):
        return {}

    @property
    def headers(self):
        return {'Content-Type': 'application/json'}

    @property
    def pre_json_data(self):
        return self._pre_json_data

    @pre_json_data.setter
    def pre_json_data(self, value):
        self._pre_json_data = {
            "articles": [
                {
                    "title": value["TITLE"],  # 标题
                    "author": value["AUTHOR"],  # 作者
                    "digest": value["DIGEST"],  # 图文消息的摘要，仅有单图文消息才有摘要，多图文此处为空。如果本字段为没有填写，则默认抓取正文前54个字。
                    "content": value["CONTENT"],  # 图文消息的具体内容，支持HTML标签，必须少于2万字符，小于1M，且此处会去除JS,涉及图片url必须来源 "上传图文消息内的图片获取URL"接口获取。外部图片url将被过滤。
                    "content_source_url": value["CONTENT_SOURCE_URL"],  # 图文消息的原文地址，即点击“阅读原文”后的URL
                    "thumb_media_id": value["THUMB_MEDIA_ID"],  # 图文消息的封面图片素材id（必须是永久MediaID）
                    "need_open_comment": 1,  # Uint32 是否打开评论，0不打开(默认)，1打开
                    "only_fans_can_comment": 0,  # Uint32 是否粉丝才可评论，0所有人可评论(默认)，1粉丝才可评论
                    "pic_crop_235_1": value["X1_Y1_X2_Y2"],
                    "pic_crop_1_1": value["X1_Y1_X2_Y2"]
                }
                # 若新增的是多图文素材，则此处应还有几段articles结构
            ]
        }

    @property
    def json_data(self):
        return self._json_data

    @json_data.setter
    def json_data(self, value):
        self._json_data = {
            "media_id": value
        }

    @property
    def mp_json_data(self):
        return self._mp_json_data

    @mp_json_data.setter
    def mp_json_data(self, value):
        self._mp_json_data = {  # 群发接口需开启微信认证（企业认证）
            "filter": {
                "is_to_all": True,  # 用于设定是否向全部用户发送，值为 true 或 false，选择 true 该消息群发给所有用户，选择 false 可根据 tag_id 发送给指定群组的用户
                "tag_id": 2  # 群发到的标签的 tag_id，参见用户管理中用户分组接口，若 is_to_all 值为true，则 tag_id 字段无效
            },
            "mpnews": {  # 用于设定即将发送的图文消息
                "media_id": value  # 用于群发的消息的 media_id
            },
            "msgtype": "mpnews",  # 群发的消息类型，图文消息为 mpnews，文本消息为 text，语音为 voice，音乐为 music，图片为 image，视频为 video，卡券为 wxcard
            "send_ignore_reprint": 1  # 图文消息被判定为转载时，是否继续群发。 1为继续群发（转载），0为停止群发。 该参数默认为0
        }

    # md2html格式转换页面元素
    @property
    def loc_code_mirror_scroll_editor(self):
        return By.XPATH, '//div[@class="CodeMirror-scroll"]'

    @property
    def loc_nice_sidebar_wechat_copy(self):
        return By.XPATH, '//*[@id="nice-sidebar-wechat"]'
