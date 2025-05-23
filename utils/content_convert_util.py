import asyncio
import re
from typing import Dict, Optional
from pypinyin import pinyin, lazy_pinyin, Style
from datetime import datetime
import uuid
from utils import request_img


def convert_to_slug(title: str) -> str:
    pinyin_list = lazy_pinyin(title)
    slug = '-'.join(pinyin_list)
    slug = re.sub(r'-+', '-', slug)
    return slug


def get_current_time() -> str:
    now = datetime.utcnow()
    return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def generate_uuid() -> str:
    return str(uuid.uuid1())  # 生成基于时间的UUID


def generate_uuid4() -> str:
    return str(uuid.uuid4())  # 生成一个随机的UUID


def github_proxy_url():
    return ['https://github.moeyy.xyz/']


async def image_request(md_content: str):
    pattern = r'!\[.*?\]\((.*?)\)'  # 正则表达式匹配图片URL, 匹配格式：![alt text](URL)
    matches = re.findall(pattern, md_content)  # 查找所有匹配的图片 URL
    tasks = [request_img("GET", image_url, timeout=10) for image_url in matches]
    results = await asyncio.gather(*tasks)
    image_results = [
        {"image_url": image_url, "image_content": image_content}
        for image_url, status_code, image_content in results
        if 200 <= status_code < 300
    ]
    return image_results


def check_dict_base_config(base_config: Dict[str, Optional[str]]):
    for key in base_config:
        value = base_config.get(key)
        if value is None or (isinstance(value, str) and len(value.strip()) == 0):
            return None
    return base_config
