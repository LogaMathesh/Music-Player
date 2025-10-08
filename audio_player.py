import pygame
import threading
import time
import os
from queue import Queue

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_song = None
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.7
        
    def load_playlist(self, playlist_file):
        """Load playlist from file"""
        self.playlist = []
        if os.path.exists(playlist_file):
            with open(playlist_file, "r", encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        name, path = line.strip().split("|")
                        self.playlist.append({"name": name, "path": path})
    
    def play_song(self, song_path):
        """Play a specific song"""
        try:
            if os.path.exists(song_path):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()
                self.current_song = song_path
                self.is_playing = True
                self.is_paused = False
                return True
            else:
                print(f"File not found: {song_path}")
                return False
        except Exception as e:
            print(f"Error playing song: {e}")
            return False
    
    def play_current(self):
        """Play current song from playlist"""
        if self.playlist and 0 <= self.current_index < len(self.playlist):
            song = self.playlist[self.current_index]
            return self.play_song(song["path"])
        return False
    
    def next_song(self):
        """Go to next song"""
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            return self.play_current()
        return False
    
    def previous_song(self):
        """Go to previous song"""
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            return self.play_current()
        return False
    
    def pause(self):
        """Pause current song"""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
    
    def resume(self):
        """Resume current song"""
        if self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
    
    def stop(self):
        """Stop current song"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def get_status(self):
        """Get current player status"""
        return {
            "current_song": self.current_song,
            "current_index": self.current_index,
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "volume": self.volume,
            "playlist_length": len(self.playlist)
        }

# Global player instance
player = AudioPlayer()
