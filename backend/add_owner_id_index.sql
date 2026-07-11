-- ⚡ Bolt Optimization: Add index to owner_id to prevent full table scans during polling
CREATE INDEX IF NOT EXISTS ix_videos_owner_id ON videos (owner_id);
