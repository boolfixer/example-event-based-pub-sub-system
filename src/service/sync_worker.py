import time
from typing import Optional

from PyQt6.QtCore import QRunnable

from src.enum.command import Command
from src.enum.event import Event
from src.service.comport_adapter import ComportAdapter
from src.service.event_emitter import EventEmitter


class SyncWorker(QRunnable):
    __comport_adapter: ComportAdapter = ComportAdapter()
    __event_emitter: EventEmitter = EventEmitter()

    __connection_opened = False
    __sync_interval: Optional[int] = None

    def __init__(self):
        super().__init__()

        self.__event_emitter.subscribe(Event.CONNECTION_OPENED, self.__on_connection_opened)
        self.__event_emitter.subscribe(Event.CONNECTION_CLOSED, self.__on_connection_closed)

    def run(self):
        last_sync_time = None

        while True:
            if not self.__connection_opened:
                continue

            now = time.time()

            if not last_sync_time or now - last_sync_time < self.__sync_interval:
                continue

            last_sync_time = now
            self.__send_sync_command()

    def __on_connection_opened(self, sync_interval: int):
        self.__sync_interval = sync_interval
        self.__connection_opened = True

    def __on_connection_closed(self):
        self.__connection_opened = False
        self.__sync_interval = None

    def __send_sync_command(self):
        self.__comport_adapter.write(Command.RXO.value)
        self.__event_emitter.emit(Event.COMMAND_SENT, Command.RXO.value)
