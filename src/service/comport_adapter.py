import serial

from src.enum.event import Event
from src.service.event_emitter import EventEmitter
from src.utils.abstract_singleton import AbstractSingleton


class ComportAdapter(AbstractSingleton):
    __port = None
    __port_name: str = None
    __event_emitter = EventEmitter()

    def open(self, port_name: str, baud_rate: int, sync_interval: int):
        try:
            self.__port_name = port_name
            self.__port = serial.Serial(self.__port_name, baud_rate)
        except:
            self.__event_emitter.emit(Event.CONNECTION_FAILED)
            return

        self.__event_emitter.emit(Event.CONNECTION_OPENED, sync_interval)

    def close(self):
        self.__port.close()

        self.__event_emitter.emit(Event.CONNECTION_CLOSED)

    def read(self) -> str:
        return self.__port.readline().decode('utf-8')

    def write(self, text: str):
        self.__port.write(text.encode())
