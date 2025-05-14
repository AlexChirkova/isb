class FileWorker:
    @staticmethod
    def read_txt_file(file_path: str) -> bytes:
        """
        Reading a text file as bytes.
        :param file_path: path to the text file
        :return: content of text file as bytes
        """
        try:
            with open(file_path, "rb") as file:
                return file.read()
        except Exception as e:
            print(f"Error: {e}")
            return b''

    @staticmethod
    def write_txt_file(data: bytes, file_path: str) -> None:
        """
        Writing bytes to a file
        :param data: data to write into the file as bytes
        :param file_path: the path to the file to save the data
        :return: None
        """
        try:
            with open(file_path, "wb") as file:
                file.write(data)
        except Exception as e:
            print(f"Error: {e}")
