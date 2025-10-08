from flask import Flask, render_template, request, redirect, flash, jsonify
import os
import time
from werkzeug.utils import secure_filename
from audio_player import player

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

PLAYLIST_FILE = "playlist.txt"
SONGS_FOLDER = "songs"
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'ogg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_song_to_playlist(song_name, file_path):
    """Add a new song to the playlist file"""
    with open(PLAYLIST_FILE, "a", encoding='utf-8') as f:
        f.write(f"{song_name}|{file_path}\n")


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
    player.load_playlist(PLAYLIST_FILE)
    return render_template("index.html", playlist=playlist)

@app.route("/play", methods=["POST"])
def play():
    song_path = request.form.get("song_path")
    if not os.path.exists(song_path):
        flash(f"Song not found: {song_path}")
        return redirect("/")
    
    # Find the song index in playlist
    playlist = read_playlist()
    song_index = None
    for i, song in enumerate(playlist):
        if song["path"] == song_path:
            song_index = i
            break
    
    if song_index is not None:
        player.current_index = song_index
    
    # Try to play the song
    if player.play_song(song_path):
        flash(f"Playing: {os.path.basename(song_path)}")
    else:
        flash(f"Error playing song: {os.path.basename(song_path)}")
    
    return redirect("/")

@app.route("/next")
def next_song():
    if player.next_song():
        flash("Skipping to next song")
    else:
        flash("No next song available")
    return redirect("/")

@app.route("/prev")
def prev_song():
    if player.previous_song():
        flash("Going to previous song")
    else:
        flash("No previous song available")
    return redirect("/")


@app.route("/pause")
def pause_song():
    player.pause()
    flash("Song paused")
    return redirect("/")


@app.route("/resume")
def resume_song():
    player.resume()
    flash("Song resumed")
    return redirect("/")


@app.route("/stop")
def stop_song():
    player.stop()
    flash("Song stopped")
    return redirect("/")


@app.route("/status")
def get_status():
    """Get current player status as JSON"""
    return jsonify(player.get_status())


@app.route("/add_song", methods=["POST"])
def add_song():
    if 'song_file' not in request.files:
        flash('No file selected')
        return redirect("/")
    
    song_name = request.form.get('song_name')
    if not song_name:
        flash('Please enter a song name')
        return redirect("/")
    
    file = request.files['song_file']
    if file.filename == '':
        flash('No file selected')
        return redirect("/")
    
    if file and allowed_file(file.filename):
        # Create songs directory if it doesn't exist
        if not os.path.exists(SONGS_FOLDER):
            os.makedirs(SONGS_FOLDER)
        
        # Get secure filename and save file
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{int(time.time())}{ext}"
        file_path = os.path.join(SONGS_FOLDER, filename)
        file.save(file_path)
        
        # Add to playlist
        relative_path = file_path.replace("\\", "/")  # Use forward slashes for consistency
        add_song_to_playlist(song_name, relative_path)
        
        flash(f'Song "{song_name}" added successfully!')
    else:
        flash('Invalid file type. Please upload MP3, WAV, M4A, FLAC, or OGG files.')
    
    return redirect("/")


@app.route("/debug")
def debug():
    """Debug route to check file paths and system info"""
    debug_info = {
        "current_directory": os.getcwd(),
        "music_player_exists": os.path.exists(C_PLAYER),
        "songs_folder_exists": os.path.exists(SONGS_FOLDER),
        "playlist_file_exists": os.path.exists(PLAYLIST_FILE),
        "songs_in_folder": os.listdir(SONGS_FOLDER) if os.path.exists(SONGS_FOLDER) else [],
        "playlist_content": []
    }
    
    # Read playlist content
    if os.path.exists(PLAYLIST_FILE):
        with open(PLAYLIST_FILE, "r") as f:
            debug_info["playlist_content"] = [line.strip() for line in f.readlines()]
    
    return f"<pre>{debug_info}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
