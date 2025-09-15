from logging import getLogger, INFO
import logging 

import random

logger = getLogger(__name__)
logger.setLevel(INFO)

# ログのフォーマットを設定
logging.basicConfig(  
    level=INFO,  # ログレベルを設定
    format='%(asctime)s - %(levelname)s - %(message)s',  # 時間とログレベルを含むフォーマット
    datefmt='%Y-%m-%d %H:%M:%S'  # 日付と時間のフォーマット
)

def __sleep_for_a_miliseconds(seconds: int):
    import time
    time.sleep(seconds)

def __generate_next_interval():
    _start = 1
    _end = 1000
    return random.randint(_start, _end)

def __dummy_log_printer(msg: str):
    _log_type = random.randint(0, 2)
    if _log_type == 0:
        logger.info(f"this is info log : {msg}")
    elif _log_type == 1:
        logger.warning(f"this is warning log : {msg}")
    elif _log_type == 2:
        logger.error(f"this is error log : {msg}")

def main():
    logger.info("starting dummy log generator!")
    __number_of_logs = 20
    for i in range(__number_of_logs):
        _next_interval = __generate_next_interval()
        __dummy_log_printer(f"dummy log {i} : wait for {_next_interval} ms")
        __sleep_for_a_miliseconds(_next_interval / 1000.0) # ミリ秒を秒に変換して待機

if __name__ == "__main__":
    main()
