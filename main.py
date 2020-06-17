# PyLotus,Lua and Moonscript IDE written in Python 3
# Written by Rabia Alhaffar in 25/May/2020
# Last update: v0.1.3
# Lotus is Open-Source Lua IDE for developing applications and games with Lua and Moonscript
# From simple console apps to games with your preferred engine/framework
# See LICENSE.txt for more

# Code editor resources
# https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
# https://stackoverflow.com/questions/50786590/tkinter-pygments-strange-results-in-highlighting
# https://stackoverflow.com/questions/32058760/improve-pygments-syntax-highlighting-speed-for-tkinter-text

debug = open("debug.txt","a+")

mainprojectfilename = "main.lua"
fileext = ".lua"
count = 0
lotus_version = "v0.1.3"

projectlabel = ""
current_project_loc = ""
current_project_dir = ""
current_project_name = ""
current_project_fold = ""
opened_project_path = ""

project_opened = False
file_opened = False
file = ""   # Current file or main project file that is opened,If not opened so use "noname" by default

# Getting language for translation
current_language = open("resources/languages/current.txt","r")
language_file = current_language.read()
language = open("resources/languages/" + str(language_file),"r")
language_strings = []
for strings in language.readlines():
    language_strings.append(strings.strip())
current_language.close()
language.close()

# Getting theme of Lotus IDE
current_theme = open("resources/themes/current.txt","r")
theme_filename = current_theme.read()
theme_file = open("resources/themes/" + str(theme_filename),"r")
theme_strings = []
for themestrings in theme_file.readlines():
    theme_strings.append(themestrings.strip())
current_theme.close()
theme_file.close()

# Snippets list,Starts by custom snippets and then by the language snippets
# Create your own in snippets.txt,Note that each snippet is function or something takes 1 line
snippets_content = [ open("resources/snippets/custom.txt","r"),
                     open("resources/snippets/lua.txt","r"),
                     open("resources/snippets/luajit.txt","r"),
                     open("resources/snippets/lualibs.txt","r"),
                     open("resources/snippets/moonscript.txt","r"),
                     open("resources/snippets/love2d.txt","r"),
                     open("resources/snippets/lovr.txt","r"),
                     open("resources/snippets/amulet.txt","r"),
                     open("resources/snippets/scrupp.txt","r") ]

snippets_list = []
for snippets in snippets_content:
    snip = snippets.readlines()
    for line in snip:
        snippets_list.append(line.strip())
    snippets.close()

# Import Libs 
import tkinter as tk
from tkinter.ttk import *
from tkinter.tix import *
from tkinter import messagebox
from tkinter import filedialog
from os import system,mkdir,path,startfile
from sys import *
import webbrowser
from PIL import *
from PIL import ImageTk
from PIL import Image
from zipfile import *
from datetime import datetime
from pygments import lex
from pygments.token import Token
from pygments.lexers.scripting import LuaLexer
from pathlib import *
from shutil import *
import tokenize as tokenize
import io as io
from keyword import *

# Classes for code editor
class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

# Got it from link below,But i modified it for some reasons
# https://stackoverflow.com/a/13814557/10896648
def copytree(src, dst, ignore = True):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                copy2(s, d)

def log(msg):
    print(str(msg))
    debug.write("[" + str(datetime.now()) + "] " + str(msg) + "\n")
    
def pathquote(p):
    return '"' + p + '"'

def restart():
    log("RESTARTING LOTUS IDE...")
    tkinter.destroy()
    debug.close()
    os.system("launch.bat")
    sys.exit(0)
    
def luacmd():
    log("STARTING LUA COMMAND LINE...")
    if os.path.exists("resources/packages/lua"):
        os.system("switch.bat 2")
        log("LUA COMMAND LINE STARTED SUCCESSFULLY!!!")
    
def getlog():
    log("OPENING DEBUG LOG TEXT FILE...")
    os.system("switch.bat 1")
    log("DEBUG LOG TEXT FILE OPENED SUCCESSFULLY!!!")
    
def cmd():
    log("LAUNCHING COMMAND PROMPT...")
    os.system("switch.bat 5")
    log("COMMAND PROMPT LAUNCHED SUCCESSFULLY!!!")

def openexec():
    log("LAUNCHING EXECUTOR...")
    os.system("switch.bat 3")
    log("EXECUTOR LAUNCHED SUCCESSFULLY!!!")
    
def close():
    log("CLOSING IDE...")
    if file_opened:
        savefile()
    elif project_opened:
        saveproject()
    tkinter.destroy()
    debug.close()
    sys.exit(0)

def exit_fullscreen():
    log("DISABLING FULLSCREEN MODE...")
    tkinter.attributes("-fullscreen",False)
    log("FULLSCREEN MODE DISABLED SUCCESSFULLY!!!")

def enable_fullscreen():
    log("TOGGLING FULLSCREEN MODE...")
    tkinter.attributes("-fullscreen",True)
    log("FULLSCREEN MODE TOGGLED SUCCESSFULLY!!!")

def clear_log():
    log("CLEARING DEBUG LOG TEXT FILE...")
    debug.truncate(0)
    log("DEBUG LOG TEXT FILE CLEARED SUCCESSFULLY!!!")
    debug.truncate(0)
        
def about():
    log("DISPLAYING ABOUT WINDOW...")
    messagebox.showinfo("About Lotus IDE","Lotus IDE " + lotus_version + "\nLotus is an Open-Source IDE for Moonscript and Lua written in Python 3\n\nWritten by Rabia Alhaffar")
    log("ABOUT WINDOW DISPLAYED SUCCESSFULLY!!!")
    
def source():
    log("OPENING SOURCE CODE WEBSITE")
    webbrowser.open_new_tab("https://github.com/Rabios/Lotus")
    log("SOURCE CODE WEBSITE OPENED SUCCESSFULLY!!!")

