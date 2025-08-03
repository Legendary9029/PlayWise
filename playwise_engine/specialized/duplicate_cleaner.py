# File: specialized/duplicate_cleaner.py

class DuplicateCleaner:
    def __init__(self):
        self.seen = set()  # Stores (title.lower(), artist.lower()) tuples

    def is_duplicate(self, title, artist):
        """
        Checks if the song is a duplicate.
        Time Complexity: O(1)
        """
        key = (title.lower(), artist.lower())
        if key in self.seen:
            return True
        self.seen.add(key)
        return False

    def clean_playlist(self, playlist):
        """
        Removes duplicates from the playlist engine (in-place).
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        self.seen.clear()
        current = playlist.head
        index = 0
        while current:
            key = (current.song.title.lower(), current.song.artist.lower())
            if key in self.seen:
                next_node = current.next
                playlist.delete_song(index)
                current = next_node
                continue  # Don't increment index because we deleted
            else:
                self.seen.add(key)
                current = current.next
                index += 1
