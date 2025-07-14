import os
from typing import Optional, Type, Dict
from base import AbstractCrawler
from utils import load_single_subclass_from_source, logger, singleton


@singleton
class CrawlerFactory:
    def __init__(self) -> None:
        self.crawler_module_extensions: Dict[str, AbstractCrawler] = {}
        self.crawler_setup_source: Dict[str, bool] = {}
        self.get_crawlers()

    def get_crawlers(self):
        current_path = os.path.abspath(__file__)
        crawler_module_path = os.path.dirname(current_path)

        crawler_module_dir_paths = [
            os.path.join(crawler_module_path, crawler_module_dir)
            for crawler_module_dir in os.listdir(crawler_module_path)
            if not crawler_module_dir.startswith("__") and os.path.isdir(os.path.join(crawler_module_path, crawler_module_dir))
        ]

        for crawler_module_dir_path in crawler_module_dir_paths:
            base_module_name = "crawler"
            crawler_module_name = os.path.basename(crawler_module_dir_path)

            file_names = os.listdir(crawler_module_dir_path)
            if (base_module_name + ".py") not in file_names:
                logger.info(f"Missing {base_module_name}.py file in {crawler_module_dir_path}, Skip.")
                continue

            py_path = os.path.join(crawler_module_dir_path, base_module_name + ".py")
            crawler_module_class = load_single_subclass_from_source(
                module_name=f"extension.{crawler_module_name}.{base_module_name}",
                script_path=py_path,
                parent_type=AbstractCrawler,
            )

            if not crawler_module_class:
                logger.warning(f"Missing module Provider Class that extends moduleProvider in {py_path}, Skip.")
                continue

            self.crawler_module_extensions.update({crawler_module_name: crawler_module_class})
            self.crawler_setup_source.update({crawler_module_name: False})


def create_crawler_instance(module_name: str) -> AbstractCrawler:
    crawler_module_class: Optional[Type[AbstractCrawler]] = CrawlerFactory().crawler_module_extensions.get(module_name)
    if not crawler_module_class:
        logger.error("Warning: Publish module not defined for this source...")
    return crawler_module_class()


def get_crawler_setup_source() -> Dict[str, bool]:
    return CrawlerFactory().crawler_setup_source

def get_crawler_reset_source() -> Dict[str, bool]:
    for key in get_crawler_setup_source():
        get_crawler_setup_source()[key] = False
    return get_crawler_setup_source()
