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
    if text is None or key is None:
        return "There is no text or key!"
    decoded_text = ""
    for let in text:
        decoded_text += key[let]
    return decoded_text


def get_frequency_analysis(path_to_text: str, path_to_save: str) \
        -> dict[str:float]:
    '''
    Calculation of the frequency of occurrence of characters in the text.
    :param path_to_text: path to the text to analysis
    :param path_to_save: path to the file to save frequency analysis
    :return: dictionary of frequency
    '''
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
    with open(path_to_save, 'w', encoding='utf-8') as file:
        json.dump(frequency, file, ensure_ascii=False, indent=4)
    return


if __name__ == '__main__':
    get_frequency_analysis(const.INPUT_FILE_2, const.FREQUENCY_ANALYSIS)
    key = get_key(const.KEY)
    encoded_text = rw.read_txt_file(const.INPUT_FILE_2)
    decoded_text = decode_by_key(encoded_text, key)
    rw.write_txt_file(decoded_text, const.OUTPUT_FILE_2)
