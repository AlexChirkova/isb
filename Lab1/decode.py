import json


import constants as const
import read_write as rw


def get_key(key_path: str) -> dict[str:str]:
    '''
    Getting the json encryption key.
    :param key_path: path to the file with the encryption key
    :return: keys dictionary
    '''
    try:
        with open(key_path, "r", encoding="utf-8") as key:
            return json.load(key)

    except Exception as e:
        print(f"Error: {e}")


def decode_by_key(text: str, key: dict[str:str]) -> str:
    '''
    Decoding the encoded text.
    :param text: encoded text
    :param key: keys dictionary
    :return: decoded text
    '''
    try:
        if text is None or key is None:
            return "There is no text or key!"
        decoded_text = ""
        for let in text:
            decoded_text += key[let]
        return decoded_text

    except Exception as e:
        print(f"Error: {e}")


def write_json_file(data: dict, file_path: str, ) -> None:
    '''
    Writing dict to a json-file
    :param data: data to write into the file
    :param file_path: path to the file to save the data
    :return: None
    '''
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error: {e}")


def get_frequency_analysis(path_to_text: str) -> dict[str:float]:
    '''
    Calculation of the frequency of occurrence of characters in the text.
    :param path_to_text: path to the text to analysis
    :return: dictionary of frequency
    '''
    try:
        text = rw.read_txt_file(path_to_text)
        alph = ""
        for i in text:
            if not (i in alph):
                alph += i

        all_count = len(text)
        frequency = list()
        for i in alph:
            count = 0
            for j in text:
                if i == j:
                    count += 1
            frequency.append([i, count/all_count])

        frequency.sort(reverse=True, key=lambda item: item[1])
        frequency = dict(frequency)

        return frequency

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    freq = get_frequency_analysis(const.INPUT_FILE_2)
    write_json_file(const.FREQUENCY_ANALYSIS, freq)
    key = get_key(const.KEY)
    encoded_text = rw.read_txt_file(const.INPUT_FILE_2)
    decoded_text = decode_by_key(encoded_text, key)
    rw.write_txt_file(decoded_text, const.OUTPUT_FILE_2)
