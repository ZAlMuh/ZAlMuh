import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import Navbar from './Navbar'
import Footer from './Footer'
import { useLanguage } from '@/contexts/LanguageContext'
import { cn } from '@/lib/utils'

interface LayoutProps {
  children: React.ReactNode
  className?: string
}

const Layout: React.FC<LayoutProps> = ({ children, className }) => {
  const { isRTL, language } = useLanguage()

  // Set document direction and language
  useEffect(() => {
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr'
    document.documentElement.lang = language
    
    // Set font family based on language
    if (isRTL) {
      document.documentElement.style.fontFamily = "'Noto Sans Arabic', 'Cairo', system-ui, sans-serif"
    } else {
      document.documentElement.style.fontFamily = "'Inter', system-ui, sans-serif"
    }
  }, [isRTL, language])

  return (
    <div 
      dir={isRTL ? 'rtl' : 'ltr'} 
      className="min-h-screen bg-background text-foreground overflow-x-hidden"
    >
      {/* Background YNA Logo - Fixed positioning outside layout flow */}
      <div className="fixed inset-0 -z-10 opacity-5 pointer-events-none">
        <div className="flex items-center justify-center w-full h-full">
          <div className="text-[12rem] md:text-[15rem] lg:text-[20rem] font-bold text-primary-500 select-none">
            YNA
          </div>
        </div>
      </div>

      <div className="flex flex-col min-h-screen">
        <Navbar />
        
        <motion.main
          className={cn(
            'flex-1 relative',
            className
          )}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3, ease: 'easeInOut' }}
        >
          <div className="container mx-auto max-w-screen-xl px-4 py-8 space-y-12">
            {children}
          </div>
        </motion.main>
        
        <Footer />
      </div>
    </div>
  )
}

export default Layout