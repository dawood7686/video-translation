## 2026-06-22 - Recursive SetTimeout vs Unconditional SetInterval in React
**Learning:** A recursive `setTimeout` within a `useEffect` needs an `isMounted` flag checked across try/catch/finally blocks. Without it, if the component unmounts during an in-flight async request, the finally block will schedule a new timeout that escapes the cleanup function, causing a permanent memory and network leak.
**Action:** Always include an `isMounted` check in recursive async polling patterns within React hooks.
