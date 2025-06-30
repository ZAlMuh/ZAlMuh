import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types
export interface Post {
  id: string
  slug: string
  title_en: string
  title_ar: string
  content_en: string
  content_ar: string
  excerpt_en?: string
  excerpt_ar?: string
  category: string
  tags: string[]
  cover_image?: string
  views: number
  status: 'published' | 'draft'
  featured: boolean
  author_id: string
  created_at: string
  updated_at: string
}

export interface Message {
  id: string
  name: string
  email: string
  message: string
  created_at: string
}

export interface User {
  id: string
  full_name: string
  email: string
  role: 'admin' | 'editor' | 'author'
  created_at: string
}

export interface SiteStats {
  id: string
  post_id: string
  view_count: number
  date: string
}

export interface Settings {
  id: string
  key: string
  value: string
  updated_at: string
}

// Helper functions for database operations
export const dbOperations = {
  // Posts
  async getPosts(limit = 10, offset = 0, status = 'published') {
    try {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .eq('status', status)
        .order('created_at', { ascending: false })
        .range(offset, offset + limit - 1)
      
      if (error) {
        if (error.message.includes('relation "posts" does not exist')) {
          return []
        }
        throw error
      }
      return data || []
    } catch (error) {
      console.warn('Posts table not found, returning empty array')
      return []
    }
  },

  async getPostBySlug(slug: string) {
    try {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .eq('slug', slug)
        .single()
      
      if (error) {
        if (error.message.includes('relation "posts" does not exist')) {
          return null
        }
        throw error
      }
      return data
    } catch (error) {
      console.warn('Posts table not found')
      return null
    }
  },

  async getPostsByCategory(category: string, limit = 10) {
    try {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .eq('category', category)
        .eq('status', 'published')
        .order('created_at', { ascending: false })
        .limit(limit)
      
      if (error) {
        if (error.message.includes('relation "posts" does not exist')) {
          return []
        }
        throw error
      }
      return data || []
    } catch (error) {
      console.warn('Posts table not found, returning empty array')
      return []
    }
  },

  async searchPosts(query: string, limit = 10) {
    try {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .or(`title_en.ilike.%${query}%,title_ar.ilike.%${query}%,content_en.ilike.%${query}%,content_ar.ilike.%${query}%`)
        .eq('status', 'published')
        .order('created_at', { ascending: false })
        .limit(limit)
      
      if (error) {
        if (error.message.includes('relation "posts" does not exist')) {
          return []
        }
        throw error
      }
      return data || []
    } catch (error) {
      console.warn('Posts table not found, returning empty array')
      return []
    }
  },

  async getFeaturedPosts(limit = 5) {
    try {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .eq('featured', true)
        .eq('status', 'published')
        .order('created_at', { ascending: false })
        .limit(limit)
      
      if (error) {
        if (error.message.includes('relation "posts" does not exist')) {
          return []
        }
        throw error
      }
      return data || []
    } catch (error) {
      console.warn('Posts table not found, returning empty array')
      return []
    }
  },

  async incrementPostViews(postId: string) {
    const { error } = await supabase.rpc('increment_post_views', {
      post_id: postId
    })
    
    if (error) throw error
  },

  // Messages
  async createMessage(message: Omit<Message, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('messages')
      .insert([message])
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  async getMessages(limit = 50) {
    const { data, error } = await supabase
      .from('messages')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit)
    
    if (error) throw error
    return data
  },

  // Settings
  async getSetting(key: string) {
    const { data, error } = await supabase
      .from('settings')
      .select('value')
      .eq('key', key)
      .single()
    
    if (error) throw error
    return data?.value
  },

  async setSetting(key: string, value: string) {
    const { error } = await supabase
      .from('settings')
      .upsert({ key, value, updated_at: new Date().toISOString() })
    
    if (error) throw error
  },

  // Analytics
  async getPostAnalytics(days = 30) {
    const { data, error } = await supabase
      .from('site_stats')
      .select('*')
      .gte('date', new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString())
      .order('date', { ascending: true })
    
    if (error) throw error
    return data
  },

  async getTotalViews() {
    const { data, error } = await supabase
      .from('posts')
      .select('views')
    
    if (error) throw error
    return data.reduce((total, post) => total + post.views, 0)
  }
}