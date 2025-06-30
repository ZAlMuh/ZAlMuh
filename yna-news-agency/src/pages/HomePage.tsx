import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { useLanguage } from '@/contexts/LanguageContext'
import { dbOperations } from '@/lib/supabase'
import type { Post } from '@/lib/supabase'
import Layout from '@/components/layout/Layout'
import PostCard from '@/components/common/PostCard'
import Loading from '@/components/common/Loading'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

const HomePage: React.FC = () => {
  const { t } = useTranslation()
  const { language } = useLanguage()
  const [featuredPosts, setFeaturedPosts] = useState<Post[]>([])
  const [latestPosts, setLatestPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true)
        const [featured, latest] = await Promise.all([
          dbOperations.getFeaturedPosts(3),
          dbOperations.getPosts(8)
        ])
        setFeaturedPosts(featured || [])
        setLatestPosts(latest || [])
      } catch (err) {
        console.error('Error fetching posts:', err)
        // Don't show error for empty database, just show empty state
        const errorMessage = err instanceof Error ? err.message : String(err)
        if (errorMessage?.includes('relation "posts" does not exist') || 
            errorMessage?.includes('Missing table definition')) {
          setFeaturedPosts([])
          setLatestPosts([])
        } else {
          setError(t('error-occurred'))
        }
      } finally {
        setLoading(false)
      }
    }

    fetchPosts()
  }, [t])

  const categories = [
    'Politics', 'Technology', 'Sports', 'Culture', 'Environment', 'Education'
  ]

  if (loading) {
    return (
      <Layout>
        <div className="min-h-[60vh] flex items-center justify-center">
          <Loading size="lg" />
        </div>
      </Layout>
    )
  }

  if (error) {
    return (
      <Layout>
        <div className="min-h-[60vh] flex items-center justify-center">
          <div className="text-center rtl:text-right space-y-4">
            <p className="text-muted-foreground">{error}</p>
            <Button onClick={() => window.location.reload()}>
              {t('try-again')}
            </Button>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      {/* Hero Section */}
      <section className="space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center rtl:text-right space-y-6"
        >
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold">
            <span className="yna-gradient bg-clip-text text-transparent">
              {t('youth-news-agency')}
            </span>
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground leading-relaxed max-w-4xl mx-auto rtl:mr-0">
            {language === 'ar' 
              ? 'آخر الأخبار والرؤى من منظور الشباب - نحن نغطي ما يهم الجيل الجديد'
              : 'Latest news and insights from a youth perspective - covering what matters to the new generation'
            }
          </p>
          <div className="flex gap-4 justify-center rtl:justify-start flex-wrap items-center">
            <Button size="lg" className="btn-accent">
              {t('latest-news')}
            </Button>
            <Button variant="outline" size="lg">
              {t('about')}
            </Button>
          </div>
        </motion.div>
      </section>

      {/* Categories */}
      <section className="space-y-6">
        <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide rtl:flex-row-reverse">
          {categories.map((category) => (
            <Badge
              key={category}
              variant="outline"
              className="whitespace-nowrap cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors"
            >
              {category}
            </Badge>
          ))}
        </div>
      </section>

      {/* Featured Posts */}
      {featuredPosts.length > 0 && (
        <section className="space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="space-y-6"
          >
            <h2 className="text-2xl md:text-3xl font-semibold rtl:text-right">
              {t('featured-posts')}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredPosts.map((post, index) => (
                <motion.div
                  key={post.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.1 * index }}
                >
                  <PostCard post={post} variant="featured" />
                </motion.div>
              ))}
            </div>
          </motion.div>
        </section>
      )}

      {/* Empty State */}
      {!loading && featuredPosts.length === 0 && latestPosts.length === 0 && !error && (
        <section className="space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="bg-white dark:bg-gray-900 rounded-xl shadow-lg p-8 md:p-12 text-center rtl:text-right space-y-6"
          >
            <div className="w-20 h-20 mx-auto rtl:mr-0 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
              <span className="text-2xl font-bold text-white">YNA</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-bold">
              {language === 'ar' ? 'مرحباً بكم في وكالة أنباء الشباب!' : 'Welcome to Youth News Agency!'}
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed max-w-2xl mx-auto rtl:mr-0">
              {language === 'ar' 
                ? 'نحن نعمل على إعداد المحتوى الأول لكم. تابعونا قريباً للحصول على آخر الأخبار والمقالات المثيرة!'
                : 'We\'re preparing our first content for you. Stay tuned for the latest news and exciting articles!'
              }
            </p>
            <div className="flex gap-4 justify-center rtl:justify-start flex-wrap items-center">
              <Button size="lg" className="btn-accent" onClick={() => window.location.href = '/about'}>
                {t('about')}
              </Button>
              <Button variant="outline" size="lg" onClick={() => window.location.href = '/contact'}>
                {t('contact-us')}
              </Button>
            </div>
          </motion.div>
        </section>
      )}

      {/* Latest Posts */}
      <section className="space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="space-y-6"
        >
          <div className="flex justify-between items-center flex-wrap gap-4 rtl:flex-row-reverse">
            <h2 className="text-2xl md:text-3xl font-semibold rtl:text-right">
              {t('latest-news')}
            </h2>
            <Button variant="outline">
              {language === 'ar' ? 'عرض الكل' : 'View All'}
            </Button>
          </div>
          
          {latestPosts.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {latestPosts.map((post, index) => (
                <motion.div
                  key={post.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.1 * index }}
                >
                  <PostCard post={post} variant="default" />
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="text-center rtl:text-right py-12">
              <p className="text-muted-foreground text-lg">{t('no-posts-found')}</p>
            </div>
          )}
        </motion.div>
      </section>

      {/* Newsletter Section */}
      <section className="space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="bg-gradient-to-r from-primary-600 to-accent-600 text-white rounded-xl p-8 md:p-12 text-center rtl:text-right space-y-6"
        >
          <h2 className="text-2xl md:text-3xl font-bold">
            {language === 'ar' ? 'اشترك في نشرتنا الإخبارية' : 'Subscribe to Our Newsletter'}
          </h2>
          <p className="text-white/90 text-lg leading-relaxed max-w-2xl mx-auto rtl:mr-0">
            {language === 'ar' 
              ? 'احصل على آخر الأخبار والتحديثات مباشرة في بريدك الإلكتروني'
              : 'Get the latest news and updates delivered directly to your inbox'
            }
          </p>
          <form className="flex gap-4 max-w-md mx-auto rtl:mr-0 flex-col sm:flex-row">
            <input
              type="email"
              placeholder={language === 'ar' ? 'أدخل بريدك الإلكتروني' : 'Enter your email'}
              className="flex-1 px-4 py-3 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-white/50 rtl:text-right"
            />
            <Button className="bg-white text-primary-600 hover:bg-white/90 font-semibold">
              {language === 'ar' ? 'اشترك' : 'Subscribe'}
            </Button>
          </form>
        </motion.div>
      </section>
    </Layout>
  )
}

export default HomePage