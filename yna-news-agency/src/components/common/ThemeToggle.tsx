import React from 'react'
import { Moon, Sun } from 'lucide-react'
import { useTheme } from '@/contexts/ThemeContext'
import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface ThemeToggleProps {
  className?: string
  size?: 'sm' | 'md' | 'lg'
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ className, size = 'md' }) => {
  const { theme, toggleTheme } = useTheme()
  const { t } = useTranslation()

  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-12 w-12'
  }

  const iconSizes = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6'
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleTheme}
      className={cn(
        sizeClasses[size],
        'relative overflow-hidden transition-all duration-300 hover:bg-accent/10',
        className
      )}
      title={theme === 'light' ? t('dark-mode') : t('light-mode')}
    >
      <Sun 
        className={cn(
          iconSizes[size],
          'absolute transition-all duration-300 rotate-0 scale-100',
          theme === 'dark' && '-rotate-90 scale-0'
        )} 
      />
      <Moon 
        className={cn(
          iconSizes[size],
          'absolute transition-all duration-300 rotate-90 scale-0',
          theme === 'dark' && 'rotate-0 scale-100'
        )} 
      />
      <span className="sr-only">
        {theme === 'light' ? t('dark-mode') : t('light-mode')}
      </span>
    </Button>
  )
}

export default ThemeToggle