# Lotus IDE Launcher
debug = open("debug.txt","a+")

# Import Libs
import tkinter as tk
from tkinter.ttk import *
from tkinter.tix import *
from tkinter import messagebox
from tkinter import filedialog
from os import system,mkdir,path
from sys import *
from PIL import *
from PIL import ImageTk
from PIL import Image
from datetime import datetime

def log(msg):
    print(str(msg))
    debug.write("[" + str(datetime.now()) + "] " + str(msg) + "\n")

def start():
    log("LAUNCHER: STARTING IDE...")
    tkinter.destroy()
    os.system("python main.py")
    log("LAUNCHER: IDE STARTED SUCCESSFULLY!!!")
    debug.close()
    sys.exit(0)
    
# Check contents before starting...
# Mainly,Lotus uses tkinter and Pillow and some main python modules as part of it
# NOTES: Unfortunately,Lotus only supports 64-bit versions of Microsoft Windows,Cause of some game engines binaries that is for 64-bit
log("LAUNCHER: CHECKING SUPPORT...")
contents_existed = (os.path.exists("resources/images") and os.path.exists("resources/inbound") and os.path.exists("docs") and os.path.exists("projects"))
win64 = os.environ["PROGRAMFILES(X86)"]

# Initializing window
log("LAUNCHER: INITIALIZING LAUNCHER...")
tkinter = tk.Tk()
tkinter.overrideredirect(1)
tkinter.geometry(("%dx%d+%d+%d") % (900,300,tkinter.winfo_screenwidth() / 6,tkinter.winfo_screenheight() / 3.3))
tkinter.resizable(0,0)

# If machine supported,Load resources
if contents_existed and win64:
    log("LAUNCHER: LOADING SPLAHSCREEN...")
    log("LAUNCHER: LOADING RESOURCES...")
    banner_image = Image.open("resources/images/lotus_banner.png")
    banner_image.resize((900,300),Image.ANTIALIAS)
    banner = ImageTk.PhotoImage(banner_image)
    banner_label = Label(tkinter,image = banner)
    banner_label.place(x = 10,y = 10)
    tkinter.after(2000,start)
    log("LAUNCHER: SPLASHSCREEN LOADED SUCCESSFULLY!!!")
    log("LAUNCHER: RESOURCES LOADED SUCCESSFULLY!!!")
else:
    log("ERROR: NOT x64 MACHINE!!!")
    tkinter.destroy()
    debug.close()
    sys.exit(0)
    
tkinter.mainloop()
