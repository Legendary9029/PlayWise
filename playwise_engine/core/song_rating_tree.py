# File: core/song_rating_tree.py

from models.song import Song

class RatingNode:
    def __init__(self, rating):
        self.rating = rating                # Rating from 1 to 5
        self.songs = []                     # List of Song objects
        self.left = None                    # Left child
        self.right = None                   # Right child

class SongRatingTree:
    def __init__(self):
        self.root = None

    def insert_song(self, song, rating):
        """
        Inserts a song into the BST based on its rating.
        Time Complexity: O(log r) where r = number of unique rating nodes (≤ 5)
        Space Complexity: O(1) per insert
        """
        def insert(node, rating):
            if not node:
                new_node = RatingNode(rating)
                new_node.songs.append(song)
                return new_node
            if rating < node.rating:
                node.left = insert(node.left, rating)
            elif rating > node.rating:
                node.right = insert(node.right, rating)
            else:
                node.songs.append(song)
            return node
        self.root = insert(self.root, rating)

    def search_by_rating(self, rating):
        """
        Returns list of songs with the specified rating.
        Time Complexity: O(log r)
        Space Complexity: O(1)
        """
        current = self.root
        while current:
            if rating < current.rating:
                current = current.left
            elif rating > current.rating:
                current = current.right
            else:
                return current.songs
        return []

    def delete_song(self, song_id):
        """
        Deletes a song from the tree by song_id.
        Time Complexity: O(r * s) worst case, where s is avg. songs per rating bucket
        Space Complexity: O(1)
        """
        def delete_from_bucket(node):
            if not node:
                return
            # Remove song from this bucket if exists
            node.songs = [s for s in node.songs if s.song_id != song_id]
            delete_from_bucket(node.left)
            delete_from_bucket(node.right)
        delete_from_bucket(self.root)

    def in_order_traversal(self):
        """
        For debugging or dashboard: Returns all songs sorted by rating.
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        result = []
        def traverse(node):
            if not node:
                return
            traverse(node.left)
            result.extend(node.songs)
            traverse(node.right)
        traverse(self.root)
        return result
