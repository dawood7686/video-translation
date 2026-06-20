## 2024-06-20 - Unnecessary API Polling
**Learning:** Polling loops in components can cause significant server load if not conditioned on application state. The dashboard was polling for video status even when all videos were in terminal states (completed/failed).
**Action:** Always condition polling mechanisms on the presence of active, pending, or processing tasks to avoid unnecessary network requests.
