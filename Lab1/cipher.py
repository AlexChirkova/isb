alph = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

with open("message.txt", 'r', encoding="utf8") as file:
    message = file.read()


def cipher_atbash(text: str, alph: str) -> str:
    '''
    Text encryption with atbash cipher.
    :param text: original text
    :param alph: original alphabet
    :return: encoded text
    '''
    encoded_text = ""
    for let in text:
        i = alph.index(let)
        encoded_text += alph[-i-1]
    return encoded_text


encoded_message = cipher_atbash(message, alph)

with open("encoded_message.txt", "w", encoding="utf8") as output_file:
    output_file.write(encoded_message)
