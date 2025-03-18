def read_txt_file(file_path: str) -> str:
    '''
    Reading a text file.
    :param file_path: path to the text file
    :return: content of text file
    '''
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error: {e}")


def write_txt_file(data: str, file_path: str) -> None:
    '''
    Writing text to a file
    :param data: data to write into the file
    :param file_path: path to the file to save the data
    :return: None
    '''
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)
    except Exception as e:
        print(f"Error: {e}")
