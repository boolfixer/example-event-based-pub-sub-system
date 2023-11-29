from PyQt6.QtCore import QRunnable

from src.enum.event import Event
from src.service.comport_adapter import ComportAdapter
from src.service.event_emitter import EventEmitter


class CommandListenerWorker(QRunnable):
    __comport_adapter: ComportAdapter = ComportAdapter()
    __event_emitter: EventEmitter = EventEmitter()

    __connection_opened = False

    def __init__(self):
        super().__init__()

        self.__event_emitter.subscribe(Event.CONNECTION_OPENED, self.__on_connection_opened)
        self.__event_emitter.subscribe(Event.CONNECTION_CLOSED, self.__on_connection_closed)

    def run(self):
        while True:
            if not self.__connection_opened:
                continue

            result = self.__comport_adapter.read()
            self.__event_emitter.emit(Event.COMMAND_RESPONSE_RECEIVED, result)

    def __on_connection_opened(self, _):
        self.__connection_opened = True

    def __on_connection_closed(self):
        self.__connection_opened = False
