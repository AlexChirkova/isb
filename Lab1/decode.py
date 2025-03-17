def create_alphabet(text: str) -> str:
    '''
    Obtaining the cryptographic alphabet of an encrypted message.
    :param text: encrypted message
    :return: cryptographic alphabet
    '''
    alph = ""
    for i in text:
        if not (i in alph):
            alph += i
    return alph


def my_sort(e):
    return e['rate']


def find_rates(text: str, alph: str) -> list:
    '''
    Getting the frequency of occurrence of characters.
    :param text: encrypted message
    :param alph: cryptographic alphabet
    :return: frequency of occurrence of characters
    '''
    all_count = len(text)
    rate = list()
    for i in alph:
        count = 0
        for j in text:
            if i == j:
                count += 1
        rate.append({'symb': i, 'rate': count/all_count})
    rate.sort(reverse=True, key=my_sort)
    return rate


def replace_letter(text: str, code_let: str, ok_let: str) -> str:
    '''
    Replacing an encoded letter with a true one.
    :param text: encrypted message
    :param code_let: the encoded letter
    :param ok_let: the decoded letter
    :return:
    '''
    text = text.replace(ok_let, '*')
    text = text.replace(code_let, ok_let)
    text = text.replace('*', code_let)
    return text


with open("text.txt", "r", encoding="utf8") as file:
    code_text = file.read()


code_alph = create_alphabet(code_text)
code_rates = find_rates(code_text, code_alph)


with open("code_alph2.txt", "a", encoding="utf16") as code_file:
    for i in code_rates:
        print(str(i), file=code_file)
       # file.write(str(i))


code_text = code_text.replace('М', ' ')
code_text = replace_letter(code_text, '>', 'И')
code_text = replace_letter(code_text, 'У', 'Л')
code_text = replace_letter(code_text, 'Х', 'Н')
code_text = replace_letter(code_text, '4', 'А')
code_text = replace_letter(code_text, 'c', 'Д')
code_text = replace_letter(code_text, 'О', 'Е')
code_text = replace_letter(code_text, '4', 'Ь')
code_text = replace_letter(code_text, 'О', 'С')
code_text = replace_letter(code_text, 'b', 'Г')
code_text = replace_letter(code_text, '1', 'О')
code_text = replace_letter(code_text, 'У', 'Я')
code_text = replace_letter(code_text, 'Ы', 'Ш')
code_text = replace_letter(code_text, '7', 'Й')
code_text = replace_letter(code_text, 'r', 'Т')
code_text = replace_letter(code_text, '8', 'К')
code_text = replace_letter(code_text, '8', 'Ю')
code_text = replace_letter(code_text, 't', 'У')
code_text = replace_letter(code_text, '4', 'Щ')
code_text = replace_letter(code_text, 'a', 'В')
code_text = replace_letter(code_text, 'c', 'Р')
code_text = replace_letter(code_text, '<', 'Ч')
code_text = replace_letter(code_text, 'Ф', 'М')
code_text = replace_letter(code_text, 'c', 'З')
code_text = replace_letter(code_text, '5', 'Б')
code_text = replace_letter(code_text, '2', 'П')
code_text = replace_letter(code_text, '7', 'Х')
code_text = replace_letter(code_text, '2', 'Ж')
code_text = replace_letter(code_text, 'С', 'Ы')
code_text = replace_letter(code_text, '5', 'Э')
code_text = replace_letter(code_text, '<', 'Ц')
code_text = replace_letter(code_text, '>', 'Ф')
code_text = replace_letter(code_text, 'Ы', 'С')


with open("decoded text.txt", "w", encoding="utf16") as file:
    file.write(code_text)
