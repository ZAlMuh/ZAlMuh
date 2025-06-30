import React from 'react'
import { Languages, Globe } from 'lucide-react'
import { useLanguage } from '@/contexts/LanguageContext'
// import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface LanguageSwitcherProps {
  className?: string
  variant?: 'button' | 'text' | 'icon'
  size?: 'sm' | 'md' | 'lg'
}

const LanguageSwitcher: React.FC<LanguageSwitcherProps> = ({ 
  className, 
  variant = 'button',
  size = 'md' 
}) => {
  const { language, toggleLanguage } = useLanguage()
  // const { t } = useTranslation()

  const sizeClasses = {
    sm: 'h-8 px-2 text-xs',
    md: 'h-10 px-3 text-sm',
    lg: 'h-12 px-4 text-base'
  }

  const iconSizes = {
    sm: 'h-3 w-3',
    md: 'h-4 w-4',
    lg: 'h-5 w-5'
  }

  if (variant === 'text') {
    return (
      <button
        onClick={toggleLanguage}
        className={cn(
          'text-sm font-medium text-muted-foreground hover:text-foreground transition-colors',
          className
        )}
      >
        {language === 'en' ? 'العربية' : 'English'}
      </button>
    )
  }

  if (variant === 'icon') {
    return (
      <Button
        variant="ghost"
        size="icon"
        onClick={toggleLanguage}
        className={cn('transition-all duration-200', className)}
        title={language === 'en' ? 'Switch to Arabic' : 'Switch to English'}
      >
        <Globe className={iconSizes[size]} />
        <span className="sr-only">
          {language === 'en' ? 'Switch to Arabic' : 'Switch to English'}
        </span>
      </Button>
    )
  }

  return (
    <Button
      variant="outline"
      onClick={toggleLanguage}
      className={cn(
        'flex items-center gap-2 transition-all duration-200',
        sizeClasses[size],
        className
      )}
    >
      <Languages className={iconSizes[size]} />
      <span className="font-medium">
        {language === 'en' ? 'العربية' : 'English'}
      </span>
    </Button>
  )
}

export default LanguageSwitcher