# このプログラムでは、スケジュールに合わせて、様々なバッチを擬似的に実行させる
# 前提として、バッチは、実行時に自分の名前と実行時間をログファイルに出力する
# また、成功か失敗かも記述する
_NUM_BEHAVIOR = 5

def _switch_main_behavior(current_num: int):
    _work_num = current_num % _NUM_BEHAVIOR 
    match _work_num:
        case 1:
            print("do batch job 1")
        case 2:
            print("do batch job 2")
        case 3:
            print("do batch job 3")
        case _:
            print("no batch job")

def _main_loop(loop_num: int, current_num: int):
    print(f"loop_num: {loop_num}, current_num: {current_num}")
    if current_num < loop_num:
        _main_loop(loop_num, current_num + 1)
    else:
        return

def main():
    print("execute : sample simple batch")

if __name__ == "__main__":
    main()