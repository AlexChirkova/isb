import constants as const
import read_write as rw


def cipher_atbash(text: str, alph: str) -> str:
    '''
    Text encryption with atbash cipher.
    :param text: original text
    :param alph: original alphabet
    :return: encoded text
    '''
    if text is None or alph is None:
        return "There is no text or alphabet!"
    encoded_text = ""
    for let in text:
        i = alph.index(let)
        encoded_text += alph[-i-1]
    return encoded_text


if __name__ == '__main__':
    message = rw.read_txt_file(const.INPUT_FILE_1)
    encoded_message = cipher_atbash(message, const.ALPHABET)
    rw.write_txt_file(encoded_message, const.OUTPUT_FILE_1)
