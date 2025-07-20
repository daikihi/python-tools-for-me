import os

def get_file_list(directory):
    """
    指定されたディレクトリ内の全てのファイルを取得する。
    :param directory: ディレクトリのパス
    :return: ファイルのリスト
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def get_files_and_make_dict(dictionary_file_list):
    """
    指定されたディレクトリ内の辞書ファイルを取得し、辞書を作成する。
    :param dictionary_file_list: 辞書ファイルのリスト
    :return: 辞書の内容
    """
    dictionary = {}
    for file_path in dictionary_file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    key, value = line.strip().split(',')
                    dictionary[key] = value
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return dictionary


def read_and_process_files(file_list, dictionary):
    for file_path in file_list:
        text_content = read_file(file_path)
        if text_content:
            new_file_content = process_text(text_content, dictionary)
            # 出力ディレクトリがなければ作成する
            output_dir = "outputs"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            write_file_name = os.path.join(output_dir, os.path.basename(file_path))
            write_file(write_file_name, new_file_content)

def write_file(file_path, content):
    """
    指定されたパスに内容を書き込む。
    :param file_path: 書き込み先のファイルパス
    :param content: 書き込む内容
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"Written to {file_path}\n")
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"Contents of {file_path}:\n{content}\n")
            return content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

def process_text(text, dictionary):
    for key, value in dictionary.items():
        text = text.replace(key, value)
    print(f"Processed text:\n{text}\n")
    return text

def main():
    input_directory_name = "inputs"
    output_directory = "outputs"
    mapping_directory  = "dictionary"
    current_files = get_file_list(input_directory_name)
    dictionary_files = get_file_list(mapping_directory)
    dictionary = get_files_and_make_dict(dictionary_files)

    print(f"Found {len(current_files)} files in '{input_directory_name}' directory.")

    if len(current_files) == 0:
        print("No files found to process.")
        return
    print("Processing files...")
    read_and_process_files(current_files, dictionary)

if __name__ == "__main__":
    main()