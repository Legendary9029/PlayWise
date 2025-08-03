# \ud83c\udfb5 PlayWise: Smart Playlist Management Engine

An intelligent backend system designed for playlist control, personalized recommendations, and real-time song analytics.

---

## \ud83d\udce6 Features Implemented

### Core Modules
- **Playlist Engine** \u2013 Add, delete, move, and reverse songs using doubly linked list
- **Playback History** \u2013 Undo recent plays with stack-based LIFO history
- **Song Rating Tree** \u2013 BST to manage and query songs by 1\u20135 star ratings
- **Instant Lookup** \u2013 HashMap for O(1) access by song ID or title
- **Time-Based Sorting** \u2013 Merge sort by title, duration, or recent
- **Playback Optimization** \u2013 Constant-time swaps and lazy reversal support
- **System Snapshot** \u2013 Dashboard shows longest songs, history, and rating stats

### Specialized Use Cases
- **Duplicate Cleaner** \u2013 Auto-removes songs with same title + artist
- **Favorite Queue** \u2013 Maintains top songs by listening duration using max-heap

---

## \ud83d\ude80 Getting Started

### Prerequisites
- Python 3.7+

### Run the Main Demo
```bash
python main.py
```

### Run Unit Tests
```bash
python test_cases.py
```

---

## \ud83d\udcc2 Project Structure
```
playwise_engine/
├── core/                 # Core modules (playlist, history, sorting, etc.)
├── specialized/          # Extra features (duplicates, favorites)
├── models/               # Song object model
├── main.py               # Simulation entry point
├── test_cases.py         # Unit tests
├── README.md             # This file
```

---

## \ud83e\udde0 Learning Objectives
- Linked List, Stack, BST, HashMap, Heap
- Sorting Algorithms: Merge Sort
- Space & Time Optimization
- Real-time system design

---

## \ud83d\udccc License
MIT \u2013 Free to use for education and open-source projects.

---

## 🚀 Example Usage

### Playlist Operations
```python
from core.playlist_engine import PlaylistEngine
playlist = PlaylistEngine()
playlist.add_song("Song A", "Artist A", 180)
playlist.add_song("Song B", "Artist B", 210)
playlist.move_song(0, 1)
playlist.reverse_playlist()
print(playlist.display_playlist())
```

### Playback History Undo
```python
from core.playback_history import PlaybackHistory
history = PlaybackHistory()
history.play_song(song)
last = history.undo_last_play()
```

### Song Rating Tree
```python
from core.song_rating_tree import SongRatingTree
tree = SongRatingTree()
tree.insert_song(song, 5)
songs_with_5 = tree.search_by_rating(5)
```

### Instant Song Lookup
```python
from core.instant_lookup import InstantSongLookup
lookup = InstantSongLookup()
lookup.add_song(song)
found = lookup.get_by_id(song.song_id)
```

### Duplicate Cleaner
```python
from specialized.duplicate_cleaner import DuplicateCleaner
cleaner = DuplicateCleaner()
cleaner.clean_playlist(playlist)
```

### Favorite Queue
```python
from specialized.favorite_sorted_queue import FavoriteSortedQueue
queue = FavoriteSortedQueue()
queue.add_listen_time(song, 300)
top = queue.get_top_k_songs(3)
```

### System Snapshot
```python
from core.system_snapshot import SystemSnapshot
snap = SystemSnapshot(playlist, history, tree)
data = snap.export_snapshot()
print(data)
```

---

## 🛠️ Extending the System
- Add new data structures or algorithms in the `core/` or `specialized/` folders.
- Write new tests in `test_cases.py` to validate your features.
- Update the dashboard logic in `system_snapshot.py` for new analytics.

---
