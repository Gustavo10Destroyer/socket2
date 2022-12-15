from typing import Tuple
from socket2 import Socket

server = Socket()
server.bind(("localhost", 8666))
server.listen(2)

@server.on("connection")
def on_connection():
    client, address = server.accept()
    client.broadcast(f"Um novo cliente se conectou! {address}".encode())
    print(f"O cliente conectou! {address}")

    @client.on("data")
    def on_data(data: bytes):
        print("O cliente enviou:")
        print(data.decode())

        client.send(data)

    @client.on("close")
    def on_close(address: Tuple[str, int]):
        print(f"O cliente desconectou! {address}")

while server.is_connected():
    server.step()