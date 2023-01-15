from tkinter import *
import os
import threading
import time
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import themed_tk as tk

mixer.init()  # Initialization

window = tk.ThemedTk()  # Tk() creates a window and stores in window
window.get_themes()
window.set_theme('aquativo')
window.configure(bg='#0f213b')

# Status Bar
status_bar = Label(window, text='Welcome to Rhythm', relief_=SUNKEN, anchor=W, font='times 14 italic')  # W->West
status_bar.pack(side=BOTTOM, fill=X)  # X->X-axis

filename_path = ""

# Create menubar
menubar = Menu(window, fg='white', bg='black')
window.config(menu=menubar)


# Create Submenu
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist_main(filename_path)


# playlist contains the full path+filename
playlistbox = []


# Function to add to playList
def delete_song():
    del_song = selected_box.curselection()
    index = int(del_song[0])
    selected_box.delete(index)
    selected_pathbox.pop(index)


# Function to add to playList
def add_to_playlist_main(filename_path):
    filename = os.path.basename(filename_path)
    index = 0
    selected_box.insert(index, filename)
    selected_pathbox.insert(index, filename_path)
    index += 1


submenu = Menu(menubar, tearoff=0, bg='black', fg='white')  # tearoff=0 removes the dashed line from cascade
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=window.destroy)


# Function to create about_us
def about_us():
    tkinter.messagebox.showinfo('Rhythm', 'This is a music player built using Python tkinter by CL InfoTech')


submenu = Menu(menubar, tearoff=0, bg='black', fg='white')  # tearoff=0 removes the dashed line from cascade
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About us", command=about_us)

window.geometry('1525x750')  # window size
#window.state('zoomed')
window.title('Rhythm')  # Title
#window.iconbitmap(r'images/Rhythm.ico')  # icon here r->raw string
window.resizable(True, True)

# Right Frame
right_frame = Frame(window, bg='#0f213b')
right_frame.pack(side=RIGHT)

# left Frame
Left_frame = Frame(window, bg='#0f213b')
Left_frame.pack(side=LEFT)

# Text
text = Label(Left_frame, text='“Music gives a soul to the universe"', font='times 20 italic', bg='#0f213b', fg='white')
text.pack(padx=40, pady=20)  # To display on window

selected_box = Listbox(Left_frame, width=60, height=25, bg='#010312', fg='white')
selected_box.pack(padx=40, pady=20)
selected_pathbox = []

# Text
text = Label(Left_frame, text='PLAYLIST', font='times 15 italic', bg='#0f213b', fg='white')
text.pack(padx=40, pady=5)  # To display on window

# Create buttons
add = ttk.Button(Left_frame, text="+Add", command=browse_file)
add.pack(pady=10)
delete = ttk.Button(Left_frame, text="-Delete", command=delete_song)
delete.pack(pady=5)

# top Frame
top_frame = Frame(right_frame, bg='#0f213b')
top_frame.pack()

image1 = PhotoImage(file='assets/images/background.png')
labelimage = Label(top_frame, image=image1, text="", width=500, height=350)
labelimage.pack(pady=20, padx=270)

# Display Filename
filelabel = Label(top_frame, font='times 15 italic', bg='#0f213b', fg='white')
filelabel.pack(pady=3, padx=10)

# Display total length of file
lengthlabel = Label(top_frame, text='  -  -  :  -  -  ', font='times 20 italic', bg='#0f213b', fg='white')
lengthlabel.pack()

# Display Current Time of file
current_timelabel = Label(top_frame, text='  -  -  :  -  -  ', font='times 20 italic', bg='#0f213b', fg='white')
current_timelabel.pack()


# Function to display Music name/Filename
def show_details(play_song):
    file_data = os.path.splitext(play_song)
    if file_data[1] == ".mp3":
        filelabel['text'] = "Playing " + '  -  ' + os.path.basename(play_song)
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        filelabel['text'] = "Playing " + '  -  ' + os.path.basename(play_song)
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    minutes, seconds = divmod(total_length, 60)  # div->total_length/60 and mod->total_length%60
    minutes = round(minutes)
    seconds = round(seconds)
    time_format = '{:02d}:{:02d}'.format(minutes, seconds)
    lengthlabel['text'] = time_format

    t1 = threading.Thread(target=start_count, args=(total_length,))  # Creating a thread
    t1.start()


