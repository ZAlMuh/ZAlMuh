-- YNA Database Schema
-- Run this in your Supabase SQL editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table (extends auth.users)
CREATE TABLE IF NOT EXISTS public.users (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL DEFAULT 'author' CHECK (role IN ('admin', 'editor', 'author')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create posts table
CREATE TABLE IF NOT EXISTS public.posts (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  slug TEXT NOT NULL UNIQUE,
  title_en TEXT NOT NULL,
  title_ar TEXT NOT NULL,
  content_en TEXT NOT NULL,
  content_ar TEXT NOT NULL,
  excerpt_en TEXT,
  excerpt_ar TEXT,
  category TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}',
  cover_image TEXT,
  views INTEGER DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('published', 'draft')),
  featured BOOLEAN DEFAULT FALSE,
  author_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create messages table (contact form submissions)
CREATE TABLE IF NOT EXISTS public.messages (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create site_stats table for analytics
CREATE TABLE IF NOT EXISTS public.site_stats (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
  view_count INTEGER DEFAULT 1,
  date DATE DEFAULT CURRENT_DATE
);

-- Create settings table
CREATE TABLE IF NOT EXISTS public.settings (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  key TEXT NOT NULL UNIQUE,
  value TEXT NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_posts_status ON public.posts(status);
CREATE INDEX IF NOT EXISTS idx_posts_category ON public.posts(category);
CREATE INDEX IF NOT EXISTS idx_posts_featured ON public.posts(featured);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON public.posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_slug ON public.posts(slug);
CREATE INDEX IF NOT EXISTS idx_site_stats_post_id ON public.site_stats(post_id);
CREATE INDEX IF NOT EXISTS idx_site_stats_date ON public.site_stats(date);

-- Create full-text search indexes
CREATE INDEX IF NOT EXISTS idx_posts_search_en ON public.posts USING gin(to_tsvector('english', title_en || ' ' || content_en));
CREATE INDEX IF NOT EXISTS idx_posts_search_ar ON public.posts USING gin(to_tsvector('arabic', title_ar || ' ' || content_ar));

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_posts_updated_at BEFORE UPDATE ON public.posts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_settings_updated_at BEFORE UPDATE ON public.settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to increment post views
CREATE OR REPLACE FUNCTION increment_post_views(post_id UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE public.posts 
  SET views = views + 1 
  WHERE id = post_id;
  
  INSERT INTO public.site_stats (post_id, view_count, date)
  VALUES (post_id, 1, CURRENT_DATE)
  ON CONFLICT (post_id, date) 
  DO UPDATE SET view_count = site_stats.view_count + 1;
END;
$$ LANGUAGE plpgsql;

-- Row Level Security (RLS) Policies

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.site_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.settings ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can view their own profile" ON public.users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON public.users
  FOR UPDATE USING (auth.uid() = id);

-- Posts policies
CREATE POLICY "Anyone can view published posts" ON public.posts
  FOR SELECT USING (status = 'published');

CREATE POLICY "Authenticated users can view all posts" ON public.posts
  FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Authors can insert their own posts" ON public.posts
  FOR INSERT WITH CHECK (auth.uid() = author_id);

CREATE POLICY "Authors can update their own posts" ON public.posts
  FOR UPDATE USING (auth.uid() = author_id);

CREATE POLICY "Authors can delete their own posts" ON public.posts
  FOR DELETE USING (auth.uid() = author_id);

-- Messages policies (contact form)
CREATE POLICY "Anyone can insert messages" ON public.messages
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Only authenticated users can view messages" ON public.messages
  FOR SELECT USING (auth.role() = 'authenticated');

-- Site stats policies
CREATE POLICY "Anyone can view site stats" ON public.site_stats
  FOR SELECT USING (true);

CREATE POLICY "System can insert site stats" ON public.site_stats
  FOR INSERT WITH CHECK (true);

-- Settings policies
CREATE POLICY "Anyone can view settings" ON public.settings
  FOR SELECT USING (true);

CREATE POLICY "Only authenticated users can modify settings" ON public.settings
  FOR ALL USING (auth.role() = 'authenticated');

-- Insert default settings
INSERT INTO public.settings (key, value) VALUES
  ('maintenance_mode', 'false'),
  ('default_language', 'en'),
  ('site_title_en', 'Youth News Agency'),
  ('site_title_ar', 'وكالة أنباء الشباب'),
  ('site_description_en', 'Latest news and insights from a youth perspective'),
  ('site_description_ar', 'آخر الأخبار والرؤى من منظور الشباب')
ON CONFLICT (key) DO NOTHING;

-- Create a function to handle new user creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, full_name, email, role)
  VALUES (NEW.id, NEW.raw_user_meta_data->>'full_name', NEW.email, 'author');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create user profile on signup
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();