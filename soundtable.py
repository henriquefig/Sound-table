import wave
import pyaudio
from tkinter import *
import time

#number of possible sounds, rows*cols
rows = 10
cols = 10
SoundMatrix = []
# This function defines the limits for the tempo used (a value above 200 simply does not make a difference)
def limit_bpms(* args):
	global bpms
	print(bpms.get())
	if int(bpms.get()) < 20:
		bpms.set(20)
	if int(bpms.get()) > 200:
		bpms.set(200)

# This funciton is the main one for playing the sound loop.
# It is kinda strangly written, but what it does is take a background sound, and take all the sounds selected (stored in the argument path)
# Then for each chunk of each sound play it sequencial (this is done to mix the sounds without using a bunch load of threads, also threads and tkinter do not combine very well in my experience)
def playsound(path,a):
	#define stream chunk   
	chunk = 1024
	stream = []
	readable = []
	for i in path:
		new = str(i)+".wav"
		#open a wav format music  
		f = wave.open(new,"rb")  
		#instantiate PyAudio  
		p = pyaudio.PyAudio()  
		#open stream  
		stream.append(p.open(format = p.get_format_from_width(f.getsampwidth()),  
		                channels = f.getnchannels(),  
		                rate = f.getframerate(),  
		                output = True))
		readable.append(f)

	background = "beat.wav"
	b = wave.open(background,"rb")
	p = pyaudio.PyAudio()
	backstream = p.open(format = p.get_format_from_width(b.getsampwidth()),
					channels = b.getnchannels(),
					rate = b.getframerate(),
					output = True)
	aux = readable[0].readframes(chunk)
	stream[0].write(aux)
	counter = 0
	now = time.time()
	start = now
	while aux:
		a.update_idletasks()
		a.update()
		#check for a minute/bpms have passed
		if (now-start) >= 60/bpms.get():
			break
		metronome = b.readframes(chunk)
		backstream.write(metronome)
		for i in readable:
			aux = i.readframes(chunk)
			stream[counter].write(aux)
			counter += 1
		counter=0
		now = time.time()

	for s in stream:
		#stop streams  
		s.stop_stream()  
		s.close()  

	backstream.stop_stream()
	backstream.close()
	#close PyAudio  
	p.terminate()  

# This function is activated with the right click and will replace the current sound of the clicked button for a new one
# This function does not terminate the recording, only when the mouse is released the stoprecording is called
def recordingsound():
	global audio,frames, stream
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = 0.5
	 
	audio = pyaudio.PyAudio()
	 
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
	                rate=RATE, input=True,
	                frames_per_buffer=CHUNK)
	print("recording...")
	frames = []
	 
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

# This function will terminate the recording of given button
# only the argument b is used (the button id), argument e is just to catch the event Object
def stoprecording(e,b):
	global audio,frames,stream
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = str(b)+".wav"
	 
	print("finished recording")
	 
	 
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	 
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

#function to check which buttons are activated (the ones with a red background)
def convertMatrixtosound():
	global SoundMatrix
	playing = []
	counter = 0
	for a in SoundMatrix:
		if a["highlightbackground"] == 'red':
			playing.append(counter)
		counter += 1
	return playing

#function to toggle each buttons color (deactivate - blue, activate - red).
#This function also enables the starting button
def loadsound(row,col):
	global cols, SoundMatrix, starting_but

	if SoundMatrix[row*cols+col].config()["highlightbackground"][4] == 'blue':
		SoundMatrix[row*cols+col].config(highlightbackground="red")
		starting_but.config(state="active")
	else:
		SoundMatrix[row*cols+col].config(highlightbackground="blue")

# this function will be triggered every time the "start making music" button is clicked.
# It only receives the argument "app" to later on pass to the "playsound()" function (its pretty dumb I know, it was to avoid excessive global variables (which there are already plenty of) )
# Flag is to start/stop the loop
def loadsoundmatrix(app):
	global bpms, starting_but,flag
	if starting_but.cget("text") != "Stop the loop!":
		starting_but.config(text="Stop the loop!",state="active")
		flag = 0
	else:
		flag = 1
	while flag == 0:
		sounds=convertMatrixtosound()
		print(sounds)
		playsound(sounds,app)
	starting_but.config(text="Start making music!",state="active")

#Main function
#Defines all the graphical components through tkinter
#Binds all the sound buttons to the previously defined functions
def main():
	global rows, cols, SoundMatrix,starting_but, bpms,flag
	flag = 0
	root = Tk()
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.title("Sound table")
	mainframe = Frame(root)
	mainframe.pack(fill="both", expand=1)
	bpms = IntVar()
	bpms.set(60)
	Label(mainframe, text="Welcome to the digital sound table!",font='Helvetica 18 bold').pack()
	Label(mainframe, text="\nPlease select the tempo (bpms)").pack()
	entry_bpms = Entry(mainframe, textvariable=bpms,width=5)
	entry_bpms.bind("<KeyRelease>",limit_bpms)
	entry_bpms.pack()
	gridframe = Frame(root)
	for r in range(0,rows):
		for c in range(0,cols):
			but = Button(gridframe,text="\t\n\t\n",command = lambda ro=r,co=c: loadsound(ro,co),highlightbackground="blue")
			but.grid(row=r,column=c)
			but.bind("<Button-2>",lambda id_but=int(r*cols+c): recordingsound(id_but))
			but.bind("<ButtonRelease-2>",lambda e,id_but=int(r*cols+c): stoprecording(e,id_but))
			SoundMatrix.append(but)
	gridframe.pack(fill="both", expand=1)
	timeframe = Frame(root)
	starting_but = Button(timeframe, text="Start making music!",command = lambda: loadsoundmatrix(root),state="disabled")
	starting_but.pack()
	timeframe.pack(fill="both", expand=1)
	while True:
		root.update_idletasks()
		root.update()

# Used so this script can be imported later on as module
if __name__ == "__main__":
	main()