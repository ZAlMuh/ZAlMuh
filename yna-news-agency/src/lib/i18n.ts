import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

const resources = {
  en: {
    translation: {
      // Navigation
      home: 'Home',
      about: 'About Us',
      contact: 'Contact',
      admin: 'Admin',
      
      // Header
      'youth-news-agency': 'Youth News Agency',
      'latest-news': 'Latest News',
      'featured-posts': 'Featured Posts',
      
      // Post
      'read-more': 'Read More',
      'reading-time': '{{time}} min read',
      'published-on': 'Published on',
      'by-author': 'By {{author}}',
      'share-post': 'Share Post',
      'related-posts': 'Related Posts',
      'no-posts-found': 'No posts found',
      
      // Categories
      'all-categories': 'All Categories',
      'category': 'Category',
      'tags': 'Tags',
      
      // Search
      'search': 'Search',
      'search-placeholder': 'Search articles...',
      'search-results': 'Search Results',
      'no-results': 'No results found for "{{query}}"',
      
      // Language & Theme
      'language': 'Language',
      'theme': 'Theme',
      'light-mode': 'Light Mode',
      'dark-mode': 'Dark Mode',
      'switch-to-arabic': 'العربية',
      'switch-to-english': 'English',
      
      // Contact Form
      'contact-us': 'Contact Us',
      'name': 'Name',
      'email': 'Email',
      'message': 'Message',
      'send-message': 'Send Message',
      'message-sent': 'Message sent successfully!',
      'required-field': 'This field is required',
      
      // About Page
      'about-title': 'About Youth News Agency',
      'about-description': 'YNA is a dynamic platform dedicated to delivering the latest news and insights from a youth perspective. We cover diverse topics that matter to young people worldwide.',
      'our-mission': 'Our Mission',
      'our-vision': 'Our Vision',
      'our-values': 'Our Values',
      
      // Admin Dashboard
      'dashboard': 'Dashboard',
      'posts': 'Posts',
      'create-post': 'Create Post',
      'edit-post': 'Edit Post',
      'delete-post': 'Delete Post',
      'post-title': 'Post Title',
      'post-content': 'Post Content',
      'post-category': 'Category',
      'post-tags': 'Tags',
      'post-status': 'Status',
      'published': 'Published',
      'draft': 'Draft',
      'save-post': 'Save Post',
      'post-saved': 'Post saved successfully!',
      'confirm-delete': 'Are you sure you want to delete this post?',
      'login': 'Login',
      'logout': 'Logout',
      'email-address': 'Email Address',
      'password': 'Password',
      'sign-in': 'Sign In',
      'analytics': 'Analytics',
      'total-posts': 'Total Posts',
      'total-views': 'Total Views',
      'messages': 'Messages',
      'settings': 'Settings',
      'maintenance-mode': 'Maintenance Mode',
      
      // Footer
      'all-rights-reserved': 'All rights reserved',
      'follow-us': 'Follow Us',
      
      // Errors
      'error-occurred': 'An error occurred',
      'try-again': 'Try Again',
      'loading': 'Loading...',
      'page-not-found': 'Page Not Found',
      'go-home': 'Go Home',
    }
  },
  ar: {
    translation: {
      // Navigation
      home: 'الرئيسية',
      about: 'من نحن',
      contact: 'اتصل بنا',
      admin: 'الإدارة',
      
      // Header
      'youth-news-agency': 'وكالة أنباء الشباب',
      'latest-news': 'آخر الأخبار',
      'featured-posts': 'المقالات المميزة',
      
      // Post
      'read-more': 'اقرأ المزيد',
      'reading-time': '{{time}} دقيقة قراءة',
      'published-on': 'نُشر في',
      'by-author': 'بواسطة {{author}}',
      'share-post': 'شارك المقال',
      'related-posts': 'مقالات ذات صلة',
      'no-posts-found': 'لم يتم العثور على مقالات',
      
      // Categories
      'all-categories': 'جميع الفئات',
      'category': 'الفئة',
      'tags': 'العلامات',
      
      // Search
      'search': 'بحث',
      'search-placeholder': 'ابحث في المقالات...',
      'search-results': 'نتائج البحث',
      'no-results': 'لم يتم العثور على نتائج لـ "{{query}}"',
      
      // Language & Theme
      'language': 'اللغة',
      'theme': 'المظهر',
      'light-mode': 'المظهر الفاتح',
      'dark-mode': 'المظهر الداكن',
      'switch-to-arabic': 'العربية',
      'switch-to-english': 'English',
      
      // Contact Form
      'contact-us': 'اتصل بنا',
      'name': 'الاسم',
      'email': 'البريد الإلكتروني',
      'message': 'الرسالة',
      'send-message': 'إرسال الرسالة',
      'message-sent': 'تم إرسال الرسالة بنجاح!',
      'required-field': 'هذا الحقل مطلوب',
      
      // About Page
      'about-title': 'حول وكالة أنباء الشباب',
      'about-description': 'وكالة أنباء الشباب منصة ديناميكية مخصصة لتقديم آخر الأخبار والرؤى من منظور الشباب. نحن نغطي مواضيع متنوعة تهم الشباب في جميع أنحاء العالم.',
      'our-mission': 'مهمتنا',
      'our-vision': 'رؤيتنا',
      'our-values': 'قيمنا',
      
      // Admin Dashboard
      'dashboard': 'لوحة التحكم',
      'posts': 'المقالات',
      'create-post': 'إنشاء مقال',
      'edit-post': 'تعديل المقال',
      'delete-post': 'حذف المقال',
      'post-title': 'عنوان المقال',
      'post-content': 'محتوى المقال',
      'post-category': 'الفئة',
      'post-tags': 'العلامات',
      'post-status': 'الحالة',
      'published': 'منشور',
      'draft': 'مسودة',
      'save-post': 'حفظ المقال',
      'post-saved': 'تم حفظ المقال بنجاح!',
      'confirm-delete': 'هل أنت متأكد من أنك تريد حذف هذا المقال؟',
      'login': 'تسجيل الدخول',
      'logout': 'تسجيل الخروج',
      'email-address': 'عنوان البريد الإلكتروني',
      'password': 'كلمة المرور',
      'sign-in': 'تسجيل الدخول',
      'analytics': 'التحليلات',
      'total-posts': 'إجمالي المقالات',
      'total-views': 'إجمالي المشاهدات',
      'messages': 'الرسائل',
      'settings': 'الإعدادات',
      'maintenance-mode': 'وضع الصيانة',
      
      // Footer
      'all-rights-reserved': 'جميع الحقوق محفوظة',
      'follow-us': 'تابعنا',
      
      // Errors
      'error-occurred': 'حدث خطأ',
      'try-again': 'حاول مرة أخرى',
      'loading': 'جاري التحميل...',
      'page-not-found': 'الصفحة غير موجودة',
      'go-home': 'العودة للرئيسية',
    }
  }
}

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    debug: false,

    interpolation: {
      escapeValue: false,
    },

    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage'],
    },
  })

export default i18n