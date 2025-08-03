# File: main.py

from models.song import Song
from core.playlist_engine import PlaylistEngine
from core.playback_history import PlaybackHistory
from core.song_rating_tree import SongRatingTree
from core.instant_lookup import InstantSongLookup
from core.system_snapshot import SystemSnapshot
from specialized.duplicate_cleaner import DuplicateCleaner
from specialized.favorite_sorted_queue import FavoriteSortedQueue

# Initialize modules
playlist = PlaylistEngine()
history = PlaybackHistory()
rating_tree = SongRatingTree()
lookup = InstantSongLookup()
snapshot = SystemSnapshot(playlist, history, rating_tree)
deduplicator = DuplicateCleaner()
favorite_queue = FavoriteSortedQueue()

# Sample demo songs
demo_songs = [
    ("Fix You", "Coldplay", 295),
    ("Blinding Lights", "The Weeknd", 200),
    ("Fix You", "Coldplay", 295),  # Duplicate
    ("Bohemian Rhapsody", "Queen", 354),
    ("Lose Yourself", "Eminem", 326),
]

# Add songs to playlist with duplicate handling
for title, artist, duration in demo_songs:
    if not deduplicator.is_duplicate(title, artist):
        playlist.add_song(title, artist, duration)

# Sync with lookup and rating tree
current = playlist.head
rating = 5
while current:
    lookup.add_song(current.song)
    rating_tree.insert_song(current.song, rating)
    rating -= 1 if rating > 1 else 0  # Vary rating
    current = current.next

# Play a few songs
current = playlist.head
while current:
    history.play_song(current.song)
    favorite_queue.add_listen_time(current.song, current.song.duration * 2)  # Simulate heavy listening
    current = current.next

# Use system snapshot
print("\n=== System Snapshot ===")
snap = snapshot.export_snapshot()
for key, value in snap.items():
    print(f"{key}:\n{value}\n")

# Favorite songs
print("Top 3 Favorite Songs:")
for song in favorite_queue.get_top_k_songs(3):
    print(f"  - {song}")