from flask import Flask, render_template, request, redirect
import subprocess
import os

app = Flask(__name__)

C_PLAYER = r"C:\Users\mloga\OneDrive\Desktop\MusicPlayer.exe"
PLAYLIST_FILE = "playlist.txt"


def read_playlist():
    playlist = []
    with open("playlist.txt", "r") as f:
        for line in f:
            name, rel_path = line.strip().split("|")
            full_path = os.path.join(os.getcwd(), rel_path)
            playlist.append({"name": name, "path": full_path})
    return playlist
@app.route("/")
def index():
    playlist = read_playlist()
    return render_template("index.html", playlist=playlist)

@app.route("/play", methods=["POST"])
def play():
    song_path = request.form.get("song_path")
    if not os.path.exists(song_path):
        return f"Song not found: {song_path}", 500
    subprocess.Popen([C_PLAYER, "play", song_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return redirect("/")

@app.route("/next")
def next_song():
    subprocess.Popen([C_PLAYER, "next"])
    return redirect("/")

@app.route("/prev")
def prev_song():
    subprocess.Popen([C_PLAYER, "prev"])
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
