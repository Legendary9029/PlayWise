# File: models/song.py

class Song:
    def __init__(self, song_id, title, artist, duration):
        self.song_id = song_id            # Unique identifier (string or hash)
        self.title = title                # Song title
        self.artist = artist              # Song artist
        self.duration = duration          # Duration in seconds (int)

    def __repr__(self):
        return f"{self.title} by {self.artist} ({self.duration}s)"
