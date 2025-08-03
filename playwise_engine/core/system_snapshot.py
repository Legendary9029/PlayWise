# File: core/system_snapshot.py

from core.sorting import sort_by_duration

class SystemSnapshot:
    def __init__(self, playlist_engine, playback_history, rating_tree):
        self.playlist_engine = playlist_engine
        self.playback_history = playback_history
        self.rating_tree = rating_tree

    def top_5_longest_songs(self):
        """
        Returns the 5 longest songs from the playlist.
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        songs = self.playlist_engine.display_playlist()
        sorted_songs = sort_by_duration(songs, reverse=True)
        return sorted_songs[:5]

    def most_recently_played(self):
        """
        Returns the most recently played 5 songs.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.playback_history.get_recent_history(limit=5)

    def song_count_by_rating(self):
        """
        Returns a dictionary of rating -> number of songs.
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        counts = {i: 0 for i in range(1, 6)}

        def traverse(node):
            if not node:
                return
            counts[node.rating] += len(node.songs)
            traverse(node.left)
            traverse(node.right)

        traverse(self.rating_tree.root)
        return counts

    def export_snapshot(self):
        """
        Returns all dashboard data in a single dict.
        Time Complexity: O(n log n) (dominated by sorting)
        Space Complexity: O(n)
        """
        return {
            'Top 5 Longest Songs': self.top_5_longest_songs(),
            'Most Recently Played': self.most_recently_played(),
            'Song Count by Rating': self.song_count_by_rating()
        }
