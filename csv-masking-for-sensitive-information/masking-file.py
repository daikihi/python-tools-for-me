# 入力パラメータから、入力ファイル名、出力ファイル名とマスキングしちゃいたいカラム数をCSV で受け取る
# args は、配列でくるものとする
import csv
import sys


def _get_arguments(args): 
    if len(args) != 4:
        raise ValueError("引数は３つでお願いします。入力ファイル名 出力ファイル名 マスキングするカラム数をCSVで")
    
    input_file_name = args[1]
    output_file_name = args[2]
    if input_file_name == output_file_name:
        raise ValueError("入力と出力のファイル名が同じです。本当に良いの？オリジナルファイルが消えちゃうよ？")
    masking_params_str = args[3]
    masking_params = list(map(lambda culumn: int(culumn) ,masking_params_str.split(",")))
    result = {"input_file_name": input_file_name, "output_file_name": output_file_name, "masking_params": masking_params }
    return result

# CSV fail をファイルシステムから取得する
def _read_csv_file_from_file_system(read_file_name):
    l = []
    with open(read_file_name) as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    return l

# 対象のカラムをマスキングする
def _masking_data(content_data, masking_column):
    masked_data = []
    for data in content_data:
        new_line = _mask_line(data, masking_column)
        masked_data.append(new_line)

    return masked_data

def _mask_line(line, masking_column):
    new_line = []
    i = 0
    for l in line:
        if i in masking_column:
            new_line.append("SAMPLE")
        else:
            new_line.append(l)
        i = i + 1
    i = 0
    return new_line

# 出力ファイルをファイルシステムに放出
def write_masked_data_into_file_system(masked_content_data, write_file):
    with open(write_file, mode = 'w', newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(masked_content_data)


# main method
def main():
    try:
        args = sys.argv
        _argument_dicts = _get_arguments(args)
        print(args)
        print(_argument_dicts)
        _content_data_array = _read_csv_file_from_file_system(_argument_dicts["input_file_name"])
        # print(_content_data_array)
        _masked_data = _masking_data(_content_data_array, _argument_dicts["masking_params"])
        # print(f"{_masked_data}\n")
        write_masked_data_into_file_system(_masked_data, _argument_dicts["output_file_name"])
    except ValueError as e:
        print(f"パラメータ違反：{e}")
        exit


if __name__ == "__main__":
    main()