def letter():
    messagebox.showinfo("Letter from the heart","Thank you so much for using Lotus IDE for developing your projects,I really appreciate that!!!\n\nYou can also support me by submitting issues about bugs on GitHub\nOr either contribute to add features to Lotus IDE\n\nReally thanks,From my heart!!!\nBest wishes,Rabia Alhaffar")

def luajit():
    log("STARTING LUAJIT...")
    os.system("resources\packages\luajit\luajit.cmd")
    log("LUAJIT STARTED SUCCESSFULLY!!!")
 
# Project wizard
def newproject():
    global project_opened
    global file_opened
    # Project wizard menu,Honestly...
    log("LOADING PROJECT WIZARD...")
    project_wizard = Toplevel()
    ploc = StringVar()
    project_wizard.title(language_strings[66])
    project_wizard.geometry(("%dx%d+%d+%d") % (480,140,project_wizard.winfo_screenwidth() / 3,project_wizard.winfo_screenheight() / 3))
    project_wizard.resizable(False, False)
    project_wizard.iconphoto(False,PhotoImage(file = "resources/images/lotus_icon.png"))
    projectname = Label(project_wizard,text = language_strings[67]) 
    projectnameentry = Entry(project_wizard,width = 58)
    projectname.place(x = 5,y = 10)
    projectnameentry.place(x = 110,y = 10)
    projectlocation = Label(project_wizard,text = language_strings[68]) 
    projectlocationentry = Entry(project_wizard,width = 58,textvariable = ploc)
    ploc.set(os.path.join(os.getcwd(),"projects"))
    projectlocation.place(x = 5,y = 40)
    projectlocationentry.place(x = 110,y = 40)

    # Setup project steps: Check project type -> Create directory -> Create main file -> Open main file to edit
    def setupproject():
        global project_opened
        global file_opened
        project_opened = True
        file_opened = False
        log("CREATING PROJECT...")
        if not os.path.isfile(projectlocationentry.get()):
            # Set created project main file name according to project type
            if projecttypes.get() == "Lua project":
                mainprojectfilename = "main.lua"
            elif projecttypes.get() == "MoonScript project":
                mainprojectfilename = "main.moon"
            elif projecttypes.get() == "Scrupp Lua project":
                mainprojectfilename = "main.slua"
                
        # Create project folder in project directories
        if not os.path.isdir(os.path.join(projectlocationentry.get(),projectnameentry.get())) and not os.path.isfile(os.path.join(projectnameentry.get(),projectlocationentry.get())):
            os.mkdir(os.path.join(projectlocationentry.get(),projectnameentry.get()))

        # Read project main file and read it,Display content in editor with setting filename label
        mainfile = open(os.path.join(os.path.join(projectlocationentry.get(),projectnameentry.get()),mainprojectfilename),"w+")
        mainfilelocator = open(os.path.join(os.path.join(projectlocationentry.get(),projectnameentry.get()),"main.txt"),"w+")
        mainfilelocator.write(os.path.join(os.path.join(projectlocationentry.get(),projectnameentry.get()),mainprojectfilename))
        mainfilelocator.close()
        projectlabel = os.path.join(os.path.join(projectlocationentry.get(),projectnameentry.get()))
        current_file.set(os.path.join(projectlabel,mainprojectfilename))
        opened_project_path = Path(current_file.get()).parents[0]
        current_project_name = os.path.join(projectnameentry.get(),"")
        current_project_dir = os.path.join(projectlocationentry.get(),"")
        current_project_loc = os.path.join(projectlocationentry.get(),projectnameentry.get())
        current_project_fold = os.path.basename(os.path.normpath(projectlocationentry.get()))
        file = os.path.join(projectlabel,mainprojectfilename)
        codeeditor.delete("1.0",END)
        codeeditor.insert(INSERT,mainfile.read())
        mainfile.close()
        project_wizard.destroy()
        log("PROJECT CREATED SUCCESSFULLY!!!")

    # Buttons and Combobox
    createprojectbutton = Button(project_wizard,text = language_strings[69],command = setupproject)
    cancelprojectbutton = Button(project_wizard,text = language_strings[70],command = project_wizard.destroy)
    createprojectbutton.place(x = 315,y = 105)
    cancelprojectbutton.place(x = 415,y = 105)
    projecttype = Label(project_wizard,text = language_strings[71])
    projecttype.place(x = 5,y = 70)
    projecttypes = ttk.Combobox(project_wizard,width = 55)

    # Project types
    projecttypes["values"] = ( "Lua project",
                               "MoonScript project",
                               "Scrupp Lua project" )
    projecttypes.place(x = 110,y = 70)
    projecttypes.current(0)
    project_wizard.mainloop()

# Projects functions section
def openproject():
    global project_opened
    global file_opened
    # Ask for project folder then read from main.txt in the project folder to open main file
    projecttoopen = filedialog.askdirectory(initialdir = "C:/",title = language_strings[72])
    if projecttoopen and not os.path.isfile(projecttoopen):
        log("OPENING SELECTED PROJECT...")
        saveproject()
        if os.path.exists(os.path.realpath(os.path.join(projecttoopen,"main.txt"))) and os.path.isfile(os.path.realpath(os.path.join(projecttoopen,"main.txt"))) and projecttoopen:
            mainprojectfile = open(projecttoopen + "/main.txt","r")
            mainfile = open(str(mainprojectfile.read()),"r")
            current_file.set(str(os.path.realpath(mainfile.name)))
            opened_project_path = Path(current_file.get()).parents[0]
            codeeditor.delete("1.0",END)
            codeeditor.insert(INSERT,mainfile.read())
            project_opened = True
            file_opened = False
            mainfile.close()
            mainprojectfile.close()
        else:
            messagebox.showerror(language_strings[102],language_strings[103])
        log("SELECTED PROJECT OPENED SUCCESSFULLY!!!")

