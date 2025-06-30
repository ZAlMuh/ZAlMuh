import React, { useState, useEffect } from 'react'
import { Search, X } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useLanguage } from '@/contexts/LanguageContext'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface SearchBarProps {
  onSearch: (query: string) => void
  placeholder?: string
  className?: string
  autoFocus?: boolean
  defaultValue?: string
}

const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  placeholder,
  className,
  autoFocus = false,
  defaultValue = ''
}) => {
  const [query, setQuery] = useState(defaultValue)
  const { t } = useTranslation()
  const { isRTL } = useLanguage()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim())
    }
  }

  const handleClear = () => {
    setQuery('')
    onSearch('')
  }

  useEffect(() => {
    setQuery(defaultValue)
  }, [defaultValue])

  return (
    <form onSubmit={handleSubmit} className={cn('relative w-full', className)}>
      <div className="relative">
        <Search className={cn(
          'absolute top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground',
          isRTL ? 'right-3' : 'left-3'
        )} />
        
        <Input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder || t('search-placeholder')}
          autoFocus={autoFocus}
          className={cn(
            'w-full transition-all duration-200 focus:ring-2 focus:ring-primary-500',
            isRTL ? 'pr-10 pl-12' : 'pl-10 pr-12'
          )}
        />
        
        {query && (
          <Button
            type="button"
            variant="ghost"
            size="icon"
            onClick={handleClear}
            className={cn(
              'absolute top-1/2 transform -translate-y-1/2 h-8 w-8 hover:bg-transparent',
              isRTL ? 'left-1' : 'right-1'
            )}
          >
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>
      
      {/* Hidden submit button for form submission */}
      <button type="submit" className="sr-only">
        {t('search')}
      </button>
    </form>
  )
}

export default SearchBar