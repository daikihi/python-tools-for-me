import os

NUMVER_OF_COMMA = 5  # CSVファイルの一行あたりのカンマ数

def is_emptry_file(file_content):
    if file_content.strip() == "":
        print("Empty file detected.")
        return True
    return False

def is_valid_csv_file(file_content):
    lines = file_content.strip().split('\n')
    for line in lines:
        if len(line.split(',')) != NUMVER_OF_COMMA:
            print(f"Invalid CSV format in line: {line}")
            return False
    return True

def is_valid_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # ここでは単純に空でないことを確認する
            empty_check = is_emptry_file(content)
            if file_path.endswith('.csv'):
                 csv_valid = is_valid_csv_file(content)
            else:
                csv_valid = True
            return empty_check and csv_valid
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False



# 正しくなかったファイルをリストで返す。理由要る？
def is_valid_files(file_list):
    invalid_files = []
    for file_path in file_list:
        if not os.path.isfile(file_path):
            print(f"Invalid file: {file_path}")
            invalid_files.append(file_path)
            continue
        else:
            if is_valid_file(file_path):
                print(f"Valid file: {file_path}")
            else:
                print(f"Invalid content in file: {file_path}")
                invalid_files.append(file_path)
    return invalid_files

# 指定されたディレクトリに入っているファイルのリストを返す
def read_file_list(directory):
    """
    指定されたディレクトリ内のファイルをリストアップする。
    :param directory: 対象ディレクトリ
    :return: ファイルのリスト
    """
    file_list = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_list.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")
    return file_list


# このプログラムでは、指定されたディレクトリに入っているファイルが、正しいかどうかを確認する
# 何をもって正しいとするかは、 is_valid_files メソッドに依存する。厳密には is_valid_files 内で利用されているメソッド群
def main():
    directory = "inputs"  # 入力ディレクトリ
    target_files = read_file_list(directory)
    print("Target files:", target_files)
    invalid_files = is_valid_files(target_files)
    print("Invalid files:", invalid_files)

if __name__ == "__main__":
    main()