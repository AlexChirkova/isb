import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTabWidget,
    QFileDialog,
    QMessageBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from card_finder import CardFinder
from luhn_checker import LuhnChecker
from time_measurer import TimeMeasurer
from plotter import Plotter
from file_handler import FileHandler


class CardRecoveryApp(QMainWindow):
    def __init__(self, args=None, input_data=None):
        super().__init__()
        self.args = args
        self.input_data = input_data

        self.card_finder = CardFinder()
        self.luhn_checker = LuhnChecker()
        self.time_measurer = TimeMeasurer()
        self.plotter = Plotter()
        self.file_handler = FileHandler()

        self.init_ui()
        self.setWindowTitle("Bank Card Number Recovery Tool")
        self.setGeometry(100, 100, 800, 600)

        if self.args and self.args.input:
            self.load_input_data()

    def load_input_data(self):
        """
        Loads data from the input file into the interface
        :return: None
        """
        try:
            if self.input_data["operation"] == "find_card_number":
                self.tabs.setCurrentIndex(0)
                self.hash_input.setText(self.input_data.get("hash", ""))
                self.last4_input.setText(self.input_data.get("last4", ""))

                bins = ""
                for bin in self.input_data["bins"]:
                    bins += bin + " "
                self.bin_input.setText(bins)

            elif self.input_data.get("operation") == "check_card":
                self.tabs.setCurrentIndex(1)
                self.card_input.setText(self.input_data.get("card_number", ""))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load input data: {str(e)}")

    def init_ui(self):
        """
        Initializing the main window
        :return: None
        """
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tabs = QTabWidget()

        self.tab_find = QWidget()
        self.init_find_tab()
        self.tabs.addTab(self.tab_find, "Find Card Number")

        self.tab_check = QWidget()
        self.init_check_tab()
        self.tabs.addTab(self.tab_check, "Check Card Number")

        self.tab_measure = QWidget()
        self.init_measure_tab()
        self.tabs.addTab(self.tab_measure, "Measure Performance")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.central_widget.setLayout(layout)

    def init_find_tab(self):
        """
        Initializing the tab to search for the card number
        :return: None
        """
        layout = QVBoxLayout()

        hash_layout = QHBoxLayout()
        hash_layout.addWidget(QLabel("Card Hash:"))
        self.hash_input = QLineEdit()
        hash_layout.addWidget(self.hash_input)
        layout.addLayout(hash_layout)

        last4_layout = QHBoxLayout()
        last4_layout.addWidget(QLabel("Last 4 Digits:"))
        self.last4_input = QLineEdit()
        self.last4_input.setMaxLength(4)
        last4_layout.addWidget(self.last4_input)
        layout.addLayout(last4_layout)

        bin_layout = QHBoxLayout()
        bin_layout.addWidget(QLabel("BIN (first 6 digits):"))
        self.bin_input = QLineEdit()
        bin_layout.addWidget(self.bin_input)
        layout.addLayout(bin_layout)

        self.find_button = QPushButton("Find Card Number")
        self.find_button.clicked.connect(self.find_card_number)
        layout.addWidget(self.find_button)

        self.find_result = QTextEdit()
        self.find_result.setReadOnly(True)
        layout.addWidget(self.find_result)

        self.save_button = QPushButton("Save Result to txt")
        self.save_button.clicked.connect(self.save_find_result)
        layout.addWidget(self.save_button)

        self.tab_find.setLayout(layout)

    def init_check_tab(self):
        """
        Initializing the card number verification tab
        :return: None
        """
        layout = QVBoxLayout()

        card_layout = QHBoxLayout()
        card_layout.addWidget(QLabel("Path to file with card number:"))
        self.card_input = QLineEdit()
        card_layout.addWidget(self.card_input)
        layout.addLayout(card_layout)

        self.check_button = QPushButton("Check Card Number")
        self.check_button.clicked.connect(self.check_card_number)
        layout.addWidget(self.check_button)

        self.check_result = QTextEdit()
        self.check_result.setReadOnly(True)
        layout.addWidget(self.check_result)

        self.tab_check.setLayout(layout)

    def init_measure_tab(self):
        """
        Initializing the tab to find and draw the time dependence on the number of processes
        :return: None
        """
        layout = QVBoxLayout()

        hash_layout = QHBoxLayout()
        hash_layout.addWidget(QLabel("Card Hash:"))
        self.measure_hash_input = QLineEdit()
        hash_layout.addWidget(self.measure_hash_input)
        layout.addLayout(hash_layout)

        last4_layout = QHBoxLayout()
        last4_layout.addWidget(QLabel("Last 4 Digits:"))
        self.measure_last4_input = QLineEdit()
        self.measure_last4_input.setMaxLength(4)
        last4_layout.addWidget(self.measure_last4_input)
        layout.addLayout(last4_layout)

        bin_layout = QHBoxLayout()
        bin_layout.addWidget(QLabel("BIN (first 6 digits):"))
        self.measure_bin_input = QLineEdit()
        bin_layout.addWidget(self.measure_bin_input)
        layout.addLayout(bin_layout)

        self.measure_button = QPushButton("Measure Performance")
        self.measure_button.clicked.connect(self.measure_performance)
        layout.addWidget(self.measure_button)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.tab_measure.setLayout(layout)

    def find_card_number(self):
        """
        Implementing a card number search
        :return: None
        """
        try:
            card_hash = self.hash_input.text().strip()
            last4 = self.last4_input.text().strip()
            bins_text = self.bin_input.text().strip()

            if not all([card_hash, last4, bins_text]):
                raise ValueError("All fields are required")

            if len(last4) != 4 or not last4.isdigit():
                raise ValueError("Last 4 digits must be 4 digits")

            bins = [b.strip() for b in bins_text.replace(",", " ").split() if b.strip()]
            for bin_prefix in bins:
                if len(bin_prefix) != 6 or not bin_prefix.isdigit():
                    raise ValueError(f"Invalid BIN: {bin_prefix}. Must be 6 digits")

            card_number = self.card_finder.find_card_number(bins, last4, card_hash)
            self.find_result.setText(f"Found card number: {card_number}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def check_card_number(self):
        """
        Implementation of card number verification
        :return: None
        """
        try:
            path_to_card_number = self.card_input.text().strip()
            if not path_to_card_number:
                raise ValueError("Card number is required")

            is_valid = self.luhn_checker.check(path_to_card_number)
            result = "VALID" if is_valid else "INVALID"
            card_number = FileHandler.load_from_txt(path_to_card_number)
            digits = ""
            for d in str(card_number.decode()):
                if d.isdigit():
                    digits += d

            self.check_result.setText(
                f"Card number {digits} is {result} according to Luhn algorithm"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def measure_performance(self):
        """
        Implementation of finding and drawing the time dependence on the number of processes
        :return: None
        """
        try:
            card_hash = self.measure_hash_input.text().strip()
            last4 = self.measure_last4_input.text().strip()
            bins_text = self.measure_bin_input.text().strip()
            if not all([card_hash, last4, bins_text]):
                raise ValueError("All fields are required")

            if len(last4) != 4 or not last4.isdigit():
                raise ValueError("Last 4 digits must be 4 digits")

            bins = [b.strip() for b in bins_text.replace(",", " ").split() if b.strip()]
            for bin_prefix in bins:
                if len(bin_prefix) != 6 or not bin_prefix.isdigit():
                    raise ValueError(f"Invalid BIN: {bin_prefix}. Must be 6 digits")

            results = self.time_measurer.measure_performance(card_hash, bins, last4)

            self.plotter.plot_results(results, self.figure)
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_find_result(self):
        """
        Implementation of saving card number
        :return: None
        """
        try:
            result_text = self.find_result.toPlainText()
            if not result_text:
                raise ValueError("No result to save")

            filename, _ = QFileDialog.getSaveFileName(
                self, "Save Result", "", "TXT Files (*.txt)"
            )
            if filename:
                if not filename.endswith(".txt"):
                    filename += ".txt"

            self.file_handler.save_to_txt(result_text, filename)
            QMessageBox.information(self, "Success", "Result saved successfully")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
