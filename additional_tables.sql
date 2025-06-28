-- Additional tables for the Arabic Telegram Bot
-- Run this in your Supabase SQL editor to add bot functionality tables
-- Your existing students and exam_results tables will remain unchanged

-- Enable necessary extensions if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Result cache table for API responses (optional - for external API caching)
CREATE TABLE IF NOT EXISTS result_cache (
    id BIGSERIAL PRIMARY KEY,
    examno TEXT NOT NULL UNIQUE,
    api_response JSONB NOT NULL,
    cached_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ttl INTEGER NOT NULL DEFAULT 3600,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Function to automatically calculate expires_at for result_cache
CREATE OR REPLACE FUNCTION update_result_cache_expires()
RETURNS TRIGGER AS $$
BEGIN
    NEW.expires_at := NEW.cached_at + (NEW.ttl || ' seconds')::INTERVAL;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to set expires_at on insert/update
DROP TRIGGER IF EXISTS set_result_cache_expiry ON result_cache;
CREATE TRIGGER set_result_cache_expiry
    BEFORE INSERT OR UPDATE ON result_cache
    FOR EACH ROW
    EXECUTE FUNCTION update_result_cache_expires();

-- User sessions table for bot state management
CREATE TABLE IF NOT EXISTS user_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    current_state TEXT NOT NULL DEFAULT 'main_menu',
    search_history JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Rate limiting table
CREATE TABLE IF NOT EXISTS rate_limits (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 1,
    window_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Analytics table for tracking usage
CREATE TABLE IF NOT EXISTS analytics (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    action TEXT NOT NULL,
    search_type TEXT,
    search_term TEXT,
    success BOOLEAN DEFAULT true,
    response_time_ms INTEGER,
    shard_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance on your existing tables
-- (Only run if these indexes don't already exist)
CREATE INDEX IF NOT EXISTS idx_students_aname ON students USING gin(aname gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_students_examno ON students(examno);
CREATE INDEX IF NOT EXISTS idx_students_gov_name ON students(gov_name);
CREATE INDEX IF NOT EXISTS idx_students_aname_gov ON students(aname, gov_name);

CREATE INDEX IF NOT EXISTS idx_exam_results_examno ON exam_results(examno);

-- Indexes for new tables
CREATE INDEX IF NOT EXISTS idx_result_cache_examno ON result_cache(examno);
CREATE INDEX IF NOT EXISTS idx_result_cache_expires ON result_cache(expires_at);

CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_updated ON user_sessions(updated_at);

CREATE INDEX IF NOT EXISTS idx_rate_limits_user_id ON rate_limits(user_id);
CREATE INDEX IF NOT EXISTS idx_rate_limits_window ON rate_limits(window_start);

CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_created_at ON analytics(created_at);
CREATE INDEX IF NOT EXISTS idx_analytics_action ON analytics(action);

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for updating timestamps on user_sessions
DROP TRIGGER IF EXISTS update_user_sessions_updated_at ON user_sessions;
CREATE TRIGGER update_user_sessions_updated_at 
    BEFORE UPDATE ON user_sessions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to clean expired cache entries
CREATE OR REPLACE FUNCTION clean_expired_cache()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM result_cache WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to clean old rate limit entries
CREATE OR REPLACE FUNCTION clean_old_rate_limits()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM rate_limits WHERE window_start < NOW() - INTERVAL '1 hour';
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function for fuzzy name search (works with your existing students table)
CREATE OR REPLACE FUNCTION search_students_fuzzy(
    search_name TEXT,
    gov_filter TEXT DEFAULT NULL,
    result_limit INTEGER DEFAULT 5,
    result_offset INTEGER DEFAULT 0
)
RETURNS TABLE(
    id BIGINT,
    examno TEXT,
    aname TEXT,
    gov_name TEXT,
    gov_code TEXT,
    sch_name TEXT,
    sch_code TEXT,
    sexcode TEXT,
    accname TEXT,
    similarity_score REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.examno,
        s.aname,
        s.gov_name,
        s.gov_code,
        s.sch_name,
        s.sch_code,
        s.sexcode,
        s.accname,
        similarity(s.aname, search_name) as similarity_score
    FROM students s
    WHERE 
        (gov_filter IS NULL OR s.gov_name = gov_filter)
        AND s.aname IS NOT NULL
        AND (
            s.aname ILIKE '%' || search_name || '%' 
            OR similarity(s.aname, search_name) > 0.3
        )
    ORDER BY 
        similarity(s.aname, search_name) DESC,
        s.aname
    LIMIT result_limit 
    OFFSET result_offset;
END;
$$ LANGUAGE plpgsql;

-- Create a view for easy student result lookup (using your existing tables)
CREATE OR REPLACE VIEW student_results AS
SELECT 
    s.id,
    s.examno,
    s.aname,
    s.gov_name,
    s.gov_code,
    s.sch_name,
    s.sch_code,
    s.sexcode,
    s.accname,
    er.stucases,
    er.finalgrd,
    er.finalrate,
    er.sub1_name, er.sub1_score, er.sub1_cscore,
    er.sub2_name, er.sub2_score, er.sub2_cscore,
    er.sub3_name, er.sub3_score, er.sub3_cscore,
    er.sub4_name, er.sub4_score, er.sub4_cscore,
    er.sub5_name, er.sub5_score, er.sub5_cscore,
    er.sub6_name, er.sub6_score, er.sub6_cscore,
    er.sub7_name, er.sub7_score, er.sub7_cscore,
    er.sub8_name, er.sub8_score, er.sub8_cscore,
    er.sub9_name, er.sub9_score, er.sub9_cscore
FROM students s
LEFT JOIN exam_results er ON s.examno = er.examno;

COMMENT ON TABLE result_cache IS 'Cache for external API responses';
COMMENT ON TABLE user_sessions IS 'Bot user session management';
COMMENT ON TABLE rate_limits IS 'Rate limiting per user';
COMMENT ON TABLE analytics IS 'Usage analytics and monitoring';
COMMENT ON VIEW student_results IS 'Combined view of students and their exam results';