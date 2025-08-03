"""
PlayWise CLI: A terminal-based interface for managing your playlist.
"""

import sys
from core.playlist_engine import PlaylistEngine
from core.playback_history import PlaybackHistory
from core.song_rating_tree import SongRatingTree
from core.instant_lookup import InstantSongLookup
from core.sorting import merge_sort
from core.system_snapshot import SystemSnapshot
from specialized.duplicate_cleaner import DuplicateCleaner
from specialized.favorite_sorted_queue import FavoriteSortedQueue
from models.song import Song
import subprocess
import os

def print_menu():
    print("\nPlayWise CLI")
    print("1. Add song")
    print("2. Delete song by index")
    print("3. Move song")
    print("4. Reverse playlist")
    print("5. Show playlist")
    print("6. Rate song (1-5)")
    print("7. Undo last playback")
    print("8. Clean duplicates")
    print("9. Show system snapshot")
    print("10. Top 3 favorite songs")
    print("11. Search by title")
    print("12. Exit")
    print("13. Simulate playback (play a song)")
    print("14. Sort playlist")
    print("15. Run all test cases")

def format_duration(seconds):
    return f"{seconds//60}:{seconds%60:02d}"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    playlist = PlaylistEngine()
    history = PlaybackHistory()
    rating_tree = SongRatingTree()
    lookup = InstantSongLookup()
    fav_queue = FavoriteSortedQueue()
    cleaner = DuplicateCleaner()
    song_counter = 1

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == '1':
            title = input("Song title: ")
            artist = input("Artist: ")
            duration = int(input("Duration (seconds): "))
            song = Song(str(song_counter), title, artist, duration)
            song_counter += 1
            playlist.add_song(title, artist, duration)
            lookup.add_song(song)
            print("Song added.")

        elif choice == '2':
            idx = int(input("Index to delete: "))
            try:
                playlist.delete_song(idx)
                print("Song deleted.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '3':
            from_idx = int(input("Move from index: "))
            to_idx = int(input("Move to index: "))
            try:
                playlist.move_song(from_idx, to_idx)
                print("Song moved.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '4':
            playlist.reverse_playlist()
            print("Playlist reversed.")

        elif choice == '5':
            songs = playlist.display_playlist()
            if not songs:
                print("Playlist is empty.")
            for i, song in enumerate(songs):
                print(f"{i}: {song.title} by {song.artist} ({format_duration(song.duration)})")

        elif choice == '6':
            idx = int(input("Index to rate: "))
            rating = int(input("Rating (1-5): "))
            try:
                song = playlist.get_song(idx)
                rating_tree.insert_song(song, rating)
                print("Song rated.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '7':
            try:
                song = history.undo_last_play()
                if song:
                    playlist.add_song(song.title, song.artist, song.duration)
                    print("Last playback undone.")
                else:
                    print("No playback history.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '8':
            cleaner.clean_playlist(playlist)
            print("Duplicates cleaned.")

        elif choice == '9':
            snap = SystemSnapshot(playlist, history, rating_tree)
            data = snap.export_snapshot()
            print("System Snapshot:")
            for k, v in data.items():
                print(f"{k}: {v}")

        elif choice == '10':
            top = fav_queue.get_top_k_songs(3)
            if not top:
                print("Top 3 Favorite Songs:")
                print("(No songs have been played yet.)")
            else:
                print("Top 3 Favorite Songs:")
                for i, song in enumerate(top, start=1):
                    print(f"{i}. {song.title} by {song.artist} ({format_duration(song.duration)})")

        elif choice == '11':
            title = input("Song title to search: ")
            song = lookup.get_by_title(title)
            if song:
                print(f"Found: {song.title} by {song.artist} ({format_duration(song.duration)})")
            else:
                print("Song not found.")

        elif choice == '12':
            print("Exiting PlayWise CLI.")
            sys.exit(0)

        elif choice == '13':
            idx = int(input("Index to play: "))
            try:
                song = playlist.get_song(idx)
                history.play_song(song)
                fav_queue.add_listen_time(song, song.duration)
                print(f"Played: {song.title} by {song.artist}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '14':
            print("Sort by: 1. Title  2. Duration")
            sort_choice = input("Sort by: ").strip()
            songs = playlist.display_playlist()
            if sort_choice == '1':
                sorted_songs = merge_sort(songs, lambda s: s.title)
            elif sort_choice == '2':
                sorted_songs = merge_sort(songs, lambda s: s.duration)
            else:
                print("Invalid sort option.")
                continue
            print("Sorted Playlist:")
            for i, song in enumerate(sorted_songs):
                print(f"{i}: {song.title} by {song.artist} ({format_duration(song.duration)})")

        elif choice == '15':
            print("Running all test cases...")
            result = subprocess.run([sys.executable, 'test_cases.py'], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Test Errors:\n", result.stderr)

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
