## 2024-06-20 - Unnecessary API Polling
**Learning:** Polling loops in components can cause significant server load if not conditioned on application state. The dashboard was polling for video status even when all videos were in terminal states (completed/failed).
**Action:** Always condition polling mechanisms on the presence of active, pending, or processing tasks to avoid unnecessary network requests.

## 2024-08-01 - Missing Database Index on Foreign Key Polled Frequently
**Learning:** SQLAlchemy (and underlying databases like PostgreSQL) does not automatically create indexes on Foreign Key columns. For endpoints that are polled frequently by the frontend (like checking video status by `owner_id`), a missing index on the foreign key results in repeated full table scans, causing unnecessary database load and degraded performance as the table grows.
**Action:** Always explicitly add `index=True` to SQLAlchemy `Column` definitions that are used for filtering in frequently hit or polled endpoints, especially foreign keys representing relationships (e.g., `owner_id`).
