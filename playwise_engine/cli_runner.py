"""
PlayWise CLI: A terminal-based interface for managing your playlist.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import subprocess

from core.playlist_engine import PlaylistEngine
from core.playback_history import PlaybackHistory
from core.song_rating_tree import SongRatingTree
from core.instant_lookup import InstantSongLookup
from core.sorting import merge_sort
from core.system_snapshot import SystemSnapshot
from specialized.duplicate_cleaner import DuplicateCleaner
from specialized.favorite_sorted_queue import FavoriteSortedQueue
from models.song import Song

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("\nPlayWise CLI")
    print("1. Add song")
    print("2. Show playlist")
    print("3. Delete song by index")
    print("4. Move song")
    print("5. Reverse playlist")
    print("6. Rate song (1–5)")
    print("7. Simulate playback (play a song)")
    print("8. Undo last playback")
    print("9. Clean duplicates")
    print("10. Search by title")
    print("11. Top 3 favorite songs")
    print("12. Show system snapshot")
    print("13. Sort playlist")
    print("14. Run all test cases")
    print("15. Exit")

def format_duration(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"

def main():
    clear_screen()

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
        clear_screen()

        try:
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
                songs = playlist.display_playlist()
                if not songs:
                    print("Playlist is empty.")
                else:
                    for i, song in enumerate(songs):
                        print(f"{i}: {song.title} by {song.artist} ({format_duration(song.duration)})")

            elif choice == '3':
                idx = int(input("Index to delete: "))
                playlist.delete_song(idx)
                print("Song deleted.")

            elif choice == '4':
                from_idx = int(input("Move from index: "))
                to_idx = int(input("Move to index: "))
                playlist.move_song(from_idx, to_idx)
                print("Song moved.")

            elif choice == '5':
                playlist.reverse_playlist()
                print("Playlist reversed.")

            elif choice == '6':
                idx = int(input("Index to rate: "))
                rating = int(input("Rating (1–5): "))
                song = playlist.get_song(idx)
                rating_tree.insert_song(song, rating)
                print("Song rated.")

            elif choice == '7':
                idx = int(input("Index to play: "))
                song = playlist.get_song(idx)
                history.play_song(song)
                fav_queue.add_listen_time(song, song.duration)
                print(f"Played: {song.title} by {song.artist}")

            elif choice == '8':
                song = history.undo_last_play()
                if song:
                    playlist.add_song(song.title, song.artist, song.duration)
                    print("Last playback undone.")
                else:
                    print("No playback history.")

            elif choice == '9':
                cleaner.clean_playlist(playlist)
                print("Duplicates cleaned.")

            elif choice == '10':
                title = input("Song title to search: ")
                song = lookup.get_by_title(title)
                if song:
                    print(f"Found: {song.title} by {song.artist} ({format_duration(song.duration)})")
                else:
                    print("Song not found.")

            elif choice == '11':
                top = fav_queue.get_top_k_songs(3)
                if not top:
                    print("Top 3 Favorite Songs:\n(No songs have been played yet.)")
                else:
                    print("Top 3 Favorite Songs:")
                    for i, song in enumerate(top, 1):
                        print(f"{i}. {song.title} by {song.artist} ({format_duration(song.duration)})")

            elif choice == '12':
                snapshot = SystemSnapshot(playlist, history, rating_tree).export_snapshot()
                print("System Snapshot:")
                for key, value in snapshot.items():
                    print(f"{key}: {value}")

            elif choice == '13':
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

                # Overwrite playlist with sorted order
                playlist.clear_playlist()
                for song in sorted_songs:
                    playlist.add_song(song.title, song.artist, song.duration)
                print("Playlist sorted and updated.")

            elif choice == '14':
                print("Running all test cases...")
                result = subprocess.run([sys.executable, 'test_cases.py'], capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Test Errors:\n", result.stderr)

            elif choice == '15':
                print("Exiting PlayWise CLI.")
                sys.exit(0)

            else:
                print("Invalid choice. Please select a number from 1 to 15.")

        except ValueError:
            print("Invalid input. Please enter numbers where expected.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
