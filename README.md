# socket2
Esse módulo permite a criação de conexões TCP assíncronas, e o envio direto de dados, sem precisar codificá-los em bytes, além de receber já decodificados

**Exemplo de Servidor**
```py
from socket2 import Socket2

host = "localhost" # Auto-explicativo
port = 8888 # Auto-explicativo
max = 1 # Limite de conexões simultâneas

server = Socket2() # Cria uma instância Socket2
server.bind((host, port)) # Auto-explicativo
server.listen(max) # Escuta o máximo de conexões

client, address = server.accept()

@client.on
def message(author, content):
  print(f"[{author}]: {content}")

@client.once
def close(): # Built-in [ emitida por padrão pelo próprio servidor ]
  print("A conexão foi finalizada!")
  server.close()
```

**Exemplo de Cliente**
```py
from socket2 import Socket2

host = "localhost" # Auto-explicativo
port = 8888 # Auto-explicativo

socket = Socket2()
socket.connect((host, port))

username = input("Nome de usuário: ")

while True:
  content = input(f"{username} >>> ")

  socket.emit("message", username, content)
```

**Explicação do funcionamento**
Para criar uma função use ```@Socket2.on``` (substitua o Socket2 pelo nome da variável)
E defina uma função abaixo, **o evento será o nome da função**

**Observação: O cliente e o servidor devem estar usando a classe para um bom funcionamento!
(Pode conter bugs, não use para produção)**
