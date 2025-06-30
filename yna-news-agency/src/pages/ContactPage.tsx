import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Mail, Phone, MapPin, Send, CheckCircle } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useLanguage } from '@/contexts/LanguageContext'
import { dbOperations } from '@/lib/supabase'
import Layout from '@/components/layout/Layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import Loading from '@/components/common/Loading'
import { cn } from '@/lib/utils'

const ContactPage: React.FC = () => {
  const { t } = useTranslation()
  const { language, isRTL } = useLanguage()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  })
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const contactInfo = [
    {
      icon: Mail,
      title: language === 'ar' ? 'البريد الإلكتروني' : 'Email',
      value: 'info@yna.news',
      href: 'mailto:info@yna.news'
    },
    {
      icon: Phone,
      title: language === 'ar' ? 'الهاتف' : 'Phone',
      value: '+1 (555) 123-4567',
      href: 'tel:+15551234567'
    },
    {
      icon: MapPin,
      title: language === 'ar' ? 'العنوان' : 'Address',
      value: language === 'ar' ? 'الرياض، المملكة العربية السعودية' : 'Riyadh, Saudi Arabia',
      href: null
    }
  ]

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.name.trim() || !formData.email.trim() || !formData.message.trim()) {
      setError(t('required-field'))
      return
    }

    try {
      setLoading(true)
      setError(null)
      
      await dbOperations.createMessage({
        name: formData.name.trim(),
        email: formData.email.trim(),
        message: formData.message.trim()
      })
      
      setSubmitted(true)
      setFormData({ name: '', email: '', message: '' })
    } catch (err) {
      console.error('Error sending message:', err)
      setError(t('error-occurred'))
    } finally {
      setLoading(false)
    }
  }

  if (submitted) {
    return (
      <Layout>
        <div className="min-h-[60vh] flex items-center justify-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="text-center max-w-md mx-auto px-4"
          >
            <div className="w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="h-8 w-8 text-green-600 dark:text-green-400" />
            </div>
            <h2 className="text-2xl font-bold mb-4">
              {language === 'ar' ? 'شكراً لك!' : 'Thank You!'}
            </h2>
            <p className="text-muted-foreground mb-6">
              {t('message-sent')}
            </p>
            <Button onClick={() => setSubmitted(false)}>
              {language === 'ar' ? 'إرسال رسالة أخرى' : 'Send Another Message'}
            </Button>
          </motion.div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      {/* Hero Section */}
      <section className="py-16 bg-gradient-to-br from-primary-50 to-accent-50 dark:from-primary-900/20 dark:to-accent-900/20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className={cn(
              'text-center',
              isRTL && 'text-right'
            )}
          >
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              {t('contact-us')}
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed max-w-2xl mx-auto">
              {language === 'ar'
                ? 'نحن نرحب بأسئلتكم واقتراحاتكم. تواصلوا معنا ونحن سنكون سعداء للإجابة عليكم'
                : 'We welcome your questions and suggestions. Contact us and we\'ll be happy to respond to you'
              }
            </p>
          </motion.div>
        </div>
      </section>

      {/* Contact Form & Info */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-2xl">
                    {language === 'ar' ? 'أرسل لنا رسالة' : 'Send us a Message'}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium mb-2">
                        {t('name')} *
                      </label>
                      <Input
                        id="name"
                        name="name"
                        type="text"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder={language === 'ar' ? 'اسمك الكامل' : 'Your full name'}
                        className={cn(isRTL && 'text-right')}
                        required
                      />
                    </div>

                    <div>
                      <label htmlFor="email" className="block text-sm font-medium mb-2">
                        {t('email')} *
                      </label>
                      <Input
                        id="email"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder={language === 'ar' ? 'بريدك الإلكتروني' : 'Your email address'}
                        className={cn(isRTL && 'text-right')}
                        required
                      />
                    </div>

                    <div>
                      <label htmlFor="message" className="block text-sm font-medium mb-2">
                        {t('message')} *
                      </label>
                      <Textarea
                        id="message"
                        name="message"
                        value={formData.message}
                        onChange={handleChange}
                        placeholder={language === 'ar' ? 'اكتب رسالتك هنا...' : 'Write your message here...'}
                        className={cn('min-h-[120px]', isRTL && 'text-right')}
                        required
                      />
                    </div>

                    {error && (
                      <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
                        <p className="text-sm text-destructive">{error}</p>
                      </div>
                    )}

                    <Button
                      type="submit"
                      disabled={loading}
                      className={cn(
                        'w-full gap-2',
                        isRTL && 'flex-row-reverse'
                      )}
                    >
                      {loading ? (
                        <Loading size="sm" />
                      ) : (
                        <>
                          <Send className="h-4 w-4" />
                          {t('send-message')}
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>

            {/* Contact Information */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="space-y-6"
            >
              <div>
                <h2 className="text-2xl font-bold mb-6">
                  {language === 'ar' ? 'معلومات التواصل' : 'Contact Information'}
                </h2>
                <p className="text-muted-foreground mb-8">
                  {language === 'ar'
                    ? 'يمكنكم التواصل معنا من خلال الوسائل التالية. نحن نتطلع لسماع آرائكم واقتراحاتكم'
                    : 'You can reach us through the following means. We look forward to hearing your opinions and suggestions'
                  }
                </p>
              </div>

              <div className="space-y-4">
                {contactInfo.map((info, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 * index + 0.4 }}
                  >
                    <Card className="p-4">
                      <div className={cn(
                        'flex items-center gap-4',
                        isRTL && 'flex-row-reverse'
                      )}>
                        <div className="flex-shrink-0 w-12 h-12 bg-primary-100 dark:bg-primary-900/20 rounded-lg flex items-center justify-center">
                          <info.icon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                        </div>
                        <div className={cn('flex-1', isRTL && 'text-right')}>
                          <h3 className="font-medium text-sm text-muted-foreground">
                            {info.title}
                          </h3>
                          {info.href ? (
                            <a
                              href={info.href}
                              className="text-foreground hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                            >
                              {info.value}
                            </a>
                          ) : (
                            <p className="text-foreground">{info.value}</p>
                          )}
                        </div>
                      </div>
                    </Card>
                  </motion.div>
                ))}
              </div>

              {/* FAQ Section */}
              <div className="mt-12">
                <h3 className="text-xl font-semibold mb-4">
                  {language === 'ar' ? 'أسئلة شائعة' : 'Frequently Asked Questions'}
                </h3>
                <div className="space-y-4">
                  <Card className="p-4">
                    <h4 className="font-medium mb-2">
                      {language === 'ar' ? 'كيف يمكنني إرسال قصة إخبارية؟' : 'How can I submit a news story?'}
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      {language === 'ar'
                        ? 'يمكنكم إرسال قصصكم الإخبارية من خلال نموذج التواصل أعلاه أو مراسلتنا على البريد الإلكتروني'
                        : 'You can submit your news stories through the contact form above or email us directly'
                      }
                    </p>
                  </Card>
                  
                  <Card className="p-4">
                    <h4 className="font-medium mb-2">
                      {language === 'ar' ? 'هل يمكنني الانضمام إلى فريق العمل؟' : 'Can I join the team?'}
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      {language === 'ar'
                        ? 'نحن نرحب بالمواهب الجديدة! أرسلوا لنا سيرتكم الذاتية ونبذة عن خبراتكم'
                        : 'We welcome new talents! Send us your CV and a brief about your experience'
                      }
                    </p>
                  </Card>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    </Layout>
  )
}

export default ContactPage