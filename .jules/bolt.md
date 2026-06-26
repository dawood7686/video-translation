## 2024-06-20 - Unnecessary API Polling
**Learning:** Polling loops in components can cause significant server load if not conditioned on application state. The dashboard was polling for video status even when all videos were in terminal states (completed/failed).
**Action:** Always condition polling mechanisms on the presence of active, pending, or processing tasks to avoid unnecessary network requests.

## 2024-06-26 - Missing Indexes on Foreign Keys
**Learning:** In PostgreSQL, foreign keys defined via SQLAlchemy `ForeignKey` do not automatically get indexes. This leads to O(N) sequential scans when filtering relations (e.g., fetching a user's videos) causing performance to degrade as the table grows.
**Action:** Always add `index=True` to SQLAlchemy columns that represent foreign keys if they are frequently used in filtering or joins.
