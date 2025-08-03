# File: core/playlist_engine.py

from models.song import Song

class SongNode:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None


class PlaylistEngine:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_song(self, title, artist, duration):
        """
        Add a new song to the end of the playlist.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        song = Song(f"{title.lower()}_{artist.lower()}", title, artist, duration)
        node = SongNode(song)
        if not self.head:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self.size += 1

    def move_song(self, from_index, to_index):
        """
        Move a song from one index to another.
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if from_index == to_index:
            return
        if from_index < 0 or from_index >= self.size or to_index < 0 or to_index >= self.size:
            raise IndexError("Index out of bounds")

        # Step 1: Remove node from from_index
        current = self.head
        for _ in range(from_index):
            current = current.next

        # Disconnect current
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

        # Step 2: Insert node at to_index
        target = self.head
        for _ in range(to_index):
            target = target.next

        if to_index == 0:
            current.next = self.head
            self.head.prev = current
            self.head = current
            current.prev = None
        else:
            prev_node = target.prev
            prev_node.next = current
            current.prev = prev_node
            current.next = target
            target.prev = current

        if to_index == self.size - 1:
            self.tail = current

    def reverse_playlist(self):
        """
        Reverse the playlist in place.
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        current = self.head
        prev = None
        while current:
            current.prev, current.next = current.next, current.prev
            prev = current
            current = current.prev

        self.head, self.tail = self.tail, self.head

    def display_playlist(self):
        """
        Utility function to print the playlist.
        """
        songs = []
        current = self.head
        while current:
            songs.append(current.song)
            current = current.next
        return songs

    def delete_song(self, index):
        """
        Delete a song at the specified index from the playlist.
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev
        self.size -= 1
