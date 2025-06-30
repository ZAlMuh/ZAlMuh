-- Arabic Telegram Bot Database Schema for Supabase
-- Run this in your Supabase SQL editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id BIGSERIAL PRIMARY KEY,
    aname TEXT NOT NULL,
    examno TEXT UNIQUE NOT NULL,
    sch_name TEXT NOT NULL,
    gov_name TEXT NOT NULL,
    gender TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Exam results table
CREATE TABLE IF NOT EXISTS exam_results (
    id BIGSERIAL PRIMARY KEY,
    examno TEXT NOT NULL REFERENCES students(examno) ON DELETE CASCADE,
    subject_scores JSONB NOT NULL DEFAULT '{}',
    total INTEGER NOT NULL DEFAULT 0,
    average DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    status TEXT NOT NULL DEFAULT 'غير متوفر',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(examno)
);

-- Result cache table for API responses
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

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_students_aname ON students USING gin(aname gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_students_examno ON students(examno);
CREATE INDEX IF NOT EXISTS idx_students_gov_name ON students(gov_name);
CREATE INDEX IF NOT EXISTS idx_students_aname_gov ON students(aname, gov_name);

CREATE INDEX IF NOT EXISTS idx_exam_results_examno ON exam_results(examno);

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

-- Triggers for updating timestamps
CREATE TRIGGER update_students_updated_at 
    BEFORE UPDATE ON students 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_exam_results_updated_at 
    BEFORE UPDATE ON exam_results 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

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

-- Function for fuzzy name search
CREATE OR REPLACE FUNCTION search_students_fuzzy(
    search_name TEXT,
    gov_filter TEXT DEFAULT NULL,
    result_limit INTEGER DEFAULT 5,
    result_offset INTEGER DEFAULT 0
)
RETURNS TABLE(
    id BIGINT,
    aname TEXT,
    examno TEXT,
    sch_name TEXT,
    gov_name TEXT,
    gender TEXT,
    similarity_score REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.aname,
        s.examno,
        s.sch_name,
        s.gov_name,
        s.gender,
        similarity(s.aname, search_name) as similarity_score
    FROM students s
    WHERE 
        (gov_filter IS NULL OR s.gov_name = gov_filter)
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

-- Sample data insertion (for testing)
-- Uncomment and modify as needed

/*
INSERT INTO students (aname, examno, sch_name, gov_name, gender) VALUES
('عبدالله بهاء رزاق', '272591110430082', 'متوسطة مؤمن قريش للبنين', 'كربلاء', 'ذكر'),
('فاطمة أحمد علي', '272591110430083', 'متوسطة الزهراء للبنات', 'بغداد', 'أنثى'),
('محمد حسن جعفر', '272591110430084', 'إعدادية الكوثر للبنين', 'النجف', 'ذكر'),
('زينب محمد كاظم', '272591110430085', 'إعدادية فاطمة الزهراء', 'كربلاء', 'أنثى'),
('علي حسين محمد', '272591110430086', 'ثانوية الإمام علي', 'البصرة', 'ذكر');

INSERT INTO exam_results (examno, subject_scores, total, average, status) VALUES
('272591110430082', '{"الاسلامية": 85, "العربية": 77, "الانكليزية": 76, "الرياضيات": 81, "الفيزياء": 78, "الكيمياء": 80, "الاحياء": 82}', 559, 79.86, 'ناجح'),
('272591110430083', '{"الاسلامية": 90, "العربية": 88, "الانكليزية": 85, "الرياضيات": 87, "الفيزياء": 83, "الكيمياء": 86, "الاحياء": 89}', 608, 86.86, 'ناجح'),
('272591110430084', '{"الاسلامية": 75, "العربية": 70, "الانكليزية": 65, "الرياضيات": 68, "الفيزياء": 72, "الكيمياء": 69, "الاحياء": 71}', 490, 70.00, 'ناجح'),
('272591110430085', '{"الاسلامية": 92, "العربية": 89, "الانكليزية": 87, "الرياضيات": 90, "الفيزياء": 85, "الكيمياء": 88, "الاحياء": 91}', 622, 88.86, 'ناجح'),
('272591110430086', '{"الاسلامية": 65, "العربية": 62, "الانكليزية": 58, "الرياضيات": 60, "الفيزياء": 55, "الكيمياء": 59, "الاحياء": 61}', 420, 60.00, 'راسب');
*/

-- Create a view for easy student result lookup
CREATE OR REPLACE VIEW student_results AS
SELECT 
    s.id,
    s.aname,
    s.examno,
    s.sch_name,
    s.gov_name,
    s.gender,
    er.subject_scores,
    er.total,
    er.average,
    er.status,
    s.created_at,
    er.updated_at as result_updated_at
FROM students s
LEFT JOIN exam_results er ON s.examno = er.examno;

-- Performance optimization: Create covering indexes
CREATE INDEX IF NOT EXISTS idx_students_covering ON students(gov_name, aname) INCLUDE (examno, sch_name, gender);

COMMENT ON TABLE students IS 'Student information table';
COMMENT ON TABLE exam_results IS 'Exam results with subject scores';
COMMENT ON TABLE result_cache IS 'Cache for external API responses';
COMMENT ON TABLE user_sessions IS 'Bot user session management';
COMMENT ON TABLE rate_limits IS 'Rate limiting per user';
COMMENT ON TABLE analytics IS 'Usage analytics and monitoring';

-- Grant necessary permissions (adjust as needed for your Supabase setup)
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;