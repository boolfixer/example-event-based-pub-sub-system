import logging
import sys

from PyQt6.QtWidgets import QApplication

from src.main_window import MainWindow


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        main_window = MainWindow()
        main_window.show()

        app.exec()
    except Exception as exception:
        logging.exception(exception)
