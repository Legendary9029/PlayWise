# File: core/optimization.py

"""
This module supports optimization logic and centralizes time/space annotations.
It is not required to implement lazy strategies directly, but suggestions and structure are provided.
"""

def annotate_complexity(func):
    """
    Decorator to attach complexity annotations to a function.
    """
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.time_complexity = getattr(func, 'time_complexity', 'O(?)')
    wrapper.space_complexity = getattr(func, 'space_complexity', 'O(?)')
    return wrapper


# Example Optimization Suggestion: Constant-Time Swap

def swap_nodes(node1, node2):
    """
    Swaps two song nodes in constant time (assuming double-linked list).
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    if node1 == node2:
        return

    # Swap song references instead of node pointers
    node1.song, node2.song = node2.song, node1.song


# Example Optimization Suggestion: Lazy Reversal
class LazyReversiblePlaylist:
    def __init__(self):
        self.reversed_flag = False
        self.songs = []  # could be actual nodes in future

    def add(self, song):
        if self.reversed_flag:
            self.songs.insert(0, song)
        else:
            self.songs.append(song)

    def reverse(self):
        self.reversed_flag = not self.reversed_flag

    def get_all(self):
        return self.songs[::-1] if self.reversed_flag else self.songs
