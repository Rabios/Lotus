# Lotus
Lotus is an Open-Source,Moddable,Freeware Lua and MoonScript IDE,Aimed towards software and game development and also for basic needs

Lotus developed entirely 11 days,11 Days of the hard work.

## Features
- Lightweight,Fast as lightning
- Simple and easy to understand,Comes with user-friendly GUI
- Scriptable and moddable,Written fully in Python 3 and Batchscript
- Fully free,No payments,No purchases
- Great for game and software development
- Comes with all needs to install (download and install packages and docs needed to run from source,See below)
- Comes with music player to have fun while coding
- Build and run projects and files fast as light!!!
- Comes with tools to disassembly,decompile,And obfuscate projects and files
- Ability to customize themes

## How to run from source
- Download and install both 64-bit versions of Python 3 and 7zip
- Download this repository as ZIP
- Extract it anywhere
- Create folder named `projects` in the directory you extracted the repository,Leave it empty
- Download documentations from [here](https://drive.google.com/uc?export=download&id=172GwQz75SoVWHgGxI8F00T-jj6tpioiR)
- Extract documentations archive in the directory you extracted the repository,Once a folder named `docs` appears,Go next step
- Download packages archive [here](https://drive.google.com/uc?export=download&id=1dIUchwWa85p49pTk_IvsgbU1sXJ8RgAI)
- When packages archive downloaded,Create folder named `inbound` inside `resources` folder (Inside repository extracted folder),And move downloaded packages archive to it
- Create folder named `cache` inside `resources` folder,But keep it empty
- Get back to the repository folder,Run `install_dependencies.bat` if you installed Python 3 and 7zip
- Run `launch.bat`,And check that you have installed Python 3 and 7zip
- As the first startup for Lotus IDE,It will extract packages archive so first startup may take minutes
- That's all,I know i know these are very long steps but i promise that they are working %100

> If you don't want to do all that instead,Download installer it from [releases](https://github.com/Rabios/Lotus/releases),It will come with 7zip and python and everything

> NOTES: Even if you're running Lotus IDE from source,To start IDE run `launch.bat`

## Requirements
- Microsoft Windows 7 and above,64-bit ONLY!!!
- 600 MB of available storage
- 4GB or more RAM

> NOTES: Until now and unfortunately,Lotus IDE Not supported on Linux and Mac

## Credits
- [Rabia Alhaffar](https://github.com/Rabios),The main developer of Lotus IDE

## Third party used
- Runtime
  - [Python](https://www.python.org)
  - [7zip](https://www.7-zip.org)
  
- Python modules used and dependencies
  - [tkinter](https://docs.python.org/3/library/tkinter.html)
  - [tkinter.tix](https://docs.python.org/3/library/tkinter.tix.html)
  - [tkinter.ttk](https://docs.python.org/3/library/tkinter.ttk.html)
  - [pygments](https://pygments.org)
  - [pynput](https://pypi.org/project/pynput)
  - [playsound](https://pypi.org/project/playsound)
  - [Pillow](https://pillow.readthedocs.io/en/stable)
  - [webbrowser](https://docs.python.org/3.8/library/webbrowser.html)
  - [os](https://docs.python.org/3.8/library/os.html)
  - [sys](https://docs.python.org/3.8/library/sys.html)
  - [zipfile](https://docs.python.org/3.8/library/zipfile.html)
  - [datetime](https://docs.python.org/3.8/library/datetime.html)
  - [shutil](https://docs.python.org/3.8/library/shutil.html)
  - [pathlib](https://docs.python.org/3.8/library/pathlib.html)
  - [tokenize](https://docs.python.org/3.8/library/tokenize.html)
  - [io](https://docs.python.org/3.8/library/io.html)
  - [keyword](https://docs.python.org/3.8/library/keyword.html)
  
- Lua compilers and tools
  - [Lua](https://www.lua.org)
  - [LuaJIT](https://luajit.org)
  - [MoonScript](https://moonscript.org)
  - [LuaForWindows](https://github.com/rjpcomputing/luaforwindows)
  - [Luarocks](https://luarocks.org)
 
- Game engines/frameworks/libraries
  - [LOVE](https://love2d.org)
  - [LOVR](https://lovr.org)
  - [Amulet](https://www.amulet.xyz)
  - [Scrupp](http://scrupp.sourceforge.net)
  - [Raylib](http://raylib.com)
 
> NOTES: All third party softwares used comes with their licenses

> NOTES: Cause of using pygments,The IDE may get slow and face some lags in some cases

## License
Lotus IDE Licensed under MIT License,Following all the third parties that used by Lotus IDE itself

## Documentation
- [FAQ](https://github.com/Rabios/Lotus/blob/master/FAQ.md)
- [How to add snippets to Lotus IDE](https://github.com/Rabios/Lotus/blob/master/Snippets.md)
- [How to translate Lotus IDE](https://github.com/Rabios/Lotus/blob/master/Translate.md)
