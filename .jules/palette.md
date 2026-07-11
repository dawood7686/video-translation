## 2026-07-11 - Standardize auth forms accessibility and loading states
**Learning:** Forms within the frontend design system can have inconsistent accessibility implementations between sibling components (e.g., login having loading states and labels, while signup lacked them).
**Action:** When adding or modifying a form component, consistently cross-reference sibling components to ensure standardized accessibility practices (like `sr-only` labels, linked `id`s, and `role="alert"` for errors) and interaction feedback (like disabled/loading states) are maintained.
