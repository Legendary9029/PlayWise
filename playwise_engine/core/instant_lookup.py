# File: core/instant_lookup.py

class InstantSongLookup:
    def __init__(self):
        self.id_map = {}       # Maps song_id to Song
        self.title_map = {}    # Maps title.lower() to Song (for case-insensitive search)

    def add_song(self, song):
        """
        Adds a song to both lookup maps.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.id_map[song.song_id] = song
        self.title_map[song.title.lower()] = song

    def remove_song(self, song):
        """
        Removes a song from both lookup maps.
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.id_map.pop(song.song_id, None)
        self.title_map.pop(song.title.lower(), None)

    def get_by_id(self, song_id):
        """
        Retrieves song by its unique ID.
        Time Complexity: O(1)
        """
        return self.id_map.get(song_id)

    def get_by_title(self, title):
        """
        Retrieves song by title (case-insensitive).
        Time Complexity: O(1)
        """
        return self.title_map.get(title.lower())