def addfilestoproject():
    global project_opened
    log("ADDING FILES TO PROJECT...")
    filesadded = []
    filesadded.clear()
    if project_opened:
        project_loc = PurePath(current_file.get())
        addfiles = filedialog.askopenfilenames(title = language_strings[74],initialdir = "C:/",filetypes = (("Lua files","*.lua"),("MoonScript files","*.moon"),("Scrupp files","*.slua"),("Other file types","*.*")))
        for f in addfiles:
            filesadded.append(f)
        for filestoadd in filesadded:
            # Add files to project folder location,Don't do any f***ing modifications right here!!!
            copyfile(os.path.realpath(filestoadd),os.path.realpath(os.path.join(os.path.join(project_loc.parents[1].name,project_loc.parent.name),os.path.basename(filestoadd))))
    log("FILES ADDED TO PROJECT SUCCESSFULLY!!!")
                
def addfoldertoproject():
    global project_opened
    if project_opened:
        folder = filedialog.askdirectory(title = language_strings[97],initialdir = "C:/")
        if folder:
            path = Path(current_file.get())
            log("ADDING FOLDER TO THE CURRENT PROJECT...")
            copytree(os.path.realpath(folder),os.path.realpath(os.path.join(path.parents[0],os.path.basename(folder))))
            log("FOLDER ADDED TO THE CURRENT PROJECT SUCCESSFULLY!!!")
            
def saveproject():
    global project_opened
    if project_opened:
        log("SAVING PROJECT...")
        file = open(current_file.get(),"w+")
        file.truncate(0)
        file.write(codeeditor.get("1.0",END))
        file.close()
        log("PROJECT SAVED SUCCESSFULLY!!!")

def refresh():
    global project_opened
    global file_opened
    log("REFRESHING CURRENT CONTENT...")
    if not project_opened or not file_opened:
        current_file.set(language_strings[65])
        codeeditor.delete("1.0",END)
    log("CONTENT REFRESHED SUCCESSFULLY!!!")


def deleteproject():
    global project_opened
    log("DELETING PROJECT...")
    delete = messagebox.askyesno(title = language_strings[74],message = language_strings[75])
    if project_opened and delete:
        path = Path(current_file.get())
        closeproject()
        rmtree(os.path.realpath(path.parents[0]),ignore_errors = True)
    log("PROJECT DELETED SUCCESSFULLY!!!")

def obfuscateproject():
    path = Path(current_file.get())
    log("OBFUSCATING PROJECT...")
    os.system(os.path.realpath(os.path.join("resources/packages/","obfuscate_lua_project.bat")) + " " + os.path.realpath(current_file.get()))
    os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"bytecode")))
    log("PROJECT OBFUSCATED SUCCESSFULLY!!!")
    

def decompileproject():
    path = Path(current_file.get())
    log("DECOMPILING PROJECT...")
    os.system(os.path.realpath(os.path.join("resources/packages/","decompile_lua_project_bytecode.bat")) + " " + os.path.realpath(current_file.get()))
    os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"decompiled")))
    log("PROJECT DECOMPILED SUCCESSFULLY!!!")

def disasmproject():
    path = Path(current_file.get())
    log("DISASSEMBLING PROJECT...")
    os.system(os.path.realpath(os.path.join("resources/packages/","disassembly_lua_project.bat")) + " " + os.path.realpath(current_file.get()))
    os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"disasm")))
    log("PROJECT DISASSEMBLED SUCCESSFULLY!!!")

def cleanproject():
    global project_opened
    log("CLEANING PROJECT...")
    clean = messagebox.askyesno(title = language_strings[76],message = language_strings[77])
    if project_opened and clean:
        path = Path(current_file.get())
        rmtree(os.path.join(path.parents[0],"build"),ignore_errors = True)
        log("PROJECT CLEANED SUCCESSFULLY!!!")
        messagebox.showinfo(language_strings[104],language_strings[105])
    else:
        log("PROJECT NOT CLEANED!!!")

def closeproject():
    global project_opened
    if project_opened:
        log("CLOSING PROJECT...")
        project_opened = False
        codeeditor.delete("1.0",END)
        refresh()
        log("PROJECT CLOSED SUCCESSFULLY!!!")


def projectexplorer():
    global project_opened
    if project_opened:
        log("OPENING PROJECT IN EXPLORER...")
        path = Path(current_file.get())
        os.system("start " + os.path.realpath(path.parents[0]))
        log("PROJECT OPENED IN EXPLORER SUCCESSFULLY!!!")


# Files functions section
def openfile():
    global file_opened
    global project_opened
    if file_opened:
        savefile()
    if project_opened:
        saveproject()
    filetoopen = filedialog.askopenfilename(title = language_strings[86],initialdir = "C:/",filetypes = (("Lua file","*.lua"),("Scrupp Lua file","*.slua"),("MoonScript file","*.moon"),("Other file types","*.*")))
    if filetoopen:
        log("OPENING FILE...")
        f = open(filetoopen,"r")
        codeeditor.delete("1.0",END)
        codeeditor.insert(INSERT,f.read())
        current_file.set(os.path.realpath(filetoopen))
        file_opened = True
        project_opened = False
        f.close()
        log("FILE OPENED SUCCESSFULLY!!!")

def savefileas():
    global file_opened
    saveas = filedialog.asksaveasfilename(title = language_strings[87],initialdir = "C:/",filetypes = (("Lua file","*.lua"),("Scrupp Lua file","*.slua"),("MoonScript file","*.moon"),("Other file types","*.*")))
    if saveas:
        log("SAVING FILE...")
        f = open(saveas,"w+")
        f.truncate(0)
        f.write(codeeditor.get("1.0",END))
        f.close()
        current_file.set(os.path.realpath(saveas))
        file_opened = True
        project_opened = False
        log("FILE SAVED SUCCESSFULLY!!!")
        
