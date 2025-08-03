# File: test_cases.py

import unittest
from models.song import Song
from core.playlist_engine import PlaylistEngine
from core.playback_history import PlaybackHistory
from core.song_rating_tree import SongRatingTree
from core.instant_lookup import InstantSongLookup
from specialized.duplicate_cleaner import DuplicateCleaner
from specialized.favorite_sorted_queue import FavoriteSortedQueue

class PlayWiseTestSuite(unittest.TestCase):
    def test_playlist_add_and_reverse(self):
        playlist = PlaylistEngine()
        playlist.add_song("Song A", "Artist A", 180)
        playlist.add_song("Song B", "Artist B", 210)
        playlist.reverse_playlist()
        songs = playlist.display_playlist()
        self.assertEqual(str(songs[0]), "Song B by Artist B (210s)")

    def test_playback_undo(self):
        history = PlaybackHistory()
        s1 = Song("1", "Test", "Artist", 120)
        history.play_song(s1)
        self.assertEqual(history.undo_last_play(), s1)

    def test_rating_tree_search(self):
        tree = SongRatingTree()
        s1 = Song("1", "Test", "Artist", 200)
        tree.insert_song(s1, 4)
        result = tree.search_by_rating(4)
        self.assertEqual(result[0], s1)

    def test_lookup(self):
        lookup = InstantSongLookup()
        s1 = Song("1", "Title", "Artist", 100)
        lookup.add_song(s1)
        self.assertEqual(lookup.get_by_title("title"), s1)
        self.assertEqual(lookup.get_by_id("1"), s1)

    def test_deduplication(self):
        cleaner = DuplicateCleaner()
        self.assertFalse(cleaner.is_duplicate("Same", "Artist"))
        self.assertTrue(cleaner.is_duplicate("Same", "Artist"))

    def test_favorite_queue(self):
        queue = FavoriteSortedQueue()
        s1 = Song("1", "Fav1", "A", 300)
        s2 = Song("2", "Fav2", "B", 200)
        queue.add_listen_time(s1, 600)
        queue.add_listen_time(s2, 400)
        top = queue.get_top_k_songs(2)
        self.assertEqual(top[0], s1)
        self.assertEqual(top[1], s2)

    def test_duplicate_cleaner_on_playlist(self):
        playlist = PlaylistEngine()
        playlist.add_song("SongA", "ArtistA", 100)
        playlist.add_song("SongA", "ArtistA", 120)
        cleaner = DuplicateCleaner()
        cleaner.clean_playlist(playlist)
        songs = playlist.display_playlist()
        self.assertEqual(len(songs), 1)

    def test_system_snapshot(self):
        playlist = PlaylistEngine()
        playlist.add_song("A", "X", 100)
        playlist.add_song("B", "Y", 200)
        playlist.add_song("C", "Z", 300)
        history = PlaybackHistory()
        s1 = Song("1", "A", "X", 100)
        s2 = Song("2", "B", "Y", 200)
        history.play_song(s1)
        history.play_song(s2)
        tree = SongRatingTree()
        tree.insert_song(s1, 5)
        tree.insert_song(s2, 4)
        from core.system_snapshot import SystemSnapshot
        snap = SystemSnapshot(playlist, history, tree)
        data = snap.export_snapshot()
        self.assertIn('Top 5 Longest Songs', data)
        self.assertIn('Most Recently Played', data)
        self.assertIn('Song Count by Rating', data)

if __name__ == "__main__":
    unittest.main()
