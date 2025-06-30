import React from 'react'
import { useLanguage } from '@/contexts/LanguageContext'
import { cn } from '@/lib/utils'

interface YNALogoProps {
  className?: string
  showText?: boolean
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'default' | 'light' | 'dark'
}

const YNALogo: React.FC<YNALogoProps> = ({
  className,
  showText = true,
  size = 'md',
  variant = 'default'
}) => {
  const { language } = useLanguage()

  const sizeClasses = {
    sm: 'h-8 w-auto',
    md: 'h-12 w-auto',
    lg: 'h-16 w-auto',
    xl: 'h-24 w-auto'
  }

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-lg',
    lg: 'text-xl',
    xl: 'text-2xl'
  }

  const logoColor = variant === 'light' ? 'text-white' : 
                   variant === 'dark' ? 'text-gray-900' : 
                   'text-primary-500'

  const accentColor = variant === 'light' ? 'text-white' : 
                     variant === 'dark' ? 'text-accent-500' : 
                     'text-accent-500'

  return (
    <div className={cn(
      'flex items-center gap-3 rtl:flex-row-reverse',
      className
    )}>
      {/* YNA Logo SVG */}
      <div className={cn('relative flex-shrink-0', sizeClasses[size])}>
        <svg
          viewBox="0 0 60 20"
          className="w-full h-full"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Background geometric pattern */}
          <defs>
            <linearGradient id="yna-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#1A2A72" />
              <stop offset="100%" stopColor="#FBB03B" />
            </linearGradient>
          </defs>
          
          {/* Y Letter */}
          <path
            d="M2 2 L5 7 L8 2 L10 2 L6 9 L6 12 L4 12 L4 9 L0 2 Z"
            fill="url(#yna-gradient)"
            className="drop-shadow-sm"
          />
          
          {/* N Letter */}
          <path
            d="M12 2 L12 12 L14 12 L14 5 L17 12 L19 12 L19 2 L17 2 L17 9 L14 2 Z"
            fill="url(#yna-gradient)"
            className="drop-shadow-sm"
          />
          
          {/* A Letter */}
          <path
            d="M22 2 L25 12 L27 12 L27.5 10 L30.5 10 L31 12 L33 12 L30 2 L25 2 Z M26.5 8 L29 8 L27.75 4 Z"
            fill="url(#yna-gradient)"
            className="drop-shadow-sm"
          />
          
          {/* Accent triangle */}
          <path
            d="M35 2 L37 4 L35 6 Z"
            fill="#FBB03B"
            className="drop-shadow-sm"
          />
        </svg>
      </div>

      {/* Text */}
      {showText && (
        <div className="flex flex-col leading-tight">
          <div className={cn(
            'font-bold font-display tracking-wide',
            textSizeClasses[size],
            logoColor
          )}>
            {language === 'ar' ? 'وكالة أنباء الشباب' : 'YOUTH NEWS AGENCY'}
          </div>
          {size !== 'sm' && (
            <div className={cn(
              'text-xs opacity-80 text-left rtl:text-right',
              accentColor
            )}>
              {language === 'ar' ? 'YNA' : 'YNA'}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default YNALogo