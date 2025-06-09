from file_handler import FileHandler


class LuhnChecker:
    @staticmethod
    def check(path_to_card_number):
        """
        Check if a card number is valid using Luhn algorithm
        :param path_to_card_number: file with card number for check
        :return: is the card number valid or not
        """
        try:
            card_number = FileHandler.load_from_txt(path_to_card_number)
            digits = [int(d) for d in str(card_number.decode()) if d.isdigit()]
            if len(digits) != 16:
                return False

            checksum = 0
            for i, digit in enumerate(reversed(digits)):
                if i % 2 == 1:
                    doubled = digit * 2
                    checksum += doubled if doubled < 10 else doubled - 9
                else:
                    checksum += digit

            return checksum % 10 == 0
        except Exception as e:
            print(f"Error: {e}")
            return False
