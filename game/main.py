#!/usr/bin/env python3
import socket
import threading
import vgamepad as g

# Nastavení serveru
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5656
gp = g.VX360Gamepad()

def control(data):
    data = list(data)
    dev = None
    if 5 > len(data) > 2:
        for i in range(3):
            data.pop()
            if len(data) == 2:
                dev = "pedaly"
                break
            else:
                pass
    elif len(data) > 5:
        for i in range(20):
            data.pop()
            if len(data) == 5:
                dev = "volant"
                break
            else:
                pass
    else:
        pass
    match dev:
        case "volant":
            data_left_transmission, data_right_transmission, data_volant, _, _ = data
            match data_left_transmission:
                case 1:
                    gp.press_button(g.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                case 0:
                    gp.release_button(g.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                case _:
                    pass
            gp.update()

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
