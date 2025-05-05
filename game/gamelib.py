#!/usr/bin/env python3
import socket
import threading
import vgamepad as g

# Nastavení serveru
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5656
gp = g.VX360Gamepad()

def calculate_volant(volant):
    volant = float(volant)
    if -90 > volant > 90:
        print("we got an error in calculate_volant()")
        gp.left_joystick_float(0, 0)
    elif -5 < volant < 5:
        gp.left_joystick_float(0, 0)
    else:
        gp.left_joystick_float(float(volant/90), 0)

def control(data):
    print(data)
    try:
        data = list(map(int, data.split(',')))  # Convert input string to list of integers
    except ValueError:
        print("Error: Input must be comma-separated integers.")
        return

    dev = None
    if data[-1] == 90:
        dev = 'volant'
    else:
        dev = 'pedaly'

    match dev:
        case "volant":
            if len(data) != 5:
                print("Error: Expected 5 values for 'volant' input.")
                return
            data_left_transmission, data_right_transmission, data_volant, _, _ = data
            match data_left_transmission:
                case 1:
                    gp.press_button(g.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                case 0:
                    gp.release_button(g.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                case _:
                    print("we got an error in data_left_transmission")
            gp.update()
            match data_right_transmission:
                case 1:
                    gp.press_button(g.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                case 0:
                    gp.release_button(g.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                case _:
                    print("we got an error in data_right_transmission")
            gp.update()
            calculate_volant(data_volant)
            gp.update()
        case "pedaly":
            if len(data) != 2:
                print("Error: Expected 2 values for 'pedaly' input.")
                return
            data_left_pedal, data_right_pedal = data
            match data_left_pedal:
                case 0:
                    gp.left_trigger_float(0)
                case 1:
                    gp.left_trigger_float(1)
                case _:
                    print("we got an error in data_left_pedal")
            gp.update()
            match data_right_pedal:
                case 0:
                    gp.right_trigger_float(0)
                case 1:
                    gp.right_trigger_float(1)
                case _:
                    print("we got an error in data_right_pedal")
            gp.update()
        case _:
            print("Unknown device type.")

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

