# Lotus IDE Music player

debug = open("debug.txt","a+")

# Import Libs 
import tkinter as tk
from tkinter.ttk import *
from tkinter.tix import *
from tkinter import messagebox
from tkinter import filedialog
from playsound import playsound
from os import *
from datetime import datetime
from sys import *

win64 = os.environ["PROGRAMFILES(X86)"]

def log(msg):
    print(str(msg))
    debug.write("[" + str(datetime.now()) + "] " + str(msg) + "\n")
	
log("MUSIC PLAYER: STARTING MUSIC PLAYER...")
tkinter = tk.Tk()
tkinter.transient()
musicfile = filedialog.askopenfilename(title = "Select music file to play",initialdir = "C:/",filetypes = (("MP3 files","*.mp3"),("OGG files","*.ogg"),("Other file types","*.*")))
if musicfile and win64:
    tkinter.destroy()
    log("MUSIC PLAYER: PLAYING COOL MUSIC...")
    playsound(musicfile)
else:
    tkinter.destroy()
    sys.exit(0)
    debug.close()

tkinter.mainloop()
