import socket
import threading

# Configurar cliente
host = '127.0.0.1'
port = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print(f"\n{message}")
        except:
            print("Error al recibir mensaje")
            client.close()
            break

def send_messages():
    while True:
        message = input("")
        client.send(message.encode())

# Hilos para enviar y recibir simultáneamente
threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages).start()