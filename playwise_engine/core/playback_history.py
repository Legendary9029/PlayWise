# File: core/playback_history.py

from collections import deque
from models.song import Song

class PlaybackHistory:
    def __init__(self):
        self.history_stack = deque()  # Stack to hold played songs (LIFO)

    def play_song(self, song):
        """
        Simulates playing a song and stores it in history.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.history_stack.append(song)

    def undo_last_play(self):
        """
        Returns the last played song to re-add to the playlist.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.history_stack:
            return self.history_stack.pop()
        return None

    def get_recent_history(self, limit=5):
        """
        View recent playback history (for UI/debugging).
        Time Complexity: O(k)
        Space Complexity: O(k)
        """
        return list(self.history_stack)[-limit:]
