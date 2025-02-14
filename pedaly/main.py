#!/usr/bin/env python3
import socket
import time
import ev3dev2
import ev3dev2.sensor.lego as Sensor
import ev3dev2.sensor as SensorPort
from ev3dev2.sound import Sound
import time

left_pedal = Sensor.TouchSensor(SensorPort.INPUT_1)
right_pedal = Sensor.TouchSensor(SensorPort.INPUT_2)
sound = Sound()
print("init complete")

device = "pedaly"


def get_data():
    data_left_pedal = left_pedal.is_pressed
    data_right_pedal = right_pedal.is_pressed
    return [data_left_pedal, data_right_pedal]


def start_client():
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.128.242", 5656))
    

    try:
        # Odeslání identifikační zprávy na server
        client_socket.send(device.encode("utf-8"))

        while True:
            # Zadání zprávy od uživatele nebo automatické odeslání
            dtata = get_data()
            client_socket.send(str(dtata).encode("utf-8"))
            print(dtata)
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("Ukončuji spojení klávesou CTRL+C.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
