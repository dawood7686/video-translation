## 2024-06-22 - Form Accessibility & Interaction Feedback
**Learning:** Found placeholder-only inputs and missing async feedback in authentication forms. Placeholders are insufficient for screen readers and disappear on typing, while lack of loading states leaves users unsure if their submission is processing.
**Action:** Always pair inputs with `<label>` tags (use `sr-only` class if visually hidden) connected via `htmlFor` and `id`. Additionally, always implement disabled states and visual text changes (e.g., "Signing in...") for submit buttons during async operations.
