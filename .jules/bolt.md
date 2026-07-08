## 2024-05-19 - Inefficient AudioSegment concatenation (O(N^2))
**Learning:** In python's `pydub`, concatenating `AudioSegment` objects using `combined_audio += seg_audio` inside a loop results in O(N^2) time complexity because it creates a new `AudioSegment` copy on every iteration. This is a common performance pitfall with immutable sequence-like objects. Using `sum(list_of_segments, AudioSegment.empty())` is slightly faster, but appending to a list and summing them or using `.append(crossfade=0)` is still O(N^2) effectively.
Wait, `sum(list_of_segments, AudioSegment.empty())` is also O(N^2) in standard python sum() over immutable types, but pydub doesn't have an O(N) multi-segment concatenation built-in. However, doing a list append of the raw bytes `[seg._data for seg in list_of_segments]` and constructing a single `AudioSegment` from the combined bytes is O(N).
Let's see if pydub has an easier way. `AudioSegment.empty()` actually just has an empty string `b""` for `_data`.
Let's measure `b"".join([seg._data])`.
**Action:** Avoid `+=` in loops for `AudioSegment`s. Collect them in a list or combine raw audio data.

## 2024-07-08 - SQLAlchemy ForeignKey Indexing
**Learning:** In SQLAlchemy, `ForeignKey` columns used in queries (e.g., filtering `owner_id` in frequently polled endpoints) do not automatically generate indexes in the underlying PostgreSQL database. This can lead to slow full table scans as the dataset grows.
**Action:** Always explicitly add `index=True` to `ForeignKey` columns that are frequently used in `WHERE` clauses or joins. For existing tables, manually apply the index via a SQL script (e.g., `CREATE INDEX`).
