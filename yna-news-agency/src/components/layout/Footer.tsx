import React from 'react'
import { Link } from 'react-router-dom'
import { Facebook, Twitter, Instagram, Linkedin } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useLanguage } from '@/contexts/LanguageContext'
import YNALogo from '@/components/common/YNALogo'
import { cn } from '@/lib/utils'

const Footer: React.FC = () => {
  const { t } = useTranslation()
  const { isRTL } = useLanguage()

  const socialLinks = [
    { name: 'Facebook', href: '#', icon: Facebook },
    { name: 'Twitter', href: '#', icon: Twitter },
    { name: 'Instagram', href: '#', icon: Instagram },
    { name: 'LinkedIn', href: '#', icon: Linkedin },
  ]

  const footerLinks = [
    {
      title: t('about'),
      links: [
        { name: t('about'), href: '/about' },
        { name: t('our-mission'), href: '/about#mission' },
        { name: t('our-vision'), href: '/about#vision' },
      ],
    },
    {
      title: t('contact'),
      links: [
        { name: t('contact-us'), href: '/contact' },
        { name: 'info@yna.news', href: 'mailto:info@yna.news' },
        { name: '+1 (555) 123-4567', href: 'tel:+15551234567' },
      ],
    },
  ]

  return (
    <footer className="bg-muted/30 border-t border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Logo and Description */}
          <div className="lg:col-span-2">
            <YNALogo size="md" />
            <p className={cn(
              'mt-4 text-sm text-muted-foreground max-w-md leading-relaxed',
              isRTL && 'text-right'
            )}>
              {t('about-description')}
            </p>
            
            {/* Social Media Links */}
            <div className="mt-6">
              <h3 className="text-sm font-semibold text-foreground mb-3">
                {t('follow-us')}
              </h3>
              <div className={cn(
                'flex space-x-4',
                isRTL && 'space-x-reverse'
              )}>
                {socialLinks.map((social) => (
                  <a
                    key={social.name}
                    href={social.href}
                    className="text-muted-foreground hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <span className="sr-only">{social.name}</span>
                    <social.icon className="h-5 w-5" />
                  </a>
                ))}
              </div>
            </div>
          </div>

          {/* Footer Links */}
          {footerLinks.map((section) => (
            <div key={section.title}>
              <h3 className="text-sm font-semibold text-foreground mb-3">
                {section.title}
              </h3>
              <ul className="space-y-2">
                {section.links.map((link) => (
                  <li key={link.name}>
                    {link.href.startsWith('mailto:') || link.href.startsWith('tel:') ? (
                      <a
                        href={link.href}
                        className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                      >
                        {link.name}
                      </a>
                    ) : (
                      <Link
                        to={link.href}
                        className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                      >
                        {link.name}
                      </Link>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}

          {/* Newsletter Signup */}
          <div>
            <h3 className="text-sm font-semibold text-foreground mb-3">
              Newsletter
            </h3>
            <p className="text-sm text-muted-foreground mb-3">
              Subscribe to get the latest news and updates.
            </p>
            <form className="flex gap-2">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-3 py-2 text-sm bg-background border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <button
                type="submit"
                className="px-4 py-2 text-sm font-medium text-primary-foreground bg-primary rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className={cn(
          'mt-8 pt-8 border-t border-border flex flex-col sm:flex-row justify-between items-center',
          isRTL && 'sm:flex-row-reverse'
        )}>
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} {t('youth-news-agency')}. {t('all-rights-reserved')}.
          </p>
          
          <div className={cn(
            'mt-4 sm:mt-0 flex space-x-6',
            isRTL && 'space-x-reverse'
          )}>
            <Link
              to="/privacy"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Privacy Policy
            </Link>
            <Link
              to="/terms"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              Terms of Service
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer