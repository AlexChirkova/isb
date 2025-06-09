import json


class FileHandler:
    @staticmethod
    def save_to_json(data, filename):
        """
        Save data to a file
        :param data: data to write into the file as bytes
        :param filename: the path to the file to save the data
        :return: None
        """
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def load_from_json(filename):
        """
        Load a data from JSON-file.
        :param filename: path to the JSON-file
        :return: content of the JSON-file
        """
        try:
            with open(filename, "r") as f:
                return json.load(f)

        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def load_from_txt(filename):
        """
        Load a text file as bytes.
        :param filename: path to the text file
        :return: content of text file as bytes
        """
        try:
            with open(filename, "rb") as file:
                return file.read()
        except Exception as e:
            print(f"Error: {e}")
            return b""

    @staticmethod
    def save_to_txt(data, filename):
        """
        Save bytes to a file
        :param data: data to write into the file as bytes
        :param filename: the path to the file to save the data
        :return: None
        """
        try:
            with open(filename, "wb") as file:
                file.write(data.encode())
        except Exception as e:
            print(f"Error: {e}")