# Function to display current time
def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():  # mixer.music.get_busy() returns false when stop button is pressed
        if paused:
            continue
        else:
            minutes, seconds = divmod(current_time, 60)
            minutes = round(minutes)
            seconds = round(seconds)
            time_format = '{:02d}:{:02d}'.format(minutes, seconds)
            current_timelabel['text'] = time_format
            time.sleep(1)
            current_time += 1


paused = False


# Function to pause Music
def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    status_bar['text'] = "Music Paused"


# Function to play Music
def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        status_bar['text'] = "Music Unpaused"
        paused = False
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = selected_box.curselection()
            index = int(selected_song[0])
            play_song = selected_pathbox[index]
            mixer.music.load(play_song)
            mixer.music.play()
            status_bar['text'] = "Playing Music" + ' - ' + os.path.basename(play_song)
            show_details(play_song)

        except:
            tkinter.messagebox.showerror('File not found', 'RHYTHM COULD NOT FIND THE FILE PLEASE CHECK AGAIN')


# Function to stop Music
def stop_music():
    mixer.music.stop()
    status_bar['text'] = "Music Stopped" + ' - ' + os.path.basename(filename_path)


# Function to Rewind music
def rewind_music():
    play_music()
    status_bar['text'] = "Music Rewinded"


# Function to Set sound
def set_sound(val):
    sound = float(val) / 100
    mixer.music.set_volume(sound)  # takes values only from 0 to 1


# variable to check music is muted or not
muted = False


# Function to Mute music
def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)  # Unmute the music
        volume.set(70)  # Sets the scale value  to 70
        volume_up_button.configure(image=volume_up)
        muted = False
    else:
        mixer.music.set_volume(0)  # Mute the music
        volume.set(0)  # Sets the scale value  to 0
        volume_up_button.configure(image=mute)
        muted = True


# Middle Frame
middle_frame = Frame(right_frame, bg='#0f213b', relief=SUNKEN)
middle_frame.pack(pady=10, padx=50)

# Play Button
play = PhotoImage(file='assets/images/play.png')  # labelPlay = Label(window, image=play)  adding image
play_button = ttk.Button(middle_frame, image=play, command=play_music)  # Creating a Button
play_button.grid(row=0, column=0, padx=10)

# Stop Button
stop = PhotoImage(file='assets/images/stop.png')  # labelPlay = Label(window, image=stop)  adding image
stop_button = ttk.Button(middle_frame, image=stop, command=stop_music)  # Creating a Button
stop_button.grid(row=0, column=1, padx=10)

# Pause Button
pause = PhotoImage(file='assets/images/pause.png')  # labelPlay = Label(window, image=pause)  adding image
pause_button = ttk.Button(middle_frame, image=pause, command=pause_music)  # Creating a Button
pause_button.grid(row=0, column=2, padx=10)

# Pause Button
pause = PhotoImage(file='assets/images/pause.png')  # labelPlay = Label(window, image=pause)  adding image
pause_button = ttk.Button(middle_frame, image=pause, command=pause_music)  # Creating a Button
pause_button.grid(row=0, column=2, padx=10)

# Bottom Frame
Bottom_frame = Frame(right_frame, bg='#0f213b')
Bottom_frame.pack(pady=20, padx=50)

# Rewind Button
rewind = PhotoImage(file='assets/images/rewind.png')  # labelPlay = Label(window, image=pause)  adding image
rewind_button = ttk.Button(Bottom_frame, image=rewind, command=rewind_music)  # Creating a Button
rewind_button.grid(row=0, column=0)

# Mute and Volume-up Button
mute = PhotoImage(file='assets/images/mute.png')  # labelPlay = Label(window, image=pause)  adding image
volume_up = PhotoImage(file='assets/images/volume-adjustment.png')
volume_up_button = ttk.Button(Bottom_frame, image=volume_up, command=mute_music)  # Creating a Button
volume_up_button.grid(row=0, column=1)

# Volume controller
volume = ttk.Scale(Bottom_frame, from_=0, to=100, orient=HORIZONTAL,
                   command=set_sound)  # function returns the value pointed by the scale
volume.set(70)  # Sets the default value to scale
mixer.music.set_volume(0.7)
volume.grid(row=0, column=2, padx=30, pady=15)


# Function to Override closing window function
def on_closing():
    stop_music()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)  # overridding a function
window.mainloop()  # mainloop function makes the window stay for a long time
