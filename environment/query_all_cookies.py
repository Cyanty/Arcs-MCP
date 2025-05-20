# -*- coding: utf-8 -*-
import platform
from functools import wraps
import psutil
from typing import Dict, List, Tuple
from DrissionPage._base.chromium import Chromium
from concurrent.futures import ThreadPoolExecutor
from environment.dp_obj import SingletonDrissionPage
from utils import logger


def dp_instance(user_path_on_off=False, headless_on_off=False) -> SingletonDrissionPage:
    return SingletonDrissionPage(user_path_on_off=user_path_on_off, headless_on_off=headless_on_off)


def browser_process_names(browser: str) -> Tuple[List[str], str]:
    """ 各平台浏览器及进程名统计:
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
    process_names = {
            "chrome": {
                "Windows": ["chrome.exe"],
                "Linux": ["chrome", "google-chrome", "chromium"],
                "Darwin": ["Google Chrome"]
            },
            "firefox": {
                "Windows": ["firefox.exe"],
                "Linux": ["firefox"],
                "Darwin": ["firefox"]
            },
            "msedge": {
                "Windows": ["msedge.exe"],
                "Linux": ["microsoft-edge", "msedge"],
                "Darwin": ["Microsoft Edge"]
            },
            "opera": {
                "Windows": ["opera.exe"],
                "Linux": ["opera"],
                "Darwin": ["Opera"]
            },
            "safari": {
                "Windows": [],
                "Linux": [],
                "Darwin": ["Safari"]
            },
            "brave": {
                "Windows": ["brave.exe"],
                "Linux": ["brave-browser"],
                "Darwin": ["Brave Browser"]
            },
            "chromium-browser": {
                "Windows": ["chromium.exe"],
                "Linux": ["chromium-browser", "chromium"],
                "Darwin": ["Chromium"]
            }
        }
    system = platform.system()
    return process_names.get(browser, {}).get(system, []), system


def is_browser_open(browser_name: str):
    names, _ = browser_process_names(browser_name)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if any(target_name.lower() in proc.name().lower() for target_name in names):
                logger.info(f"✅ Browser is open: PID={proc.pid} NAME={proc.name()}")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    logger.info("❌ Browser is not open.")
    return False


def check_browser_remote_debugging(browser_name: str):
    names, _ = browser_process_names(browser_name)
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN' and conn.laddr.port == 9223:
            pid = conn.pid
            if pid:
                try:
                    proc = psutil.Process(pid)
                    if any(target_name.lower() in proc.name().lower() for target_name in names):
                        logger.info(f"✅ Browser remote debug mode is enabled: PID={pid} NAME={proc.name()}")
                        return True
                except psutil.NoSuchProcess:
                    pass
    logger.info("❌ Browser remote debug mode is not enabled (port 9223 is not used by the browser).")
    return False


def proc_process_browsers(browsers: List, killed=False):
    for browser in browsers:
        names, system = browser_process_names(browser)
        if not names:
            logger.warning(f"{browser} is skipped, the browser process name for the {system} system is not configured.")
            continue

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.name()
                if system == "Windows":
                    proc_name = proc_name.lower()
                    target_names = [n.lower() for n in names]
                else:
                    target_names = names

                if proc_name in target_names:
                    logger.info(f"Terminating process: PID={proc.pid} NAME={proc_name}")
                    if not killed:
                        proc.terminate()  # 先尝试正常终止
                    else:
                        proc.kill()
                    proc.wait(timeout=2)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue


def _kill_browsers(browsers: List):
    """ 使用 psutil 终止指定浏览器的所有进程（跨平台实现）"""
    try:
        [proc_process_browsers(browsers=browsers, killed=killed)
         for killed in [False, True]]
        logger.info("The browser process is terminated.")
    except Exception as e:
        logger.error(f"Failed to terminate the browser process. Procedure: {str(e)}", exc_info=True)


def _close_all_browsers(first_startup=False):
    browsers = ["chrome", ]  # 默认谷歌浏览器
    is_killed = False
    for browser in browsers:
        if is_browser_open(browser) and not check_browser_remote_debugging(browser):
            is_killed = True
            break

    if is_killed:
        if first_startup:
            confirm = input("警告：这将强制关闭浏览器，未保存的数据会丢失！\n确认继续？(y/n): ").lower()
            if confirm == 'y':
                _kill_browsers(browsers)
            else:
                logger.info("关闭浏览器操作已取消！")
        else:
            _kill_browsers(browsers)


def with_browser_lifecycle(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        get_sync_browser_init()
        try:
            return await func(*args, **kwargs)
        finally:
            get_sync_browser_destroy()
    return wrapper


def check_browser_process_states() -> bool:
    states = dp_instance().get_current_browser_states()
    return True if states is None else not states.is_alive


def get_sync_browser_init():
    return check_browser_process_states() and dp_instance().init_browser_process()


def get_sync_browser_destroy():
    dp_instance().destroy_browser_process()


def get_browser_by_reconnect():
    dp_instance().destroy_browser_process().init_browser_process()


def get_chromium_browser_signal() -> Tuple[Chromium, ThreadPoolExecutor]:
    return dp_instance().get_chromium_browser_signal()


def get_cookies_from_chromium(cookies_key: str) -> Dict[str, str]:
    dp_instance().refresh_cookies()
    return dp_instance().get_cookies_from_chromium(cookies_key)
