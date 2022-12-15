# socket2

## Exemplo de cliente
```py
from socket2 import Socket

client = Socket()
client.connect(("localhost", 8666))

client.send(b"Olá mundo!")

@client.on("data")
def on_data(data: bytes) -> None:
    print("Dados recebidos:")

    try:
        print(data.decode("utf-8"))
    except UnicodeDecodeError:
        print(data)

@client.on("close")
def on_close(address) -> None:
    print(f"A conexão com {address} foi fechada!")

while client.is_connected():
    client.step()
```

## Exemplo de servidor
```py
from socket2 import Socket

server = Socket()
server.bind(("localhost", 8666))
server.listen(5)

@server.on("connection")
def on_connection():
    client, address = server.accept()
    print(f"{address} se conectou!")

    @client.on("data")
    def on_data(data: bytes) -> None:
        print(f"{address} enviou dados:")

        try:
            print(data.decode("utf-8"))
        except UnicodeDecodeError:
            print(data)

        client.send(data)

    @client.once("close")
    def on_close(address) -> None:
        print(f"{address} foi desconectado!")

while server.is_connected():
    server.step()
```

# Métodos da classe `Socket`
### Daqui em diante ficam listados os métodos da classe `Socket`

## Socket.bind(address: tuple) -> None
### address: tuple(str, int)
### Retorna: None
### Descrição: Liga o socket a um endereço e uma porta
```py
from socket2 import Socket

socket = Socket()
socket.bind(("localhost", 8666))
...
```

## Socket.listen(backlog: int) -> None
### backlog: int
### Retorna: None
### Descrição: Coloca o socket em modo de escuta
```py
... # o trecho de código anterior
socket.listen(5)
... # o trecho de código posterior
```

## Socket.accept() -> tuple
### Retorna: tuple(Socket, tuple(str, int))
### Descrição: Aceita uma conexão
```py
... # o trecho de código anterior
client, address = socket.accept()
```

## Socket.connect(address: tuple) -> None
### address: tuple(str, int)
### Retorna: None
### Descrição: Conecta o socket a um endereço e uma porta
```py
from socket2 import Socket

socket = Socket()
socket.connect(("localhost", 8666))
...
```

## Socket.send(data: bytes) -> None
### data: bytes
### Retorna: None
### Descrição: Envia dados para o socket
```py
... # o trecho de código anterior
socket.send(b"Olá mundo!")
```

## Socket.recv(size: int) -> bytes
### size: int
### Retorna: bytes
### Descrição: Recebe dados do socket
```py
... # o trecho de código anterior
data = socket.recv(1024)
```

## Socket.close() -> None
### Retorna: None
### Descrição: Fecha o socket
```py
... # o trecho de código anterior
socket.close()
```

## Socket.is_connected() -> bool
### Retorna: bool
### Descrição: Retorna se o socket está conectado
```py
from socket2 import Socket

socket = Socket()
socket.bind(("localhost", 8666))
socket.listen(5)

while socket.is_connected():
    ...
```

## Socket.step() -> None
### Retorna: None
### Descrição: Função interna para o funcionamento do socket (eventos)
```py
    ... # o trecho de código anterior
    socket.step()
```

## Socket.on(event: str) -> Callable
### event: str
### Retorna: Callable
### Descrição: Decorador para eventos
```py
from socket2 import Socket

socket = Socket()
socket.bind(("localhost", 8666))
socket.listen(5)

@socket.on("connection")
def on_connection():
    ...

while socket.is_connected():
    socket.step()
```

## Socket.once(event: str) -> Callable
### event: str
### Retorna: Callable
### Descrição: Decorador para eventos que são chamados apenas uma vez
```py
    ... # o trecho de código anterior
    @socket.once("close")
    def on_close(address) -> None:
        print("O socket foi fechado!")
```

# Eventos da classe `Socket`
### Daqui em diante ficam listados os eventos da classe `Socket`

## Socket.on("connection")
### Descrição: Evento chamado quando um cliente se conecta ao servidor

## Socket.on("data")
### Parâmetros | data: bytes
### Descrição: Evento chamado quando o socket recebe dados

## Socket.on("close")
### Parâmetros | address: tuple(str, int)
### Descrição: Evento chamado quando o socket é fechado