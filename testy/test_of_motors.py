
import socket
import time
import ev3dev2
import ev3dev2.sensor.lego as Sensor
import ev3dev2.sensor as SensorPort
import ev3dev2.motor as Motor
from ev3dev2.sound import Sound
import time

left_transmission = Sensor.TouchSensor(SensorPort.INPUT_1)
right_transmission = Sensor.TouchSensor(SensorPort.INPUT_2)
volant = Sensor.GyroSensor(SensorPort.INPUT_3)
sound = Sound()
print("init complete")

device = "volant"
valid_data = bool()
volant_data = [-90, 90]
# volant_data in format: [max_left, max_right]

def calibrate():
#    global volant_data  # Přidáno: označení, že volant_data je globální proměnná
    volant.reset()
#    sound.play_tone(500, 1)
#    for i in range(2):
#        if i == 0:
#            input("volant doleva a enter")
#        else:
#            input("volant doprava a enter")
#        sound.play_tone(500, 1)
#        print("got press")
#        for j in range(50):
#            volant_data[i] += volant.angle
#            time.sleep(0.05)
#        volant_data[i] = volant_data[i] / 50
#        sound.play_tone(500, 1)
#    print("calib complete")
#    input("sec step of cali: set to 0")
#    volant.reset()
#    print("calib2 complete")

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
    return [data_right_transmission, data_left_transmission, data_volant, min_volant, max_volant]

def main():
    volant.reset()
    volant.calibrate()
    while True:
        print(str(get_data()))

main()