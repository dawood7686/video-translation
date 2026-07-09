## 2024-06-21 - Path Traversal Vulnerability in Video Upload
**Vulnerability:** The application was vulnerable to path traversal during file uploads. It blindly trusted `file.filename` provided by the client, taking the extension via `file.filename.split(".")[-1]` and directly concatenating it into the `original_video_key` for MinIO storage without sanitization. An attacker could provide a crafted filename like `evil.mp4/../../../../etc/passwd`, causing the `original_video_key` to contain path traversal sequences that could allow unauthorized file writing in the storage backend or local filesystem depending on how MinIO resolves it, and also polluting the database with a malicious string in the `title` and `original_filename` fields.
**Learning:** Never trust client-provided input, especially filenames. We must always sanitize filenames before using them to construct paths or storage keys, and ensure any derived components (like file extensions) are strictly validated.
**Prevention:** Always use `os.path.basename()` to strip off any directory paths from the filename provided by the client. Additionally, ensure the parsed file extension contains only expected characters (e.g., alphanumeric) to prevent injection of special characters.

## 2024-06-24 - Information Disclosure in Background Tasks
**Vulnerability:** Background workers caught generic exceptions and saved the raw `str(e)` payload directly to the database. The public API endpoints then blindly mapped and returned this error_message field. This risks leaking internal environment specifics, database URIs, API keys, or exact internal paths if third-party libraries fail verbosely.
**Learning:** Architectural boundaries must be respected. Just because an error is caught in a background worker doesn't mean it's safe to present to the end-user. Data bound for the frontend should always be considered untrusted and sanitized, or generically mapped, even if it originates internally.
**Prevention:** Catch blocks in background processors should log the raw stack trace/error securely on the server-side, and only write safe, generic error strings to any status fields that are eventually serialized back to clients.

## 2026-07-09 - Missing Input Validation on Video Uploads
**Vulnerability:** The `/upload` endpoint lacked file size and content type validation, allowing arbitrary file uploads and potential DoS via massive file processing.
**Learning:** FastAPI `UploadFile` relies on client-side headers unless explicitly validated. MinIO and Celery processing would blindly accept and process any file, consuming unbounded resources.
**Prevention:** Always manually validate `file.content_type` and enforce strict size limits via `file.file.seek(0, 2)` before passing files to storage or background workers.
