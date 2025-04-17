import threading
import pyperclip
from typing import Callable, Optional, Any

# 全局锁
_clipboard_lock = threading.Lock()


def pyperclip_copy(text: str, post_action: Optional[Callable[[], None]] = None):
    with _clipboard_lock:
        pyperclip.copy(text)  # 剪贴板写入
        if post_action is not None:
            post_action()


def pyperclip_paste(post_action: Optional[Callable[[], Any]] = None) -> str:
    with _clipboard_lock:
        if post_action is not None:
            post_action()
        content = pyperclip.paste()  # 剪贴板读取
        return content

