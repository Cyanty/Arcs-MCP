# -*- coding: utf-8 -*-
import asyncio
from base import AbstractCrawler
from extension.crawler_factory import get_crawler_setup_source, create_crawler_instance
from functools import wraps
from utils import logger, image_request


def config_feature(model_name: str):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if get_crawler_setup_source().get(model_name, False):
                return await func(*args, **kwargs)
            else:
                return {'result': f'发布来源 < {model_name.upper()} > 未启用'}
        return async_wrapper
    return decorator


async def crawlers_start(file_name: str, md_content: str):
    file_name = file_name.rsplit('.', 1)[0]
    logger.info(f"----- Enable publishing the article -> {file_name} -----")
    image_results = await image_request(md_content)
    tasks = []
    for model_name in get_crawler_setup_source().keys():
        crawler_object = create_crawler_instance(model_name)

        @config_feature(model_name)
        async def start(crawler_class: AbstractCrawler):
            await crawler_class.init_config(file_name=file_name,
                                            md_content=md_content,
                                            image_results=image_results)
            return await crawler_class.run()

        tasks.append(start(crawler_object))

    results = await asyncio.gather(*tasks)
    result_dict = {source: result for source, result in zip(get_crawler_setup_source(), results)}

    logger.info("----- The article publishing process is complete! -----")
    return result_dict