def savefile():
    global file_opened
    if file_opened and os.path.isfile(os.path.realpath(current_file.get())):
        log("SAVING FILE...")
        f = open(os.path.realpath(current_file.get()),"w+")
        f.truncate(0)
        f.write(codeeditor.get("1.0",END))
        f.close()
        log("FILE SAVED SUCCESSFULLY!!!")
    else:
        savefileas()

def closefile():
    global file_opened
    if file_opened:
        log("CLOSING FILE...")
        savefile()
        codeeditor.delete("1.0",END)
        current_file.set(language_strings[65])
        refresh()
        file_opened = False
        project_opened = False
        log("FILE CLOSED SUCCESSFULLY!!!")

def obfuscatefile():
    log("OBFUSCATING FILE...")
    savefile()
    os.system(os.path.realpath(os.path.join("resources/packages/","obfuscate_lua_file.bat")) + " " + os.path.realpath(current_file.get()))
    log("FILE OBFUSCATED SUCCESSFULLY!!!")

def decompilefile():
    log("DECOMPILING FILE...")
    savefile()
    os.system(os.path.realpath(os.path.join("resources/packages/","decompile_lua_file_bytecode.bat")) + " " + os.path.realpath(current_file.get()))
    log("FILE DECOMPILED SUCCESSFULLY!!!")

def disasmfile():
    log("DISASSEMBLING FILE...")
    savefile()
    os.system(os.path.realpath(os.path.join("resources/packages/","disassembly_lua_file.bat")) + " " + os.path.realpath(current_file.get()))
    log("FILE DISASSEMBLED SUCCESSFULLY!!!")

def deletefile():
    global file_opened
    if file_opened:
        deletefile = messagebox.askyesno(title = language_strings[84],message = language_strings[85])
        if deletefile:
            log("DELETING FILE...")
            os.system("erase " + os.path.realpath(current_file.get()))
            closefile()
            log("FILE DELETED SUCCESSFULLY!!!")

def newfile():
    log("LOADING FILE WIZARD...")
    createfilewindow = Toplevel(tkinter)
    filedir = StringVar()
    fname = StringVar()
    filedir.set("C:/")
    createfilewindow.title(language_strings[78])
    createfilewindow.geometry(("%dx%d+%d+%d") % (480,140,createfilewindow.winfo_screenwidth() / 3,createfilewindow.winfo_screenheight() / 3))
    createfilewindow.resizable(False,False)
    createfilewindow.iconphoto(False,PhotoImage(file = "resources/images/lotus_icon.png"))
    filename = Label(createfilewindow,text = language_strings[79]) 
    filenameentry = Entry(createfilewindow,width = 58,textvariable = fname)
    filename.place(x = 5,y = 10)
    filenameentry.place(x = 110,y = 10)
    filedirectory = Label(createfilewindow,text = language_strings[80]) 
    filedirectoryentry = Entry(createfilewindow,width = 58,textvariable = filedir)
    filedirectory.place(x = 5,y = 40)
    filedirectoryentry.place(x = 110,y = 40)
    
    def setupfile():
        log("CREATING FILE...")
        global file_opened
        global project_opened
        global fileext
        closeproject()
        closefile()
        if filetypes.get() == "Lua file":
            fileext = ".lua"
        if filetypes.get() == "Scrupp Lua file":
            fileext = ".slua"
        if filetypes.get() == "MoonScript file":
            fileext = ".moon"
        if not os.path.exists(os.path.realpath(filedir.get())):
            os.mkdir(os.path.realpath(filedir.get()))
        f = open(os.path.join(filedir.get(),str(fname.get() + fileext)),"w+")
        file_opened = True
        codeeditor.delete("1.0",END)
        codeeditor.insert(INSERT,f.read())
        current_file.set(os.path.join(filedir.get(),str(fname.get() + fileext)))
        f.close()
        createfilewindow.destroy()
        log("FILE CREATED SUCCESSFULLY!!!")        
    log("FILE WIZARD CREATED SUCCESSFULLY!!!")
            
    # Buttons and Combobox
    createfilebutton = Button(createfilewindow,text = language_strings[81],command = setupfile)
    cancelfilebutton = Button(createfilewindow,text = language_strings[82],command = createfilewindow.destroy)
    createfilebutton.place(x = 315,y = 105)
    cancelfilebutton.place(x = 415,y = 105)
    filetype = Label(createfilewindow,text = language_strings[83])
    filetype.place(x = 5,y = 70)
    filetypes = ttk.Combobox(createfilewindow,width = 55)

    # Project types
    filetypes["values"] = ( "Lua file",
                            "Scrupp Lua file",
                            "MoonScript file" )
    
    filetypes.place(x = 110,y = 70)
    filetypes.current(0)
    createfilewindow.mainloop()

def fixpackages():
    log("REINSTALLING PACKAGES...")
    # The same way when first time you open Lotus IDE,But without checking packages directory
    log("SEARCHING FOR PACKAGES ARCHIVE...")
    if os.path.exists("resources/inbound/packages.zip") and os.path.isfile("resources/inbound/packages.zip"):
        with ZipFile("resources/inbound/packages.zip", "r") as content:
            log("UPDATING IDE PACKAGES...")
            content.extractall("resources/packages")
    elif not os.path.exists("resources/inbound/packages.zip") and not os.path.exists("resources/inbound"):
        log("ERROR: PACKAGES ARCHIVE NOT FOUND!!!")
        close()

    # Show message that packages reinstalled
    messagebox.showinfo(language_strings[88],language_strings[89])
    log("PACKAGES REINSTALLED SUCCESSFULLY!!!")

def runbydefault():
    global file_opened
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if file_opened:
        savefile()
        log("COMPILING CODE...")
        log("RUNNING CODE...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " 1")
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " 1")
        log("CODE RUNNED SUCCESSFULLY!!!")
    elif project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("RUNNING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 1")
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 1")
        log("PROJECT RUNNED SUCCESSFULLY!!!")
    else:
        messagebox.showerror(language_strings[90],language_strings[91])
        
