import json
import base64
import threading
import serializer
from socket import *
from events import EmitterAsync

def _recv(self):
  buffer = b""
  
  while self.mode == "client":
    packet = b""
    
    try:
      packet = socket.recv(self, 1024)
    except Exception as e:
      if self.mode == "closed":
        return None
      else:
        raise e
    
    buffer += packet
    
    if len(packet) > 0:
      if packet.endswith("\r\n".encode()):
        buffer = buffer.rsplit("\r\n".encode(), 1)[0]
        
        try:
          data = serializer.loads(buffer.decode())
          
          if "type" in data and data["type"] == "event":
            EmitterAsync.emit(self, data["name"], *data["data"])
          else:
            if data["type"] in ["str", "int", "float", "bool"]:
              EmitterAsync.emit(self, "data", data["data"])
            elif data["type"] in ["list", "dict", "tuple"]:
              EmitterAsync.emit(self, "data", data["data"])
            elif data["type"] == "tuple":
              EmitterAsync.emit(self, "data", data["data"])
            elif data["type"] == "bytes":
              EmitterAsync.emit(self, "data", base64.b64decode(data["data"].encode()))
            elif data["type"] == "complex":
              EmitterAsync.emit(self, "data", complex(data["data"]))
        except Exception:
          EmitterAsync.emit(self, "data", buffer)
        
        buffer = b""
    else:
      self.close()

class Socket2(socket, EmitterAsync):
  def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
    self.mode = "base"
    EmitterAsync.__init__(self)
    socket.__init__(self, family, type, proto, fileno)
    
    if fileno:
      self.mode = "client"
      threading.Thread(target=_recv, args=[self]).start()

  def accept(self):
    fd, addr = super()._accept()

    sock = Socket2(self.family, self.type, self.proto, fd)

    return sock, addr

  def connect(self, address):
    socket.connect(self, address)
    self.mode = "client"
    threading.Thread(target=_recv, args=[self]).start()

  def send(self, data):
    if type(data) == bytes:
      data = {
        "type": "bytes",
        "data": base64.b64encode(data).decode()
      }
    elif type(data) in [list, tuple]:
      data = {
        "type": type(data).__name__,
        "data": data
      }
    elif type(data) == dict:
      if "type" in data:
        if data["type"] == "event":
          pass
      else:
        data = {
          "type": "dict",
          "data": data
        }
    elif type(data) == complex:
      data = {
        "type": "complex",
        "data": str(data)
      }
    elif type(data) in [int, float, str, bool]:
      data = {
        "type": type(data).__name__,
        "data": data
      }
    else:
      raise TypeError("Este tipo de dados não é suportado!")

    socket.sendall(self, (serializer.dumps(data) + "\r\n").encode())

  def emit(self, event, *data):
    return self.sendall({
      "type": "event",
      "name": event,
      "data": list(data)
    })

  def sendall(self, data):
    self.send(data)

  def close(self):
    if not self.mode == "closed":
      self.mode = "closed"
      socket.close(self)
      EmitterAsync.emit(self, "close")