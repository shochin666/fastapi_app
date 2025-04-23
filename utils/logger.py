import logging
import sys
from enum import Enum


# Logger
class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def setup_logger(log_level: LogLevel = LogLevel.DEBUG, log_file=None):
    """
    ロガーの初期設定を行う関数

    Args:
        log_level: ログレベル (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
        log_file: ログを出力するファイルパス（Noneの場合はコンソールのみに出力）

    Returns:
        設定されたロガーオブジェクト
    """
    # ロガーの取得
    logger = logging.getLogger("memo_app_log")
    # ログレベルの設定
    logger.setLevel(log_level)

    # フォーマットの設定
    formatter = logging.Formatter("%(asctime)s: [%(levelname)s] \n %(message)s")

    # コンソールへの出力ハンドラ
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ファイルへの出力ハンドラ（指定されている場合）
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger():
    return setup_logger(log_level=logging.DEBUG, log_file="app.log")
