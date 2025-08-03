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
        Time Complexity: O(n) for duplicate check, O(1) for add
        Space Complexity: O(1)
        """
        # Prevent duplicate (by title and artist)
        current = self.head
        while current:
            if current.song.title == title and current.song.artist == artist:
                print("Song already exists. Not adding duplicate.")
                return
            current = current.next
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
        if to_index == self.size - 1:
            # Insert at the end
            current.prev = self.tail
            current.next = None
            if self.tail:
                self.tail.next = current
            self.tail = current
            if self.size == 1:
                self.head = current
        elif to_index == 0:
            # Insert at the head
            current.next = self.head
            if self.head:
                self.head.prev = current
            self.head = current
            current.prev = None
            if self.size == 1:
                self.tail = current
        else:
            target = self.head
            for _ in range(to_index):
                target = target.next
            prev_node = target.prev
            prev_node.next = current
            current.prev = prev_node
            current.next = target
            target.prev = current

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
        Deletes the song at the given index from the playlist.
        Time: O(n) | Space: O(1)
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
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
        # If list is now empty, reset head and tail
        if self.size == 0:
            self.head = None
            self.tail = None

    def get_song(self, index):
        """
        Returns the Song object at the given index.
        Time: O(n) | Space: O(1)
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.song

    def clear_playlist(self):
        """
        Clears the entire playlist.
        Time: O(1) | Space: O(1)
        """
        self.head = None
        self.tail = None
        self.size = 0
