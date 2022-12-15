from typing import Tuple
from socket2 import Socket

client = Socket()
client.connect(("localhost", 8666))

client.send(b"Hello world!")

@client.on("data")
def on_data(data: bytes) -> None:
    print("O servidor enviou:")
    print(data.decode())

@client.on("close")
def on_close(address: Tuple[str, int]):
    print(f"O servidor desconectou! {address}")

while client.is_connected():
    client.step()