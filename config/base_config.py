import os


# WEB环境变量配置
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", default="127.0.0.1")
WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT", default=8001))


"""
各平台账号秘钥的配置格式：

    # 博客园metablog配置
    CNBLOGS_METABLOG_CONFIG = {
        "url": "https://rpc.cnblogs.com/metaweblog/xxx",
        "appkey": "xxx",
        "usr": "xxx",
        "passwd": "xxx",
        "blogid": "xxx"
    }

    # 微信公众号
    wechat_public_account = {
        "grant_type": "client_credential",
        "appid": "xxxxx",
        "secret": "xxxxx"
    }

    # halo publish 个人令牌
    halo_publish_token = "xxxxx"
"""


# 博客园metablog配置
CNBLOGS_METABLOG_CONFIG = {
    "url": os.getenv("CNBLOGS_METABLOG_CONFIG_URL"),
    "appkey": os.getenv("CNBLOGS_METABLOG_CONFIG_APPKEY"),
    "usr": os.getenv("CNBLOGS_METABLOG_CONFIG_USR"),
    "passwd": os.getenv("CNBLOGS_METABLOG_CONFIG_PASSWD"),
    "blogid": os.getenv("CNBLOGS_METABLOG_CONFIG_BLOGID")
}

# 微信公众号
WECHAT_PUBLIC_ACCOUNT = {
    "grant_type": os.getenv("WECHAT_PUBLIC_ACCOUNT_GRANT_TYPE"),
    "appid": os.getenv("WECHAT_PUBLIC_ACCOUNT_APPID"),
    "secret": os.getenv("WECHAT_PUBLIC_ACCOUNT_SECRET")
}

# halo publish 个人令牌
HALO_PUBLISH_TOKEN = os.getenv("HALO_PUBLISH_TOKEN")

# 星火认知大模型
SPARKAI_URL = os.getenv("SPARKAI_URL")
SPARKAI_APP_ID = os.getenv("SPARKAI_APP_ID")
SPARKAI_API_SECRET = os.getenv("SPARKAI_API_SECRET")
SPARKAI_API_KEY = os.getenv("SPARKAI_API_KEY")
SPARKAI_DOMAIN = os.getenv("SPARKAI_DOMAIN")
