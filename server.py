import socket

# Configurar servidor
host = '127.0.0.1'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

print(f"Servidor escuchando en {host}:{port}")

clients = []

def broadcast(message, client):
    for c in clients:
        if c != client:
            c.send(message)

while True:
    client, address = server.accept()
    print(f"Conexión establecida con {address}")
    clients.append(client)

    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            print(f"{address} dice: {message.decode()}")
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break