import argparse
import sys
from PyQt5.QtWidgets import QApplication

from gui import CardRecoveryApp

from file_handler import FileHandler


def parse_args():
    parser = argparse.ArgumentParser(description="Bank Card Number Recovery Tool")
    parser.add_argument(
        "--mode", choices=["find", "check", "measure"], help="Operation mode"
    )
    parser.add_argument("--input", help="Input JSON file with parameters")

    return parser.parse_args()


def load_input_file(filename):

    try:
        data = FileHandler.load_from_json(filename)

        if "operation" not in data:
            raise ValueError("Input JSON must contain 'operation' field")

        if data["operation"] == "find_card_number":
            if not all(field in data for field in ["hash", "bins", "last4"]):
                raise ValueError(
                    "Find operation requires 'hash', 'bins' and 'last4' fields"
                )

            if "bin" in data and "bins" not in data:
                data["bins"] = [data["bin"]]

            for bin_str in data["bins"]:
                if len(bin_str) != 6 or not bin_str.isdigit():
                    raise ValueError(f"Invalid BIN: {bin_str}. Must be 6 digits")

            if len(data["last4"]) != 4 or not data["last4"].isdigit():
                raise ValueError("Last 4 digits must be 4 digits")

        return data

    except Exception as e:
        print(f"Error: {e}")


def main():
    args = parse_args()
    app = QApplication(sys.argv)

    input_data = None
    if args.input:
        try:
            input_data = load_input_file(args.input)
        except ValueError as e:
            print(f"Error loading input file: {e}")
            sys.exit(1)

    window = CardRecoveryApp(args, input_data)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
