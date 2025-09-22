#  このプログラムは、エラー検出器が正常に動いているか、ファイルのタイムスタンプをベースに確認する
from datetime import datetime
from typing import Final

_LAST_EXEC_FILE_NAME: Final[str] = "last_executed_data.txt"
_TIME_DIFF_THRESHOLD_SECONDS: Final[int] = 5.0 # seconds

def __load_conditions():
    print("load condition file")
    try:
        with open(_LAST_EXEC_FILE_NAME, "r", encoding="utf-8") as f:
            _last_executed_time = f.read()
            print(f"last executed time : {_last_executed_time}")
            return _last_executed_time
    except FileNotFoundError as e:
        print(f"not found last executed file : {e}")

def __check_last_exec_time(_last_exec_time_str: str):
    _last_exec_time = datetime.strptime(_last_exec_time_str, "%Y-%m-%d %H:%M:%S")
    _now = datetime.now()
    print(f"last exec time : {_last_exec_time_str}, now {_now}")
    _datetime_diff_seconds = (_now - _last_exec_time).total_seconds()
    print(f"diff : {_datetime_diff_seconds}")
    if _datetime_diff_seconds > _TIME_DIFF_THRESHOLD_SECONDS:
        raise Exception(f"error detector seems not working. last exec time is too old. diff seconds : {_datetime_diff_seconds}")

def __write_current_time_to_file():
    _now = datetime.now()
    try:
        with open(_LAST_EXEC_FILE_NAME, "w", encoding="utf-8") as f:
            f.write(_now.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print(f"error in write current time to file : {e}")

def main():
    try:
        print("ERROR DETECTION - start")
        _last_exec_time = __load_conditions()
        __check_last_exec_time(_last_exec_time)
    except Exception as e:
        print(f"error detected : {e}")
    finally:
        __write_current_time_to_file()

if __name__ == "__main__":
    main()