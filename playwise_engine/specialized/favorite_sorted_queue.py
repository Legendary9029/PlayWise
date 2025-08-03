# File: specialized/favorite_sorted_queue.py

import heapq

class FavoriteSortedQueue:
    def __init__(self):
        # Max-heap: use negative duration
        self.listen_heap = []  # Each entry: (-total_time_listened, song_id, song)
        self.song_map = {}     # Maps song_id to (total_time_listened, song)

    def add_listen_time(self, song, seconds):
        """
        Add listening time to a song and keep the queue sorted.
        Time Complexity: O(log n)
        Space Complexity: O(n)
        """
        if song.song_id in self.song_map:
            total_time, _ = self.song_map[song.song_id]
            total_time += seconds
        else:
            total_time = seconds

        self.song_map[song.song_id] = (total_time, song)
        heapq.heappush(self.listen_heap, (-total_time, song.song_id, song))

    def get_top_k_songs(self, k=5):
        """
        Returns top k most-listened songs.
        Time Complexity: O(k)
        Space Complexity: O(k)
        """
        seen = set()
        result = []
        temp = []

        while self.listen_heap and len(result) < k:
            duration_neg, song_id, song = heapq.heappop(self.listen_heap)
            if song_id not in seen:
                seen.add(song_id)
                result.append(song)
                temp.append((duration_neg, song_id, song))

        for entry in temp:
            heapq.heappush(self.listen_heap, entry)

        return result