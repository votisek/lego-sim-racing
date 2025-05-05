import vgamepad as g
import time
import random

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
    

# Testování
if __name__ == "__main__":
    print("Testování gamepadu...")
    print("Zadejte vstup ve formátu '0,1' pro pedaly nebo '1,0,45,0,90' pro volant.")
    while True:
        control(f"{random.randint(0, 1)}, {random.randint(1, 1)}, {random.randint(-90, 90)}, -90, 90")
        time.sleep(0.02)