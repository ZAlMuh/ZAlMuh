import React, { createContext, useContext, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'

interface LanguageContextType {
  language: string
  isRTL: boolean
  toggleLanguage: () => void
  setLanguage: (lang: string) => void
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export const useLanguage = () => {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
}

interface LanguageProviderProps {
  children: React.ReactNode
}

export const LanguageProvider: React.FC<LanguageProviderProps> = ({ children }) => {
  const { i18n } = useTranslation()
  const [language, setLanguageState] = useState(i18n.language || 'en')
  const [isRTL, setIsRTL] = useState(language === 'ar')

  const setLanguage = (lang: string) => {
    i18n.changeLanguage(lang)
    setLanguageState(lang)
    setIsRTL(lang === 'ar')
    
    // Update document direction and lang attribute
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr'
    document.documentElement.lang = lang
    
    // Store in localStorage
    localStorage.setItem('language', lang)
  }

  const toggleLanguage = () => {
    const newLang = language === 'en' ? 'ar' : 'en'
    setLanguage(newLang)
  }

  useEffect(() => {
    // Initialize language from localStorage or browser
    const storedLang = localStorage.getItem('language')
    const initialLang = storedLang || i18n.language || 'en'
    
    if (initialLang !== language) {
      setLanguage(initialLang)
    }
  }, [])

  useEffect(() => {
    // Update document direction when language changes
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr'
    document.documentElement.lang = language
  }, [language, isRTL])

  const value: LanguageContextType = {
    language,
    isRTL,
    toggleLanguage,
    setLanguage,
  }

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  )
}