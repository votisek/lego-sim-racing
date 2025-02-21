#!/usr/bin/env python3
import socket
import time
import ev3dev2
import ev3dev2.sensor.lego as Sensor
import ev3dev2.sensor as SensorPort
import ev3dev2.motor as Motor
from ev3dev2.sound import Sound
import time

left_transmission = Sensor.TouchSensor(SensorPort.INPUT_2)
right_transmission = Sensor.TouchSensor(SensorPort.INPUT_1)
volant = Sensor.GyroSensor(SensorPort.INPUT_3)
sound = Sound()
print("init complete ol")



def set_debug(mode):
    if mode:
        delay = input("Zadej delay mezi čtením ůdajů ze senzorů: ")
        if delay == "":
            delay = 0.05
        else:
            delay = float(delay)
        max_left = input("Zadej maximální rotaci volantu doleva: ")
        if max_left == "":
            max_left = -90
        else:
            max_left = int(max_left)
        max_right = input("Zadej maximální rotaci volantu doprava: ")
        if max_right == "":
            max_right = 90
        else:
            max_right = int(max_right)
        volant_data = [max_left, max_right]
        

def calibrate():
#    global volant_data  # Přidáno: označení, že volant_data je globální proměnná
    volant.reset()
    volant.calibrate()

def get_volant():
    volant_angle = volant.angle
    if volant_angle < volant_data[0]:
        volant_angle = volant_data[0]
    else:
        pass
    if volant_angle > volant_data[1]:
        volant_angle = volant_data[1]
    else:
        pass
    return volant_angle

def get_data():
    data_right_transmission = right_transmission.is_pressed
    data_left_transmission = left_transmission.is_pressed
    data_volant = get_volant()
    min_volant, max_volant = volant_data
    return [data_left_transmission, data_right_transmission, data_volant, min_volant, max_volant]


def start_client():
    calibrate()
    print("calibrovano")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.94.38", 5656))
    print("pripojeno")

    try:
        # Odeslání identifikační zprávy na server
        client_socket.send(device.encode("utf-8"))
        if debug:
            while True:
                # Odesílání na server s debug
                data = get_data()
                client_socket.send(str(data).encode("utf-8"))
                print(data)
                time.sleep(0.1)
        else:
            while True:
                # Odeslání na server bez debug
                data = get_data()
                client_socket.send(str(data).encode("utf-8"))
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Ukončuji spojení klávesou CTRL+C.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    device = "volant"
    valid_data = bool()
    volant_data = [-90, 90]
    # debug = bool(input("debug mode: "))
    debug = True
    # volant_data in format: [max_left, max_right]
    # set_debug(debug)
    start_client()
