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


key = get_key(const.KEY)
encoded_text = rw.read_txt_file(const.INPUT_FILE_2)
decoded_text = decode_by_key(encoded_text, key)
rw.write_txt_file(decoded_text, const.OUTPUT_FILE_2)
