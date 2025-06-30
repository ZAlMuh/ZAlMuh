import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Search } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useLanguage } from '@/contexts/LanguageContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import YNALogo from '@/components/common/YNALogo'
import ThemeToggle from '@/components/common/ThemeToggle'
import LanguageSwitcher from '@/components/common/LanguageSwitcher'
import { cn } from '@/lib/utils'

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const { t } = useTranslation()
  const { isRTL } = useLanguage()
  const location = useLocation()

  const navigation = [
    { name: t('home'), href: '/' },
    { name: t('about'), href: '/about' },
    { name: t('contact'), href: '/contact' },
  ]

  const isActive = (path: string) => location.pathname === path

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      // Navigate to search results
      window.location.href = `/search?q=${encodeURIComponent(searchQuery.trim())}`
    }
  }

  return (
    <nav className="sticky top-0 z-50 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="flex items-center">
              <YNALogo size="sm" showText={false} />
              <span className="ml-2 rtl:ml-0 rtl:mr-2 font-bold text-lg text-primary-600 dark:text-primary-400">
                YNA
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="flex items-center space-x-8 rtl:space-x-reverse">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    'text-sm font-medium transition-colors duration-200 hover:text-primary-600 dark:hover:text-primary-400',
                    isActive(item.href)
                      ? 'text-primary-600 dark:text-primary-400'
                      : 'text-muted-foreground'
                  )}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>

          {/* Search Bar */}
          <div className="hidden lg:block flex-1 max-w-md mx-8">
            <form onSubmit={handleSearch} className="relative">
              <Search className="absolute top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground left-3 rtl:left-auto rtl:right-3" />
              <Input
                type="text"
                placeholder={t('search-placeholder')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-muted/50 border-0 focus:bg-background pl-10 pr-4 rtl:pl-4 rtl:pr-10"
              />
            </form>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-4 rtl:space-x-reverse">
            {/* Mobile Search Toggle */}
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setIsSearchOpen(!isSearchOpen)}
            >
              <Search className="h-5 w-5" />
            </Button>

            {/* Theme Toggle */}
            <ThemeToggle size="sm" />

            {/* Language Switcher */}
            <LanguageSwitcher variant="icon" size="sm" />

            {/* Mobile Menu Toggle */}
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Search */}
        {isSearchOpen && (
          <div className="lg:hidden py-4 border-t border-border">
            <form onSubmit={handleSearch} className="relative">
              <Search className="absolute top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground left-3 rtl:left-auto rtl:right-3" />
              <Input
                type="text"
                placeholder={t('search-placeholder')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className={cn(
                  'w-full',
                  isRTL ? 'pr-10 pl-4' : 'pl-10 pr-4'
                )}
                autoFocus
              />
            </form>
          </div>
        )}

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 border-t border-border">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    'block px-3 py-2 text-base font-medium rounded-md transition-colors duration-200',
                    isActive(item.href)
                      ? 'text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20'
                      : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                  )}
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              
              {/* Mobile Language Switcher */}
              <div className="px-3 py-2">
                <LanguageSwitcher variant="button" size="sm" />
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar