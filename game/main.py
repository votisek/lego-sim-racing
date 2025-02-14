#!/usr/bin/env python3
import socket
import threading
import vgamepad

# Nastavení serveru
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5656
gp = vgamepad.VX360Gamepad()

def control(data):
    if '"]' not in str(data):
        pass
    else:
        data = str(data).split('"]', 1).pop()
    print(data)

# Vytvoření TCP/IP socketu
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)  # Umožní až 5 čekajících připojení
print(f"Server běží na {SERVER_HOST}:{SERVER_PORT}")

def handle_client(client_socket, address):
    print(f"Připojen nový klient: {address}")
    print(f"zarizeni: {client_socket.recv(1024)}")
    
    try:
        while True:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                print(f"Klient {address} se odpojil.")
                break
            control(data=data)
    except ConnectionResetError:
        print(f"Klient {address} se neočekávaně odpojil.")
    finally:
        client_socket.close()

def main():
    print("Server je připraven přijímat spojení.")
    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer ukončen klávesou CTRL+C.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
