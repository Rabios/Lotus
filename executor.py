# Lotus IDE Executor tool
# Execute collections of batch commands parallely at once
debug = open("debug.txt","a+")
batcache = open("resources/cache/last.bat","w+")
batcache.truncate(0)

# Import Libs
try:
    import Tkinter as tk
    from Tkinter import ttk
    from Tkinter import tix
    from Tkinter import tkMessageBox
    from Tkinter import tkFileDialog
except ImportError:
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

def runbat():
    batcache.write(editor.get("1.0",END))
    tkinter.destroy()
    batcache.close()
    log("EXECUTOR: EXECUTING COMMANDS...")
    os.system("start resources\cache\last.bat")
    log("EXECUTOR: COMMANDS EXECUTED SUCCESSFULLY!!!")
    debug.close()
    sys.exit(0)
    
# Check contents before starting...
# Mainly,Lotus uses tkinter and Pillow and some main python modules as part of it
# NOTES: Unfortunately,Lotus only supports 64-bit versions of Microsoft Windows,Cause of some game engines binaries that is for 64-bit
log("EXECUTOR: CHECKING SUPPORT...")
contents_existed = (os.path.exists("resources/images") and os.path.exists("resources/inbound") and os.path.exists("docs") and os.path.exists("projects"))
win64 = os.environ["PROGRAMFILES(X86)"]
    
# Initializing window
log("EXECUTOR: INITIALIZING LAUNCHER...")
tkinter = tk.Tk()

if not win64 or not contents_existed:
    log("ERROR: NOT x64 MACHINE OR RESOURCES IS MISSING!!!")
    tkinter.destroy()
    debug.close()
    batcache.close()
    sys.exit(0)

log("EXECUTOR: INITIALIZING EXECUTOR WINDOW...")
tkinter.title("Lotus IDE Executor")
tkinter.geometry("600x414")
tkinter.iconphoto(False,PhotoImage(file = "resources/images/lotus_icon.png"))
tkinter.resizable(0,0)

log("EXECUTOR: LOADING WINDOW GUI...")
editor = Text(tkinter)
editor.pack(fill = "both")
runbutton = Button(tkinter,text = "EXECUTE",command = runbat)
runbutton.pack(fill = "x")
log("EXECUTOR: WINDOW GUI LOADED SUCCESSFULLY!!!")

tkinter.mainloop()
