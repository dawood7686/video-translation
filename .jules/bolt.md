## 2024-05-19 - Inefficient AudioSegment concatenation (O(N^2))
**Learning:** In python's `pydub`, concatenating `AudioSegment` objects using `combined_audio += seg_audio` inside a loop results in O(N^2) time complexity because it creates a new `AudioSegment` copy on every iteration. This is a common performance pitfall with immutable sequence-like objects. Using `sum(list_of_segments, AudioSegment.empty())` is slightly faster, but appending to a list and summing them or using `.append(crossfade=0)` is still O(N^2) effectively.
Wait, `sum(list_of_segments, AudioSegment.empty())` is also O(N^2) in standard python sum() over immutable types, but pydub doesn't have an O(N) multi-segment concatenation built-in. However, doing a list append of the raw bytes `[seg._data for seg in list_of_segments]` and constructing a single `AudioSegment` from the combined bytes is O(N).
Let's see if pydub has an easier way. `AudioSegment.empty()` actually just has an empty string `b""` for `_data`.
Let's measure `b"".join([seg._data])`.
**Action:** Avoid `+=` in loops for `AudioSegment`s. Collect them in a list or combine raw audio data.

## 2026-07-03 - Missing Index on SQLAlchemy ForeignKey
**Learning:** In SQLAlchemy, explicitly add `index=True` to `ForeignKey` columns used in queries (e.g., filtering in frequently polled endpoints), as they do not automatically generate indexes in the underlying PostgreSQL database, which can lead to slow full table scans.
**Action:** Always add `index=True` to `ForeignKey` columns if they are frequently used in WHERE clauses or JOINs to prevent performance degradation on large datasets.
