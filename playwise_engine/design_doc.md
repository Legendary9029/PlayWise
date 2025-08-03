```
add_song(title, artist, duration):
    node = new Node(Song(...))
    if tail is None:
        head = tail = node
    else:
        tail.next = node
        node.prev = tail
        tail = node

move_song(from_idx, to_idx):
    node = get_node(from_idx)
    detach node
    insert at to_idx

reverse_playlist():
    curr = head
    while curr:
        swap curr.next and curr.prev
        curr = curr.prev
    swap head and tail
```

### Rating Tree Insert/Search
```
insert_song(song, rating):
    if root is None:
        root = new Node(rating)
    traverse BST to rating node
    add song to node.songs

search_by_rating(rating):
    traverse BST to rating node
    return node.songs
```

### Duplicate Cleaner
```
for song in playlist:
    key = (title.lower(), artist.lower())
    if key in seen:
        remove song
    else:
        seen.add(key)
```

## 4. Example Diagrams

### Playlist Engine (Doubly Linked List)

    [head] <-> [Song1] <-> [Song2] <-> [tail]

### Song Rating Tree (BST with Buckets)

         [3]
        /   \
     [2]     [5]
             /
           [4]

## 5. Benchmarks / Test Results

- All core and specialized features are covered by unit tests in `test_cases.py`.
- Example: Playlist add/reverse, rating tree search, duplicate cleaning, favorite queue, and dashboard snapshot all pass.

## 6. Extensibility
- Add new analytics in `system_snapshot.py`.
- Add new data structures in `core/` or `specialized/`.
- Write new tests in `test_cases.py`.

---
# PlayWise Engine: Technical Design Document

## 1. High-Level Architecture

```
[User Actions]
     |
     v
[Playlist Engine] <-> [Instant Lookup]
     |                    |
     v                    v
[Playback History]   [Song Rating Tree]
     |                    |
     v                    v
[System Snapshot] <-> [Sorting]
     |
     v
[Specialized: Duplicate Cleaner, Favorite Queue]
```

- **Playlist Engine:** Doubly linked list for efficient add, delete, move, reverse.
- **Playback History:** Stack for undo/redo of recent plays.
- **Song Rating Tree:** BST with buckets for fast rating-based queries.
- **Instant Lookup:** HashMap for O(1) song search by ID/title.
- **Sorting:** Merge sort for custom criteria (title, duration, recent).
- **System Snapshot:** Aggregates stats for dashboard.
- **Specialized:** Duplicate removal (HashSet), favorite queue (Heap).

## 2. Data Structure & Algorithm Trade-offs

| Feature                | Structure      | Why? (Trade-off)                                  |
|------------------------|---------------|---------------------------------------------------|
| Playlist               | Doubly Linked | O(1) add/delete/move, bidirectional traversal      |
| Playback History       | Stack         | O(1) undo, simple LIFO                            |
| Song Rating            | BST w/ Buckets| O(log r) search, fast rating queries, extensible   |
| Instant Lookup         | HashMap       | O(1) search, sync with playlist                   |
| Sorting                | Merge Sort    | Stable, O(n log n), custom key support            |
| Duplicate Cleaner      | HashSet       | O(1) duplicate check, composite key                |
| Favorite Queue         | Max-Heap      | O(log n) insert, O(1) top-k retrieval             |

## 3. Pseudocode for Major Algorithms

### Playlist Add/Move/Reverse

