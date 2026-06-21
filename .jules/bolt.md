## 2024-10-25 - Conditional Recursive Timeout Polling
**Learning:** The dashboard previously used unconditional `setInterval` polling every 10 seconds, creating unnecessary continuous load on the backend even when no tasks were pending. Furthermore, `setInterval` could lead to overlapping network requests if a slow backend takes longer than the interval.
**Action:** Replace `setInterval` with conditional recursive `setTimeout` pattern. This guarantees non-overlapping requests, and polling naturally stops when all background tasks reach a terminal state, vastly reducing server strain.
