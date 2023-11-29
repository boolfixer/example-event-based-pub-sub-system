import typing

from PyQt6.QtWidgets import QTextBrowser

from src.enum.event import Event
from src.service.event_emitter import EventEmitter


class ConsoleOutputTextarea(QTextBrowser):
    __event_emitter = EventEmitter()

    def __init__(self):
        super().__init__()

        self.__event_emitter.subscribe(Event.CONNECTION_OPENED, self.__on_connection_opened)
        self.__event_emitter.subscribe(Event.CONNECTION_CLOSED, self.__on_connection_closed)
        self.__event_emitter.subscribe(Event.CONNECTION_FAILED, self.__on_connection_failed)
        self.__event_emitter.subscribe(Event.COMMAND_SENT, self.__on_command_sent)
        self.__event_emitter.subscribe(Event.COMMAND_BUTTON_CLICKED, self.__on_command_button_clicked)
        self.__event_emitter.subscribe(Event.COMMAND_RESPONSE_RECEIVED, self.__on_command_response_received)
        self.__event_emitter.subscribe(Event.WARNING, self.__on_warning_received)

    # override in order to scroll down all the time when we append new message to the end
    def append(self, text: typing.Optional[str]) -> None:
        super().append(text)
        self.__scroll_to_the_end()

    def __on_connection_opened(self, _):
        message = 'Connection opened.'
        self.append(message)

    def __on_connection_closed(self):
        message = 'Connection closed.'
        self.append(message)

    def __on_connection_failed(self):
        message = 'Connection failed.'
        self.append(message)

    def __on_command_sent(self, command_name: str):
        message = f'Command {command_name} was sent.'
        self.append(message)

    def __on_command_button_clicked(self, command: str):
        message = f'Command button {command} was clicked.'
        self.append(message)

    def __on_command_response_received(self, response: str):
        message = f'Command response received: {response}'
        self.append(message)

    def __on_warning_received(self, message: str):
        self.append('[WARNING]: ' + message)

    def __scroll_to_the_end(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
