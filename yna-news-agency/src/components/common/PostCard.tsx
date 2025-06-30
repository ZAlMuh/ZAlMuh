import React from 'react'
import { Link } from 'react-router-dom'
import { Clock, Eye, Calendar, ArrowRight, ArrowLeft } from 'lucide-react'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { useLanguage } from '@/contexts/LanguageContext'
import { Card, CardContent, CardFooter } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { Post } from '@/lib/supabase'
import { formatDate, formatDateArabic, calculateReadingTime } from '@/lib/utils'
import { cn } from '@/lib/utils'

interface PostCardProps {
  post: Post
  variant?: 'default' | 'featured' | 'compact'
  className?: string
}

const PostCard: React.FC<PostCardProps> = ({ post, variant = 'default', className }) => {
  const { t } = useTranslation()
  const { language, isRTL } = useLanguage()

  const title = language === 'ar' ? post.title_ar : post.title_en
  const excerpt = language === 'ar' ? post.excerpt_ar : post.excerpt_en
  const content = language === 'ar' ? post.content_ar : post.content_en
  const readingTime = calculateReadingTime(content)
  const formattedDate = language === 'ar' 
    ? formatDateArabic(post.created_at)
    : formatDate(post.created_at)

  const ArrowIcon = isRTL ? ArrowLeft : ArrowRight

  if (variant === 'compact') {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        whileHover={{ y: -2 }}
        transition={{ duration: 0.2 }}
        className={className}
      >
        <Link
          to={`/post/${post.slug}`}
          className="group block"
        >
          <div className="flex gap-4">
            {post.cover_image && (
              <div className="flex-shrink-0">
                <img
                  src={post.cover_image}
                  alt={title}
                  className="w-20 h-20 object-cover rounded-lg"
                />
              </div>
            )}
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-medium line-clamp-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                {title}
              </h3>
              <div className={cn(
                'mt-2 flex items-center gap-4 text-xs text-muted-foreground',
                isRTL && 'flex-row-reverse'
              )}>
                <span className="flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {formattedDate}
                </span>
                <span className="flex items-center gap-1">
                  <Eye className="h-3 w-3" />
                  {post.views}
                </span>
              </div>
            </div>
          </div>
        </Link>
      </motion.div>
    )
  }

  if (variant === 'featured') {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        whileHover={{ scale: 1.02 }}
        transition={{ duration: 0.3 }}
        className={className}
      >
        <Card className="group overflow-hidden border-0 bg-gradient-to-br from-primary-50 to-accent-50 dark:from-primary-900/20 dark:to-accent-900/20">
          <Link to={`/post/${post.slug}`}>
            {post.cover_image && (
              <div className="relative h-64 overflow-hidden">
                <img
                  src={post.cover_image}
                  alt={title}
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
                <div className="absolute top-4 right-4">
                  <Badge variant="secondary" className="bg-accent-500 text-white">
                    {t('featured-posts')}
                  </Badge>
                </div>
              </div>
            )}
            
            <CardContent className="p-6">
              <div className={cn(
                'flex items-center gap-2 mb-3',
                isRTL && 'flex-row-reverse'
              )}>
                <Badge variant="outline" className="text-xs">
                  {post.category}
                </Badge>
                <span className="text-xs text-muted-foreground">
                  {formattedDate}
                </span>
              </div>
              
              <h2 className="text-xl font-bold mb-3 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors line-clamp-2">
                {title}
              </h2>
              
              {excerpt && (
                <p className="text-muted-foreground mb-4 line-clamp-3">
                  {excerpt}
                </p>
              )}
            </CardContent>
            
            <CardFooter className="p-6 pt-0 flex justify-between items-center">
              <div className={cn(
                'flex items-center gap-4 text-sm text-muted-foreground',
                isRTL && 'flex-row-reverse'
              )}>
                <span className="flex items-center gap-1">
                  <Clock className="h-4 w-4" />
                  {t('reading-time', { time: readingTime })}
                </span>
                <span className="flex items-center gap-1">
                  <Eye className="h-4 w-4" />
                  {post.views}
                </span>
              </div>
              
              <span className="flex items-center gap-2 text-sm font-medium text-primary-600 dark:text-primary-400 group-hover:gap-3 transition-all">
                {t('read-more')}
                <ArrowIcon className="h-4 w-4" />
              </span>
            </CardFooter>
          </Link>
        </Card>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
      className={className}
    >
      <Card className="group overflow-hidden h-full">
        <Link to={`/post/${post.slug}`}>
          {post.cover_image && (
            <div className="relative h-48 overflow-hidden">
              <img
                src={post.cover_image}
                alt={title}
                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
            </div>
          )}
          
          <CardContent className="p-4">
            <div className={cn(
              'flex items-center gap-2 mb-2',
              isRTL && 'flex-row-reverse'
            )}>
              <Badge variant="outline" className="text-xs">
                {post.category}
              </Badge>
              <span className="text-xs text-muted-foreground">
                {formattedDate}
              </span>
            </div>
            
            <h3 className="font-semibold mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors line-clamp-2">
              {title}
            </h3>
            
            {excerpt && (
              <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                {excerpt}
              </p>
            )}
          </CardContent>
          
          <CardFooter className="p-4 pt-0 flex justify-between items-center">
            <div className={cn(
              'flex items-center gap-3 text-xs text-muted-foreground',
              isRTL && 'flex-row-reverse'
            )}>
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {t('reading-time', { time: readingTime })}
              </span>
              <span className="flex items-center gap-1">
                <Eye className="h-3 w-3" />
                {post.views}
              </span>
            </div>
            
            <span className="flex items-center gap-1 text-xs font-medium text-primary-600 dark:text-primary-400 group-hover:gap-2 transition-all">
              {t('read-more')}
              <ArrowIcon className="h-3 w-3" />
            </span>
          </CardFooter>
        </Link>
      </Card>
    </motion.div>
  )
}

export default PostCard