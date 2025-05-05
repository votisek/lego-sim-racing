import gamelib
import customtkinter
import json

gui = customtkinter.CTk()
gui.title("lego-racing-sim Driver")
gui.geometry("800x600")
is_scanning = False
lang = "en-us"
langfile = dict()
l = None
with open("/home/linux/Documents/code/LeWhego/game/lang.json", "r") as f:
    langfile = json.load(f)
    l = langfile.get(lang)
    print(l["button_start_scanning"])
    f.close()

def start_scanning():
    print('def scanning')

button = customtkinter.CTkButton(gui, text=l.get("button_start_scanning"), command=start_scanning)

gui.mainloop()