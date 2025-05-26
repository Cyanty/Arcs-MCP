import os
from config.tag_collection import *

"""发布文章自定义参数配置"""

# 博客园
CNBLOGS_MT_KEYWORDS = os.getenv("CNBLOGS_MT_KEYWORDS")

# CSDN
CSDN_LOC_TAG = os.getenv("CSDN_LOC_TAG")

# 稀土掘金
JUEJIN_CATEGORY_ID = category_id[os.getenv("JUEJIN_CATEGORY_ID")]
JUEJIN_TAG_IDS = tag_ids[os.getenv("JUEJIN_TAG_IDS")]

# 微信公众号
WECHAT_MARKDOWN2HTML = os.getenv("WECHAT_MARKDOWN2HTML")
WECHAT_AUTHOR = os.getenv("WECHAT_AUTHOR")

# 知乎
ZHIHU_ARIA_LABEL = os.getenv("ZHIHU_ARIA_LABEL")
ZHIHU_MARKDOWN2HTML = WECHAT_MARKDOWN2HTML





