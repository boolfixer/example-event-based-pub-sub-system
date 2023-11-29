from PyQt6.QtWidgets import QMainWindow, QWidget

from src.layout.main_layout import MainLayout
from src.service.command_manager import CommandManager
from src.service.comport_adapter import ComportAdapter


class MainWindow(QMainWindow):
    __comport_adapter: ComportAdapter = ComportAdapter()

    def __init__(self):
        super().__init__()

        widget = QWidget()
        widget.setLayout(MainLayout())

        self.setCentralWidget(widget)

        self.destroyed.connect(lambda: self.__comport_adapter.close())

        CommandManager()
