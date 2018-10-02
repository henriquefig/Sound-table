# Sound table
## Introduction

This is small project to make a digital sound table (a "table" that plays pre-recorded sounds in a loop, used by DJs or enthusiasts).
I'm very new to python, so there could be some glaring mistakes (e.g. the overuse of global variables), feel free to commit pull requests if you think you got a better solution!

<!-- [START getstarted] -->
## Getting Started

### Installation

To use Sound-table you will need python 3.x (the project was developed with python 3.7)
and the following modules:

**Wave** - to read and write .wav files with help of Pyaudio

**Tkinter** - to load all the graphical contents

**Pyaudio** - to read and write .wav files with help of Wave


```bash
pip3 install wave
pip3 install tkinter
pip3 install pyaudio
```

**Note:** Again, I'm a begginner in python so there's a possibility that only Wave or Pyaudio modules are need (feel free to make a pull request ^^).

### Usage

Just run the script in a command line:

```bash
python3 soundtable.py
```

A window should be launched and you can see the program for yourself. Blue means the button is not active, red means it's active, the program will not allow you to start the loop with no sounds selected (even though the background beat will be loaded already).

**Note 1:** The sounds are not pre-recorded, only the beat (which is a knock on wood), if try to use a button that doesn't have a recorded sound the program will crash. To record/assign a sound to a button, right-click it for the duration of the sound you wish to record.

**Note 2:** The BPMs functionality is very shaky (specially because I'm not using threads), and as such, a big amount of sounds selected might fall out of the choosen BPMs. Also a higher BPMs can cause the program to cut your pre-recorded sound half way through.

**Note 3:** There is something you might find odd, which is why use "highlightbackground" to color the buttons. Well this a Mac OS specific problem, and seeing I'm working on one, for my sake, this option was adopted, feel free to change it if you use a Windows/Linux.
