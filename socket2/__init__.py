"""
Copyright (c) 2022-2024 Gustavo Vitor Alves Santos

Este projeto é de código aberto e pode ser modificado e distribuído sob os termos da Licença de Uso Não-Comercial e Restrita a IA disponível em https://github.com/Gustavo10Destroyer/socket2/blob/master/LICENSE.

Para os termos de uso comercial deste software e para o uso em treinamento de modelos para IA, consulte a Licença de Uso Não-Comercial e Restrita a IA mencionada acima.
"""
import os
import atexit
import socket
import select
import shutil
from . import events
from typing import List
from typing import Tuple

SERVER = "@server"
CLIENT = "@client"
PEER = "@peer"

class Socket(socket.socket, events.EventEmitter):
    def __init__(self, family=-1, _type=-1, proto=-1, fileno=None) -> None:
        events.EventEmitter.__init__(self)
        socket.socket.__init__(self, family, _type, proto, fileno)

        self.mode = None
        self._listening = False
        self._clients = [] # type: List[Socket]

        if fileno:
            self.mode = PEER

        # apagar a pasta '__pycache__'
        shutil.rmtree(os.path.join(os.path.dirname(__file__), "__pycache__"), True)

        # registrar a função 'on_exit' para ser executada quando o programa for fechado
        atexit.register(self.on_exit)

    def bind(self, address: Tuple[str, int]) -> None:
        if self.mode != None:
            raise Exception("O socket já está sendo usado!")

        self.mode = SERVER
        socket.socket.bind(self, address)

    def listen(self, backlog: int) -> None:
        if self.mode != SERVER:
            raise Exception("O socket não é um servidor!")

        socket.socket.listen(self, backlog)
        self._listening = True

    def connect(self, address: Tuple[str, int]) -> None:
        if self.mode != None:
            raise Exception("O socket já está sendo usado!")

        self.mode = CLIENT
        socket.socket.connect(self, address)

    def is_connected(self) -> bool:
        if self.mode == SERVER:
            return self._listening

        return self.mode != None

    def accept(self) -> "Socket":
        if self.mode != SERVER:
            raise Exception("O socket não é um servidor!")

        _fd, address = socket.socket._accept(self)
        sock = Socket(self.family, self.type, self.proto, _fd)
        self._clients.append(sock)

        @sock.once("_should_remove")
        def on_should_remove():
            # remover o socket da lista de clientes
            self._clients.remove(sock)

        @sock.on("_should_broadcast")
        def on_should_broadcast(data: bytes) -> None:
            # enviar os dados para todos os clientes
            for client in self._clients:
                # não enviar os dados para o próprio cliente de origem
                if client.getpeername() != address:
                    client.send(data)

        return sock, address

    def send(self, data: bytes) -> int:
        if self.mode == None:
            raise Exception("O socket não está conectado!")
        elif self.mode == SERVER:
            raise Exception("O socket é um servidor!")

        return socket.socket.send(self, data)

    def recv(self, buffer_size: int, flags: int = None) -> bytes:
        if self.mode == None:
            raise Exception("O socket não está conectado!")
        elif self.mode == SERVER:
            raise Exception("O socket é um servidor!")

        if not flags:
            data = socket.socket.recv(self, buffer_size)

            if not data:
                self.close()
                return b""

            return data

        data = socket.socket.recv(self, buffer_size, flags)

        if not data:
            self.close()
            return b""

        return data

    def close(self, ignore_exceptions: bool = True) -> None:
        if not ignore_exceptions:
            if self.mode == None:
                raise Exception("O socket não está conectado!")

        if self.mode == PEER:
            self.emit("_should_remove")

        if self.mode == SERVER:
            self._listening = False

        if self.mode != None:
            address = self.getpeername()
            self.emit("close", address)

        self.mode = None
        socket.socket.close(self)

    def on_exit(self) -> None:
        if self.mode == SERVER:
            for client in self._clients:
                client.close()

        self.close()

    def broadcast(self, data: bytes) -> None:
        if self.mode == None:
            raise Exception("O socket não está conectado!")

        if self.mode == SERVER:
            for client in self._clients:
                client.send(data)
            return

        if self.mode == CLIENT:
            self.send(data)
            return

        self.emit("_should_broadcast", data)

    def step(self) -> None:
        if self.mode == SERVER:
            self._step_server()
        elif self.mode == CLIENT:
            self._step_client()
        elif self.mode == PEER:
            self._step_peer()

    def _step_server(self) -> None:
        read, write, error = select.select([self], [], [], 0.016) # 60 times per second

        if self in read:
            self.emit("connection")

        for client in self._clients:
            client.step()

    def _step_client(self) -> None:
        read, write, error = select.select([self], [], [], 0.016) # 60 times per second

        if self in read:
            try:
                data = self.recv(1024)
            except:
                self.close()
                return

            if not data:
                self.close()
                return

            self.emit("data", data)

    def _step_peer(self) -> None:
        read, write, error = select.select([self], [], [], 0.016) # 60 times per second

        if self in read:
            try:
                data = self.recv(1024)
            except:
                self.close()
                return

            if not data:
                self.close()
                return

            self.emit("data", data)
