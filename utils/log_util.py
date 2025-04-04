import logging


def init_loging_config():
    level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(name)s [%(processName)s] %(module)s %(levelname)s %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    _logger = logging.getLogger("=>")
    _logger.setLevel(level)
    return _logger


logger = init_loging_config()

