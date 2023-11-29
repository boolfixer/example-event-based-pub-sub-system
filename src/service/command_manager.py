from PyQt6.QtCore import QThreadPool

from src.enum.event import Event
from src.service.command_listener_worker import CommandListenerWorker
from src.service.comport_adapter import ComportAdapter
from src.service.event_emitter import EventEmitter
from src.service.sync_worker import SyncWorker
from src.utils.abstract_singleton import AbstractSingleton


class CommandManager(AbstractSingleton):
    __comport_adapter: ComportAdapter = ComportAdapter()
    __event_emitter: EventEmitter = EventEmitter()
    __thread_pool: QThreadPool = QThreadPool()

    def __init__(self):
        super().__init__()

        self.__event_emitter.subscribe(Event.COMMAND_BUTTON_CLICKED, self.__command_button_clicked)
        self.__thread_pool.start(CommandListenerWorker())
        self.__thread_pool.start(SyncWorker())

    def __command_button_clicked(self, command: str):
        command_name = command
        self.__comport_adapter.write(command_name)
        self.__event_emitter.emit(Event.COMMAND_SENT, command_name)
