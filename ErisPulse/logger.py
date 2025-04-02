import logging
import inspect
from rich.logging import RichHandler
from . import sdk
from .envManager import env

_logger = logging.getLogger("RyhBot")
_log_level = env.get("LOG_LEVEL", "DEBUG")
if _log_level is None:
    _log_level = logging.DEBUG
_logger.setLevel(_log_level)

if not _logger.handlers:
    # 自定义时间格式
    console_handler = RichHandler(
        show_time=True,                         # 显示时间
        show_level=True,                        # 显示日志级别
        show_path=False,                        # 不显示调用路径
        markup=True,                            # 支持 Markdown
        log_time_format="[%Y-%m-%d %H:%M:%S]",  # 自定义时间格式
        rich_tracebacks=True,                   # 支持更美观的异常堆栈
    )
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(console_handler)


def _get_caller():
    frame = inspect.currentframe().f_back.f_back
    module = inspect.getmodule(frame)
    module_name = module.__name__
    if module_name == "__main__":
        module_name = "Main"
    if module_name.endswith(".Core"):
        module_name = module_name[:-5]
    return module_name


def debug(msg, *args, **kwargs):
    caller_module = _get_caller()
    _logger.debug(f"[{caller_module}] {msg}", *args, **kwargs)


def info(msg, *args, **kwargs):
    caller_module = _get_caller()
    _logger.info(f"[{caller_module}] {msg}", *args, **kwargs)


def warning(msg, *args, **kwargs):
    caller_module = _get_caller()
    _logger.warning(f"[{caller_module}] {msg}", *args, **kwargs)


def error(msg, *args, **kwargs):
    caller_module = _get_caller()
    _logger.error(f"[{caller_module}] {msg}", *args, **kwargs)


def critical(msg, *args, **kwargs):
    caller_module = _get_caller()
    _logger.critical(f"[{caller_module}] {msg}", *args, **kwargs)