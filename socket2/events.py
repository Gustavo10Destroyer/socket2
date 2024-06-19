"""
Copyright (c) 2022-2024 Gustavo Vitor Alves Santos

Este projeto é de código aberto e pode ser modificado e distribuído sob os termos da Licença de Uso Não-Comercial e Restrita a IA disponível em https://github.com/Gustavo10Destroyer/socket2/blob/master/LICENSE.

Para os termos de uso comercial deste software e para o uso em treinamento de modelos para IA, consulte a Licença de Uso Não-Comercial e Restrita a IA mencionada acima.
"""
from typing import List
from typing import Callable

class Handler:
    def __init__(self, mode: str, event: str, handler: Callable) -> None:
        self.mode = mode
        self.event = event
        self.handler = handler

class EventEmitter:
    def __init__(self) -> None:
        self.handlers = [] # type: List[Handler]

    def on(self, event: str) -> None:
        def decorator(handler: Callable) -> None:
            self.handlers.append(Handler("on", event, handler))

        return decorator

    def once(self, event: str) -> None:
        def decorator(handler: Callable) -> None:
            self.handlers.append(Handler("once", event, handler))

        return decorator

    def emit(self, event: str, *args, **kwargs) -> None:
        for handler in self.handlers:
            if handler.event == event:
                handler.handler(*args, **kwargs)

                if handler.mode == "once":
                    self.handlers.remove(handler)

    def remove_listener(self, event: str, handler: Callable = None) -> None:
        for h in self.handlers:
            if h.event == event:
                if not handler or h.handler == handler:
                    self.handlers.remove(h)

    def remove_all_listeners(self, event: str = None) -> None:
        if event:
            for h in self.handlers:
                if h.event == event:
                    self.handlers.remove(h)
        else:
            self.handlers = []
