from typing import Callable, Optional

from src.enum.event import Event
from src.utils.abstract_singleton import AbstractSingleton


class EventEmitter(AbstractSingleton):
    __subscribers = {
        Event.CONNECTION_OPENED: [],
        Event.CONNECTION_CLOSED: [],
        Event.CONNECTION_FAILED: [],
        Event.COMMAND_SENT: [],
        Event.COMMAND_RESPONSE_RECEIVED: [],
        Event.COMMAND_BUTTON_CLICKED: [],
        Event.WARNING: []
    }

    def emit(self, event: Event, payload: Optional[any] = None):
        for subscriber in self.__subscribers[event]:
            if payload is not None:
                subscriber(payload)
            else:
                subscriber()

        pass

    def subscribe(self, event: Event, subscriber: Callable):
        self.__subscribers[event].append(subscriber)
