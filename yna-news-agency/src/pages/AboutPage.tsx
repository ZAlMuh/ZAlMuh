import React from 'react'
import { motion } from 'framer-motion'
import { Users, Target, Heart, Award } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useLanguage } from '@/contexts/LanguageContext'
import Layout from '@/components/layout/Layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import YNALogo from '@/components/common/YNALogo'
import { cn } from '@/lib/utils'

const AboutPage: React.FC = () => {
  const { t } = useTranslation()
  const { language, isRTL } = useLanguage()

  const values = [
    {
      icon: Users,
      title: language === 'ar' ? 'التنوع والشمولية' : 'Diversity & Inclusion',
      description: language === 'ar' 
        ? 'نؤمن بقوة التنوع ونسعى لتمثيل جميع أصوات الشباب من مختلف الخلفيات والثقافات'
        : 'We believe in the power of diversity and strive to represent all youth voices from different backgrounds and cultures'
    },
    {
      icon: Target,
      title: language === 'ar' ? 'الدقة والمصداقية' : 'Accuracy & Credibility',
      description: language === 'ar'
        ? 'نلتزم بأعلى معايير الصحافة المهنية ونحرص على تقديم المعلومات الموثوقة والدقيقة'
        : 'We maintain the highest standards of professional journalism and ensure reliable and accurate information'
    },
    {
      icon: Heart,
      title: language === 'ar' ? 'الشغف والالتزام' : 'Passion & Commitment',
      description: language === 'ar'
        ? 'نحن شغوفون بخدمة مجتمع الشباب وملتزمون بتقديم محتوى يلهم ويمكّن الجيل الجديد'
        : 'We are passionate about serving the youth community and committed to providing content that inspires and empowers the new generation'
    },
    {
      icon: Award,
      title: language === 'ar' ? 'التميز والإبداع' : 'Excellence & Innovation',
      description: language === 'ar'
        ? 'نسعى للتميز في كل ما نقوم به ونبتكر طرقًا جديدة لإيصال الأخبار والمعلومات'
        : 'We strive for excellence in everything we do and innovate new ways to deliver news and information'
    }
  ]

  const team = [
    {
      name: language === 'ar' ? 'أحمد محمد' : 'Ahmed Mohamed',
      role: language === 'ar' ? 'رئيس التحرير' : 'Editor-in-Chief',
      bio: language === 'ar' 
        ? 'صحفي متمرس مع أكثر من 10 سنوات من الخبرة في تغطية قضايا الشباب'
        : 'Experienced journalist with over 10 years of experience covering youth issues'
    },
    {
      name: language === 'ar' ? 'سارة أحمد' : 'Sarah Ahmed',
      role: language === 'ar' ? 'مديرة المحتوى' : 'Content Manager',
      bio: language === 'ar'
        ? 'خبيرة في استراتيجيات المحتوى الرقمي وإدارة المجتمعات الإلكترونية'
        : 'Expert in digital content strategies and online community management'
    },
    {
      name: language === 'ar' ? 'عمر خالد' : 'Omar Khalid',
      role: language === 'ar' ? 'مطور التقنية' : 'Tech Lead',
      bio: language === 'ar'
        ? 'مطور متخصص في بناء منصات الإعلام الرقمي وتجربة المستخدم'
        : 'Developer specialized in building digital media platforms and user experience'
    }
  ]

  return (
    <Layout>
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-br from-primary-50 to-accent-50 dark:from-primary-900/20 dark:to-accent-900/20">
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
            <div className="flex justify-center mb-8">
              <YNALogo size="xl" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              {t('about-title')}
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed">
              {t('about-description')}
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Card className="h-full">
                <CardHeader>
                  <CardTitle className="text-2xl text-primary-600 dark:text-primary-400">
                    {t('our-mission')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground leading-relaxed">
                    {language === 'ar' 
                      ? 'مهمتنا هي تمكين الشباب من خلال توفير منصة إعلامية موثوقة وشاملة تغطي القضايا التي تهمهم. نسعى لإعطاء صوت للجيل الجديد وتشجيعهم على المشاركة الفعالة في بناء مجتمعاتهم.'
                      : 'Our mission is to empower youth by providing a reliable and comprehensive media platform that covers issues that matter to them. We strive to give voice to the new generation and encourage them to actively participate in building their communities.'
                    }
                  </p>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <Card className="h-full">
                <CardHeader>
                  <CardTitle className="text-2xl text-accent-600 dark:text-accent-400">
                    {t('our-vision')}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground leading-relaxed">
                    {language === 'ar'
                      ? 'رؤيتنا هي أن نصبح المنصة الإعلامية الرائدة عالميًا في تغطية أخبار وقضايا الشباب، ونكون جسرًا للتفاهم والتواصل بين الثقافات المختلفة من خلال منظور الجيل الجديد.'
                      : 'Our vision is to become the world\'s leading media platform for youth news and issues, serving as a bridge for understanding and communication between different cultures through the perspective of the new generation.'
                    }
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="py-16 bg-muted/30">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className={cn(
              'text-center mb-12',
              isRTL && 'text-right'
            )}
          >
            <h2 className="text-3xl font-bold mb-4">{t('our-values')}</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              {language === 'ar'
                ? 'القيم التي نؤمن بها وتوجه عملنا في وكالة أنباء الشباب'
                : 'The values we believe in and that guide our work at Youth News Agency'
              }
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {values.map((value, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 * index + 0.5 }}
              >
                <Card className="h-full hover:shadow-lg transition-shadow duration-300">
                  <CardHeader>
                    <div className={cn(
                      'flex items-center gap-4',
                      isRTL && 'flex-row-reverse'
                    )}>
                      <div className="flex-shrink-0 w-12 h-12 bg-primary-100 dark:bg-primary-900/20 rounded-lg flex items-center justify-center">
                        <value.icon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                      </div>
                      <CardTitle className="text-lg">{value.title}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground leading-relaxed">
                      {value.description}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.8 }}
            className={cn(
              'text-center mb-12',
              isRTL && 'text-right'
            )}
          >
            <h2 className="text-3xl font-bold mb-4">
              {language === 'ar' ? 'فريقنا' : 'Our Team'}
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              {language === 'ar'
                ? 'تعرف على الأشخاص الذين يقفون وراء وكالة أنباء الشباب'
                : 'Meet the people behind Youth News Agency'
              }
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 * index + 0.9 }}
              >
                <Card className="text-center h-full">
                  <CardContent className="pt-6">
                    <div className="w-24 h-24 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full mx-auto mb-4 flex items-center justify-center text-white text-2xl font-bold">
                      {member.name.charAt(0)}
                    </div>
                    <h3 className="text-lg font-semibold mb-1">{member.name}</h3>
                    <p className="text-primary-600 dark:text-primary-400 mb-3 text-sm">
                      {member.role}
                    </p>
                    <p className="text-muted-foreground text-sm leading-relaxed">
                      {member.bio}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact CTA */}
      <section className="py-16 bg-gradient-to-r from-primary-600 to-accent-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.2 }}
          >
            <h2 className="text-3xl font-bold mb-4">
              {language === 'ar' ? 'تواصل معنا' : 'Get in Touch'}
            </h2>
            <p className="text-white/90 mb-8 max-w-2xl mx-auto">
              {language === 'ar'
                ? 'هل لديك قصة تريد مشاركتها؟ أو تريد الانضمام إلى فريقنا؟ نحن نرحب بك!'
                : 'Have a story to share? Want to join our team? We welcome you!'
              }
            </p>
            <motion.a
              href="/contact"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="inline-block bg-white text-primary-600 px-8 py-3 rounded-lg font-medium hover:bg-white/90 transition-colors"
            >
              {t('contact-us')}
            </motion.a>
          </motion.div>
        </div>
      </section>
    </Layout>
  )
}

export default AboutPage