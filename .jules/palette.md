## 2026-06-27 - Loading state disabled buttons
**Learning:** Auth forms lacked disabled loading states leading to duplicate request potentials, and `role="alert"` missing on error popups.
**Action:** Always add an `isLoading` boolean bound to form submit disabling logic, and append `role="alert"` to dynamically conditionally rendered errors across all Next.js applications in this repo.
