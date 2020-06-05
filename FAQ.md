# FAQ

## Does Lotus IDE runs on 32-bit devices?
NO,Only 64-bit!!!

## Is Lotus IDE cross-platform?
Until now,It's only supports Microsoft Windows 7 and up,Sorry there is no Linux and Mac support,But you can help us by porting project to Linux and Mac if you can

## Does Lotus IDE takes huge size?
NO,Only over 180 MB the installer size,But at launch it extracts packages (This only occurs first time),So his size become over 500 MB

## Why source code not bundled as executable,Even installer installs source?
To provide ability to modify,But as normal user install all needs (Just run `install_requirements.bat` for the first time) and then run `launch.bat` to start IDE everytime

Else if you are run from source,Use `install_dependencies.bat` instead of `install_requirements.bat` for the first time then run `launch.bat` to start IDE everytime

## Why highlighting has parsing problems?
That caused by pygments and the somehow highlighting code system,Help us and fix it if you want

## Why there is no themes?
I'm working on that feature,It's not hard so i promise i'll add that

## Why there is no autocompletion?
The implementation of it is somehow hard especially when it comes to tkinter,So that's why i added snippets box at the right side of the IDE

> NOTES: You can add your line of code as snippet,Check [here](https://github.com/Rabios/Lotus/blob/master/Snippets.md) to know how to create snippets

## Isn't there is translations?
NO,But you can create one so if you would see [here](https://github.com/Rabios/Lotus/blob/master/Translate.md)

## Won't Lotus IDE eat my RAM memory?
I think you are asking about visual studio not Lotus IDE,right? OK,Lotus IDE designed to run from source code,And it has very powerful debugging,Of course it will not take RAM,I sway!!!
