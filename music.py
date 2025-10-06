import tkinter as tk
from tkinter import ttk
import subprocess

# Run C executable
subprocess.Popen(['MusicPlayer.exe'])

# Load playlist
playlist = []
with open("playlist.txt", "r") as f:
    for line in f:
        song = line.strip().split("|")
        playlist.append({"name": song[0], "path": song[1]})

current_index = 0

# GUI
root = tk.Tk()
root.title("Music Player GUI")

# Playlist Listbox
listbox = tk.Listbox(root, width=50)
listbox.pack()
for song in playlist:
    listbox.insert(tk.END, song["name"])
listbox.select_set(current_index)

# Now Playing
now_playing = tk.Label(root, text=f"Now Playing: {playlist[current_index]['name']}")
now_playing.pack()

# Control Buttons
def play_next():
    global current_index
    if current_index < len(playlist)-1:
        current_index += 1
        listbox.select_clear(0, tk.END)
        listbox.select_set(current_index)
        now_playing.config(text=f"Now Playing: {playlist[current_index]['name']}")

def play_prev():
    global current_index
    if current_index > 0:
        current_index -= 1
        listbox.select_clear(0, tk.END)
        listbox.select_set(current_index)
        now_playing.config(text=f"Now Playing: {playlist[current_index]['name']}")

frame = tk.Frame(root)
frame.pack()
tk.Button(frame, text="Previous", command=play_prev).pack(side=tk.LEFT)
tk.Button(frame, text="Next", command=play_next).pack(side=tk.LEFT)

root.mainloop()
