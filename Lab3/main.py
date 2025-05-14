import argparse

import constants as const

from camellia import *
from read_write import *
from rsa import *


def generate_keys() -> None:
    try:
        asymmetric_keys = RSA.generate_rsa_keys()
        RSA.serialize_private_key(asymmetric_keys[0], const.PATH_TO_PRIVATE_KEY)
        RSA.serialize_public_key(asymmetric_keys[1], const.PATH_TO_PUBLIC_KEY)
        print("Asymmetric keys were generated end wrote in file successfully.")
        size = int(input("Enter a key length of 16, 24, or 32 bytes: "))
        symmetric_key = Camellia.generate_camellia_key(size)
        FileWorker.write_txt_file(
            RSA.encrypt_symmetric_key(symmetric_key, asymmetric_keys[1]),
            const.PATH_TO_SYM_KEY,
        )
        print("Symmetric key was generated end wrote in file successfully.")

    except Exception as e:
        print(f"Error: {e}")


def encrypt_text() -> None:
    try:
        if not (
            FileWorker.read_txt_file(const.PATH_TO_SYM_KEY)
            and FileWorker.read_txt_file(const.PATH_TO_PRIVATE_KEY)
            and FileWorker.read_txt_file(const.PATH_TO_PUBLIC_KEY)
        ):
            print("You have to generate keys at first.")
            return

        symmetric_key = RSA.decrypt_symmetric_key(
            FileWorker.read_txt_file(const.PATH_TO_SYM_KEY),
            RSA.get_private_key(const.PATH_TO_PRIVATE_KEY),
        )
        plaintext = FileWorker.read_txt_file(const.PATH_TO_PLAINTEXT)
        ciphertext = Camellia.camellia_encrypt(symmetric_key, plaintext)
        FileWorker.write_txt_file(ciphertext, const.PATH_TO_CIPHERTEXT)
        print("Text was encrypted and wrote to the file.")

    except Exception as e:
        print(f"Error: {e}")


def decrypt_text() -> None:
    try:
        if not (
            FileWorker.read_txt_file(const.PATH_TO_SYM_KEY)
            and FileWorker.read_txt_file(const.PATH_TO_PRIVATE_KEY)
            and FileWorker.read_txt_file(const.PATH_TO_PUBLIC_KEY)
        ):
            print("You must have keys to decrypt text.")
            return

        symmetric_key = RSA.decrypt_symmetric_key(
            FileWorker.read_txt_file(const.PATH_TO_SYM_KEY),
            RSA.get_private_key(const.PATH_TO_PRIVATE_KEY),
        )
        ciphertext = FileWorker.read_txt_file(const.PATH_TO_CIPHERTEXT)
        encrypted_text = Camellia.camellia_decrypt(symmetric_key, ciphertext)
        FileWorker.write_txt_file(encrypted_text, const.PATH_TO_ENCRYPTED_TEXT)
        print("Text was decrypted and wrote to the file.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", help="Запускает режим генерации ключей")
    group.add_argument("-enc", "--encryption", help="Запускает режим шифрования")
    group.add_argument("-dec", "--decryption", help="Запускает режим дешифрования")

    args = parser.parse_args()

    if args.generation is not None:
        generate_keys()

    elif args.encryption is not None:
        encrypt_text()

    else:
        decrypt_text()
