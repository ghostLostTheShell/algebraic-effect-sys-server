import logging
from logging.handlers import TimedRotatingFileHandler
import os
from .formatter import COLOR_FORMATTER, fmt
from typing import Optional, Set, Dict


file_handler: Optional[TimedRotatingFileHandler] = None


def init_file_handler():
    global file_handler
    log_path = "log/app.log"
    if os.path.exists(os.path.dirname(log_path)) is False:
        os.mkdir(os.path.dirname(log_path))
    file_handler = TimedRotatingFileHandler(log_path, when="D", interval=1, backupCount=7, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(fmt))
    file_handler.doRollover()  # Clear log content by triggering a rollover

ch_handler = logging.StreamHandler()
ch_handler.setFormatter(COLOR_FORMATTER)



logger = logging.getLogger("tickbutcherserver")
# logger.addHandler(file_handler)
logger.addHandler(ch_handler)
logger.setLevel(logging.INFO)

def file_logger_enable():
  if file_handler is None:
    init_file_handler()
  
  logger.addHandler(file_handler) # type: ignore

def ch_handler_disable():
    logger.removeHandler(ch_handler) # type: ignore

def file_handler_disable():
    logger.removeHandler(file_handler) # type: ignore

def set_log_level(level: int):
    logger.setLevel(level)
    if file_handler is not None:
        file_handler.setLevel(level)
    ch_handler.setLevel(level)

loggers: Set[logging.Logger] = set()

def get_all_loggers() -> Dict[str, logging.Logger]:
    """获取所有已创建的 logger"""
    all_loggers = {}
    
    # 获取根 logger
    all_loggers['root'] = logging.getLogger()
    
    # 获取所有其他 logger
    for name in logging.Logger.manager.loggerDict:
        all_loggers[name] = logging.getLogger(name)
    
    return all_loggers


def get_logger(name: str | None = None) -> logging.Logger:
    """获取指定名称的日志记录器"""
    if name is None:
        name =  'root'
    log = logging.getLogger(name)
    if log not in loggers:
        loggers.add(log)
        if file_handler is not None:
            log.addHandler(file_handler) # type: ignore
        log.addHandler(ch_handler) # type: ignore
        log.setLevel(logging.INFO)
        
    return log

def disable_logger(name: str | None = None) -> None:
    """禁用指定名称的日志记录器"""

    if name is None:
        all_loggers = get_all_loggers()
        for logger in all_loggers.values():
            logger.disabled = True

    else:
      log = logging.getLogger(name)
      log.disabled = True

__all__ = ["logger", "ch_handler", "get_logger", "get_all_loggers", "disable_logger"]