## 2024-06-25 - Unconditional React Effect Polling Anti-Pattern
**Learning:** Found a common anti-pattern where a `setInterval` was placed unconditionally inside a `useEffect` on the dashboard to check status. This leads to continuous backend requests even when there is no active job, significantly wasting bandwidth and server resources.
**Action:** When implementing polling, always split the initial fetch and the polling logic. Only initiate the polling interval if the frontend state explicitly dictates that a background process is incomplete (e.g., jobs in a pending/processing status).