def runbyjit():
    global file_opened
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if file_opened:
        savefile()
        log("COMPILING CODE...")
        log("RUNNING CODE...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " 2")
        if fx == ".moon": 
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " " + os.path.splitext(os.path.realpath(current_file.get()))[0] + ".lua" + " 4")
        log("CODE RUNNED SUCCESSFULLY!!!")
    elif project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("RUNNING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 2")
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 3")
        log("PROJECT RUNNED SUCCESSFULLY!!!")
    else:
        messagebox.showerror(language_strings[90],language_strings[91])

def runbylove():
    global file_opened
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if file_opened:
        savefile()
        log("COMPILING CODE...")
        log("RUNNING CODE...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " 3")
        if fx == ".moon": 
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " " + os.path.splitext(os.path.realpath(current_file.get()))[0] + ".lua" + " 2")
        log("CODE RUNNED SUCCESSFULLY!!!")
    elif project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("RUNNING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 4")
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 4")
        log("PROJECT RUNNED SUCCESSFULLY!!!")
    else:
        messagebox.showerror(language_strings[90],language_strings[91])

def runbylovr():
    global file_opened
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if file_opened:
        savefile()
        log("COMPILING CODE...")
        log("RUNNING CODE...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " 3")
        if fx == ".moon": 
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " " + os.path.splitext(os.path.realpath(current_file.get()))[0] + ".lua" + " 3")
        log("CODE RUNNED SUCCESSFULLY!!!")
    elif project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("RUNNING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 3")
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 5")
        log("PROJECT RUNNED SUCCESSFULLY!!!")
    else:
        messagebox.showerror(language_strings[90],language_strings[91])

def runbyamulet():
    global file_opened
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if file_opened:
        savefile()
        log("COMPILING CODE...")
        log("RUNNING CODE...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " 5")
        if fx == ".moon": 
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " " + os.path.splitext(os.path.realpath(current_file.get()))[0] + ".lua" + " 5")
        log("CODE RUNNED SUCCESSFULLY!!!")
    elif project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("RUNNING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 5")
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","run_moonscript_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 6")
        log("PROJECT RUNNED SUCCESSFULLY!!!")
    else:
        messagebox.showerror(language_strings[90],language_strings[91])

def runbyscrupp():
    global file_opened
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if file_opened:
        savefile()
        log("COMPILING CODE...")
        log("RUNNING CODE...")
        if fx == ".slua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " 6")
        else:
            messagebox.showerror(language_strings[92],language_strings[93])
        log("CODE RUNNED SUCCESSFULLY!!!")
    elif project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("RUNNING PROJECT...")
        if fx == ".slua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 6")
        else:
            messagebox.showerror(language_strings[92],language_strings[93])
        log("PROJECT RUNNED SUCCESSFULLY!!!")
    else:
        messagebox.showerror(language_strings[90],language_strings[91])

def runbyraylib():
    global file_opened
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if file_opened:
        savefile()
        log("COMPILING CODE...")
        log("RUNNING CODE...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_file.bat")) + " " + pathquote(os.path.realpath(current_file.get())) + " 7")
    elif project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("RUNNING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","run_lua_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 7")
    else:
        messagebox.showerror(language_strings[90],language_strings[91])
        
        
def runbybrowser():
    global file_opened
    global file_opened
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if file_opened and fx == ".lua":
        log("DEPLOYING TO HTML5...")
        copyfile(os.path.realpath("resources/packages/web/fengari-web.js"),os.path.join(pathquote(os.path.realpath(path.parents[0])),"fengari-web.js"))
        f = open(os.path.join(os.path.realpath(path.parents[0]),"index.html"),"w+")
        f.truncate(0)
        f.write("<!DOCTYPE html>\n<html>\n<head>\n" + "<script src=" + '"{}"'.format("fengari-web.js") + "></script>\n<title>" + os.path.realpath(os.path.basename(path.parents[0])) + "</title>\n</head>\n" +  "<script type=" + '"{}"'.format("application/lua") + ">\n" + codeeditor.get("1.0",END) + "</script>\n" + "\n<body>\n</body></html>")
        f.close()
        log("RUNNING IN BROWSER...")
        webbrowser.open_new_tab(os.path.realpath(os.path.join(path.parents[0],"index.html")))
        log("CODE RUNNED SUCCESSFULLY!!!")
    else:
        messagebox.showwarning(language_strings[94],language_strings[95])

