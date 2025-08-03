# File: core/sorting.py

def merge_sort(songs, key=None, reverse=False):
    """
    Generic merge sort implementation with key argument (like built-in sorted).
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if key is None:
        key_func = lambda x: x
    else:
        key_func = key
    if len(songs) <= 1:
        return songs

    mid = len(songs) // 2
    left = merge_sort(songs[:mid], key=key, reverse=reverse)
    right = merge_sort(songs[mid:], key=key, reverse=reverse)

    return merge(left, right, key_func, reverse)


def merge(left, right, key_func, reverse):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if reverse:
            if key_func(left[i]) > key_func(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        else:
            if key_func(left[i]) < key_func(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def sort_by_title(songs, reverse=False):
    return merge_sort(songs, key=lambda s: s.title.lower(), reverse=reverse)


def sort_by_duration(songs, reverse=False):
    return merge_sort(songs, key=lambda s: s.duration, reverse=reverse)


def sort_by_recent(songs):
    """
    Assumes songs are in order of addition.
    Reverses list to simulate recent-first.
    Time Complexity: O(n)
    """
    return list(reversed(songs))


def sort_by_recently_added(songs, reverse=False):
    """
    Sorts songs by their order in the playlist (recently added last by default).
    If songs have a 'created_at' attribute, use it; otherwise, preserve list order.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    # If Song has 'created_at', use it; else, just reverse the list for 'recently added first'
    if hasattr(songs[0], 'created_at'):
        return merge_sort(songs, key_func=lambda s: s.created_at, reverse=reverse)
    return list(reversed(songs)) if reverse else list(songs)

# Usage example for toggling criteria:
# sort_by_title(songs, reverse=False)
# sort_by_duration(songs, reverse=True)
# sort_by_recently_added(songs, reverse=True)
