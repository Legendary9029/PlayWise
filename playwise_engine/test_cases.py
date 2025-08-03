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

    def test_reverse_empty_playlist(self):
        playlist = PlaylistEngine()
        playlist.reverse_playlist()  # Should not crash
        self.assertEqual(playlist.display_playlist(), [])

    def test_sorting_merge(self):
        from core.sorting import merge_sort
        playlist = PlaylistEngine()
        playlist.add_song("C", "A", 100)
        playlist.add_song("A", "B", 200)
        playlist.add_song("B", "C", 150)
        # Sort by title
        sorted_songs = merge_sort(playlist.display_playlist(), key=lambda s: s.title)
        self.assertEqual([s.title for s in sorted_songs], ["A", "B", "C"])

    def test_large_input_performance(self):
        import time
        playlist = PlaylistEngine()
        for i in range(1000):
            playlist.add_song(f"Song{i}", f"Artist{i%10}", i)
        lookup = InstantSongLookup()
        for song in playlist.display_playlist():
            lookup.add_song(song)
        start = time.time()
        found = lookup.get_by_title("Song500")
        end = time.time()
        self.assertIsNotNone(found)
        self.assertLess(end - start, 0.01)  # Should be fast

if __name__ == "__main__":
    unittest.main()