# Build functions section
def buildproject():
    global project_opened
    global file_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("BUILDING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","build_lua_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])))
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","build_moonscript_project.bat")) + " " + pathquote(os.path.realpath(path.parents[0])))
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        log("PROJECT BUILT SUCCESSFULLY!!!")
    elif file_opened:
        messagebox.showerror(language_strings[90],language_strings[91])
        
def buildwithlove():
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("BUILDING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","build_lua_game.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 1")
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","build_moonscript_game.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 1")
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        log("PROJECT BUILT SUCCESSFULLY!!!")
    elif file_opened:
        messagebox.showerror(language_strings[96],language_strings[97])

def buildwithlovr():
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("BUILDING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","build_lua_game.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 2")
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","build_moonscript_game.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 2")
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        log("PROJECT BUILT SUCCESSFULLY!!!")
    elif file_opened:
        messagebox.showerror(language_strings[96],language_strings[97])

def buildwithamulet():
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("BUILDING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","build_lua_game.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 3")
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        if fx == ".moon":
            os.system("start " + os.path.realpath(os.path.join("resources/packages/","build_moonscript_game.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 3")
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        log("PROJECT BUILT SUCCESSFULLY!!!")
    elif file_opened:
        messagebox.showerror(language_strings[96],language_strings[97])

def buildwithscrupp():
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("BUILDING PROJECT...")
        if fx == ".slua":
            os.system(os.path.realpath(os.path.join("resources/packages/","build_lua_game.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 4")
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        elif fx == ".moon" or fx == ".lua":
            messagebox.showerror(language_strings[94],language_strings[95])
        log("PROJECT BUILT SUCCESSFULLY!!!")
    elif file_opened:
        messagebox.showerror(language_strings[96],language_strings[97])

def buildwithraylib():
    global project_opened
    path = Path(current_file.get())
    f,fx = os.path.splitext(path)
    if project_opened:
        saveproject()
        log("COMPILING PROJECT...")
        log("BUILDING PROJECT...")
        if fx == ".lua":
            os.system(os.path.realpath(os.path.join("resources/packages/","build_lua_game.bat")) + " " + pathquote(os.path.realpath(path.parents[0])) + " 5")
            os.startfile(pathquote(os.path.join(os.path.realpath(path.parents[0]),"build")))
        elif fx == ".moon" or fx == ".slua":
            messagebox.showerror(language_strings[94],language_strings[95])
        log("PROJECT BUILT SUCCESSFULLY!!!")
        
# Documentations functions section
def luadocs():
    if os.path.exists("docs") and not os.path.isfile("docs"):
        log("OPENING DOCUMENTATION...")
        if os.path.exists("docs/lua"):
            webbrowser.open_new_tab(os.path.join(os.path.realpath("docs/lua"),"lua53ref.html"))
            log("DOCUMENTATION OPENED SUCCESSFULLY!!!")

def luajitdocs():
    log("OPENING DOCUMENTATION...")
    webbrowser.open_new_tab("https://luajit.org/extensions.html")
    log("DOCUMENTATION OPENED SUCCESSFULLY!!!")

def moonscriptdocs():
    log("OPENING DOCUMENTATION...")
    webbrowser.open_new_tab("https://moonscript.org/reference")
    log("DOCUMENTATION OPENED SUCCESSFULLY!!!")

def lovedocs():
    if os.path.exists("docs") and not os.path.isfile("docs"):
        log("OPENING DOCUMENTATION...")
        if os.path.exists("docs/love"):
            webbrowser.open_new_tab(os.path.join(os.path.realpath("docs/love"),"LÖVE 11.3 Reference.html"))
            log("DOCUMENTATION OPENED SUCCESSFULLY!!!")

def lovrdocs():
    log("OPENING DOCUMENTATION...")
    webbrowser.open_new_tab("https://lovr.org/docs")
    log("DOCUMENTATION OPENED SUCCESSFULLY!!!")
    

def amuletdocs():
    if os.path.exists("docs") and not os.path.isfile("docs"):
        log("OPENING DOCUMENTATION...")
        if os.path.exists("docs/amulet"):
            webbrowser.open_new_tab(os.path.join(os.path.realpath("docs/amulet"),"Amulet Manual.html"))
            log("DOCUMENTATION OPENED SUCCESSFULLY!!!")

def scruppdocs():
    if os.path.exists("docs") and not os.path.isfile("docs"):
        log("OPENING DOCUMENTATION...")
        if os.path.exists("docs/scrupp"):
            webbrowser.open_new_tab(os.path.join(os.path.realpath("docs/scrupp"),"Scrupp SVN Manual.html"))
            log("DOCUMENTATION OPENED SUCCESSFULLY!!!")

def fengaridocs():
    log("OPENING DOCUMENTATION...")
    webbrowser.open_new_tab("https://fengari.io")
    log("DOCUMENTATION OPENED SUCCESSFULLY!!!")

def raylibdocs():
    log("OPENING DOCUMENTATION...")
    if os.path.exists("docs/raylib"):
        webbrowser.open_new_tab(os.path.join(os.path.realpath("docs/raylib"),"raylib_cheatsheet.html"))
        log("DOCUMENTATION OPENED SUCCESSFULLY!!!")


# Music player,To have fun while coding
def musicplayer():
    log("LAUNCHING MUSIC PLAYER...")
    os.system("switch.bat 6")
    log("MUSIC PLAYER LAUNCHED SUCCESSFULLY!!!")

def faq():
    log("OPENING FAQ PAGE...")
    webbrowswer.open_new_tab("https://github.com/Cake-Engine/Documentation/blob/master/FAQ.md")
    
def lotuswiki():
    log("OPENING WIKI...")
    webbrowser.open_new_tab("https://github.com/Rabios/Lotus/wiki")
    log("WIKI OPENED SUCCESSFULLY!!!")

def support():
    log("OPENING SUPPORT PAGE...")
    webbrowser.open_new_tab("https://github.com/Rabios/Lotus/issues")

def submitissue():
    log("GOING TO SUBMITTING ISSUE ON GITHUB...")
    webbrowser.open_new_tab("https://github.com/Rabios/Lotus/issues/new/choose")

# Main code    
log("IDE STARTED...")        
log("IDE LAUNCHED SUCCESSFULLY!!!")
tkinter = tk.Tk()

# Check contents before starting...
# Mainly,Lotus uses tkinter and Pillow and some main python modules as part of it
# NOTES: Unfortunately,Lotus only supports 64-bit versions of Microsoft Windows,Cause of some game engines binaries that is for 64-bit
os.system("mkdir projects") # Hack in case projects folder not found
os.system("mkdir resources\cache")
contents_existed = (os.path.exists("resources/images") and os.path.exists("resources/inbound") and os.path.exists("docs") and os.path.exists("resources/themes"))
win64 = os.environ["PROGRAMFILES(X86)"]
        
# IDE Window
log("INITIALIZING IDE WINDOW...") 
tkinter.geometry("%dx%d" % (tkinter.winfo_screenwidth(),tkinter.winfo_screenheight()))
tkinter.resizable(False, False)
tkinter.attributes("-fullscreen",True)
tkinter.title("Lotus IDE")
log("IDE WINDOW INITIALIZED SUCCESSFULLY!!!")

# Window GUI
log("LOADING WINDOW GUI...")

# Menus
log("LOADING IDE WINDOW MENUS...")
menus = Menu(tkinter)
tkinter.config(menu = menus)

# Removed tearoff,Of course
log("CREATING MENUS...")
projectmenu = Menu(menus,tearoff = False)
filemenu = Menu(menus,tearoff = False)
runmenu = Menu(menus,tearoff = False)
buildmenu = Menu(menus,tearoff = False)
toolsmenu = Menu(menus,tearoff = False)
settingsmenu = Menu(menus,tearoff = False)
helpmenu = Menu(menus,tearoff = False)
docsmenu = Menu(menus,tearoff = False)
moremenu = Menu(menus,tearoff = False)
windowmenu = Menu(menus,tearoff = False)

# Labels
menus.add_cascade(label = language_strings[0],menu = projectmenu)
menus.add_cascade(label = language_strings[1],menu = filemenu)
menus.add_cascade(label = language_strings[2],menu = runmenu)
menus.add_cascade(label = language_strings[3],menu = buildmenu)
menus.add_cascade(label = language_strings[4],menu = toolsmenu)
menus.add_cascade(label = language_strings[5],menu = settingsmenu)
menus.add_cascade(label = language_strings[6],menu = helpmenu)
menus.add_cascade(label = language_strings[7],menu = docsmenu)
menus.add_cascade(label = language_strings[8],menu = moremenu)
menus.add_cascade(label = language_strings[9],menu = windowmenu)

# Menus commands
# Project menu commands
projectmenu.add_command(label = language_strings[10],command = newproject)
projectmenu.add_command(label = language_strings[11],command = openproject)
projectmenu.add_command(label = language_strings[12],command = saveproject)
projectmenu.add_command(label = language_strings[13],command = addfilestoproject)
projectmenu.add_command(label = language_strings[96],command = addfoldertoproject)
projectmenu.add_command(label = language_strings[14],command = projectexplorer)
projectmenu.add_command(label = language_strings[15],command = closeproject)
projectmenu.add_command(label = language_strings[16],command = cleanproject)
projectmenu.add_command(label = language_strings[17],command = deleteproject)

# File menu commands
filemenu.add_command(label = language_strings[18],command = newfile)
filemenu.add_command(label = language_strings[19],command = openfile)
filemenu.add_command(label = language_strings[20],command = savefile)
filemenu.add_command(label = language_strings[21],command = savefileas)
filemenu.add_command(label = language_strings[22],command = closefile)
filemenu.add_command(label = language_strings[23],command = deletefile)

# Run menu commands
runmenu.add_command(label = language_strings[24],command = runbydefault)
runmenu.add_command(label = language_strings[25],command = runbyjit)
runmenu.add_command(label = language_strings[26],command = runbylove)
runmenu.add_command(label = language_strings[27],command = runbylovr)
runmenu.add_command(label = language_strings[28],command = runbyamulet)
runmenu.add_command(label = language_strings[29],command = runbyscrupp)
runmenu.add_command(label = language_strings[106],command = runbyraylib)
runmenu.add_command(label = language_strings[30],command = runbybrowser)

# Build (Compile and export as executable) menu commands
buildmenu.add_command(label = language_strings[31],command = buildproject)
buildmenu.add_command(label = language_strings[32],command = buildwithlove)
buildmenu.add_command(label = language_strings[33],command = buildwithlovr)
buildmenu.add_command(label = language_strings[34],command = buildwithamulet)
buildmenu.add_command(label = language_strings[35],command = buildwithscrupp)
buildmenu.add_command(label = language_strings[107],command = buildwithraylib)
    
# Tools menu commands
toolsmenu.add_command(label = language_strings[38],command = openexec)
toolsmenu.add_command(label = language_strings[39],command = luacmd)
toolsmenu.add_command(label = language_strings[40],command = luajit)
toolsmenu.add_command(label = language_strings[41],command = cmd)
toolsmenu.add_command(label = language_strings[42],command = musicplayer)
toolsmenu.add_command(label = language_strings[43],command = getlog)

# Settings menu commands
settingsmenu.add_command(label = language_strings[44],command = fixpackages)
settingsmenu.add_command(label = language_strings[45],command = clear_log)
settingsmenu.add_command(label = language_strings[46],command = restart)

# Help menu commands
helpmenu.add_command(label = language_strings[47],command = lotuswiki)
helpmenu.add_command(label = language_strings[48],command = faq)
helpmenu.add_command(label = language_strings[49],command = support)
helpmenu.add_command(label = language_strings[50],command = submitissue)

# Documentations menu commands
docsmenu.add_command(label = language_strings[51],command = luadocs)
docsmenu.add_command(label = language_strings[52],command = luajitdocs)
docsmenu.add_command(label = language_strings[53],command = moonscriptdocs)
docsmenu.add_command(label = language_strings[54],command = lovedocs)
docsmenu.add_command(label = language_strings[55],command = lovrdocs)
docsmenu.add_command(label = language_strings[56],command = amuletdocs)
docsmenu.add_command(label = language_strings[57],command = scruppdocs)
docsmenu.add_command(label = language_strings[58],command = fengaridocs)
docsmenu.add_command(label = language_strings[108],command = raylibdocs)

# More menu commands
moremenu.add_command(label = language_strings[59],command = about)
moremenu.add_command(label = language_strings[60],command = source)
moremenu.add_command(label = language_strings[61],command = letter)

# Window menu commands
windowmenu.add_command(label = language_strings[62],command = enable_fullscreen)
windowmenu.add_command(label = language_strings[63],command = exit_fullscreen)
windowmenu.add_command(label = language_strings[64],command = close)

log("MENUS CREATED SUCCESSFULLY!!!")
current_file = StringVar()
if file == "":
    current_file.set(language_strings[65])
    
# Filename label
filename_label = Label(tkinter,textvariable = current_file,background = theme_strings[2],foreground = theme_strings[3]) 
filename_label.pack()

# Code editor
log("LOADING CODE EDITOR...")

# Use CustomText and LineNumbers class with Scrollbar widget
codeeditor = CustomText(tkinter,background = theme_strings[0])
codeeditor.configure(wrap = "none",font = ("Lucida Console", "12"))
linenumbers = TextLineNumbers(tkinter, width = 50)
linenumbers.attach(codeeditor)

# Snippets window
log("LOADING SNIPPETS WINDOW...")
snippets_listbox = Listbox(tkinter,width = 1)
vertical_scrollbar1 = Scrollbar(orient = "vertical", command = codeeditor.yview)
vertical_scrollbar2 = Scrollbar(orient = "vertical",command = snippets_listbox.yview)
horizontal_scrollbar1 = Scrollbar(orient = "horizontal",command = codeeditor.xview)
horizontal_scrollbar2 = Scrollbar(orient = "horizontal",command = snippets_listbox.xview)
codeeditor.configure(yscrollcommand = vertical_scrollbar1.set,xscrollcommand = horizontal_scrollbar1.set)
snippets_listbox.configure(yscrollcommand = vertical_scrollbar2.set,xscrollcommand = horizontal_scrollbar2.set)

for items in snippets_list:
    snippets_listbox.insert(END,items)

def insert_selected(e):
    w = e.widget
    selected = w.curselection()
    picked = w.get(selected[1 - 1])
    log("PASTING SNIPPET INTO EDITOR...")
    codeeditor.insert(INSERT,picked)
    log("SNIPPED PASTED INTO EDITOR SUCCESSFULLY!!!")

# Pack all parts
vertical_scrollbar1.pack(side = "right", fill = "y")
vertical_scrollbar2.pack(side = "right",fill = "y")
horizontal_scrollbar1.pack(side = "bottom",fill = "x")
horizontal_scrollbar2.pack(side = "bottom",fill = "x")
linenumbers.pack(side = "left", fill = "y")
codeeditor.pack(side = "left", fill = "both", expand = True)
snippets_listbox.pack(side = "right",fill = "both",expand = True)
snippets_listbox.pack(expand = True,fill = "both")
log("CODE EDITOR LOADED SUCCESSFULLY!!!")
log("SNIPPETS WINDOW LOADED SUCCESSFULLY!!!")

# On change
def sen(*args):
    linenumbers.redraw(*args)
    
codeeditor.bind("<<Change>>", sen)
codeeditor.bind("<Configure>", sen)
snippets_listbox.bind('<<ListboxSelect>>',insert_selected)

# Syntax highlighting with pygments
# NOTES: Syntax highlighting takes words to highlight from snippets list
def tag(*args):
    def color(word, color):
        index = []
        index1 = codeeditor.search(word, "1.0", "end")
        while index1:
            index2 = ".".join([index1.split(".")[0], str(int(index1.split(".")[1]) + len(word))])
            index.append((index1, index2))
            index1 = codeeditor.search(word, index2, "end")
        for i, j in index:
            codeeditor.tag_add(word, i, j)
            codeeditor.tag_configure(word, foreground = color)

    for token, content in lex(codeeditor.get("1.0", "end"), LuaLexer()):
        if token == Token.Literal.Number.Integer or token == Token.Literal.Number.Float or token == Token.Literal.Number.Hex:
            color(content,color = theme_strings[4])
        elif token == Token.Operator:
            color(content,color = theme_strings[5])
        elif token == Token.Comment.Single or token == Token.Comment.Multiline or token == Token.Comment.Special:
            color(content,color = theme_strings[6])
        elif token == Token.Punctuation:
            color(content,color = theme_strings[7])
        elif token == Token.Name.Function or token == Token.Name.Class or token == Token.Variable.Class:
            color(content,color = theme_strings[8])

# The new highlighter,DO NOT DELETE THE OLD cause merged with the new one
# All fixed up
def colorize(*args):
    global count
    row1, col1 = args[0].start
    row1, col1 = str(row1), str(col1)
    row2, col2 = args[0].end
    row2, col2 = str(row2), str(col2)
    start = ".".join((row1, col1))
    end = ".".join((row2, col2))
    codeeditor.tag_add(str(count), start, end)
    try:
        codeeditor.tag_config(str(count), foreground = args[1])
    except IndexError:
        codeeditor.tag_config(str(count), foreground = args[1])
    count += 1

def search(event):
    try:
        for i in tokenize.tokenize(io.BytesIO(codeeditor.get("1.0", "end").encode("utf-8")).readline):
            if i.type == 1:
                if i.string in snippets_list:
                    colorize(i, theme_strings[9])
            elif i.type == 2:
                colorize(i, theme_strings[10])
            elif i.type == 3:
                colorize(i, theme_strings[11])
    except tokenize.TokenError:
        pass
        tag()
    tag()
          
# Check OS and contents existing
log("CHECKING SUPPORT...")
if not win64 and contents_existed:
    log("ERROR: NOT x64 MACHINE!!!")
    close()

# Load packages
if contents_existed:
    # Window icon
    log("LOADING WINDOW ICON...") 
    tkinter.iconphoto(False,PhotoImage(file = "resources/images/lotus_icon.png"))
    
    # Finding compressed packages file then extract it
    log("SEARCHING FOR PACKAGES ARCHIVE...")
    if os.path.exists("resources/inbound/packages.zip") and os.path.isfile("resources/inbound/packages.zip") and not os.path.exists("resources/packages"):
        with ZipFile("resources/inbound/packages.zip", "r") as content:
            log("UPDATING IDE PACKAGES...")
            content.extractall("resources/packages")
    elif os.path.exists("resources/packages"):
        log("PACKAGES INSTALLED BEFORE!!!")
    else:
        log("ERROR: PACKAGES ARCHIVE NOT FOUND!!!")
        close()

codeeditor.bind("<KeyRelease>", search)
tkinter.mainloop()
