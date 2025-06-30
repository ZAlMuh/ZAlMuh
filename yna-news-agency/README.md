# YNA - Youth News Agency 🌟

A modern, bilingual (Arabic/English) news platform built with React, TypeScript, and Supabase. YNA delivers the latest news and insights from a youth perspective, featuring beautiful UI/UX with full RTL support and dark/light themes.

![YNA Screenshot](https://via.placeholder.com/800x400/1A2A72/FBB03B?text=YNA+Youth+News+Agency)

## ✨ Features

### 🌐 Bilingual Support
- **Arabic (RTL)** and **English (LTR)** support
- Dynamic text direction switching
- Localized content and UI elements
- Arabic typography with Noto Sans Arabic

### 🎨 Modern UI/UX
- **YNA Brand Colors**: Deep Blue (#1A2A72), Accent Orange (#FBB03B), Navy (#081C45)
- Dark/Light theme toggle with localStorage persistence
- Responsive design for mobile, tablet, and desktop
- Smooth animations with Framer Motion
- Component library with shadcn/ui and Radix UI

### 📰 Content Management
- Full-featured blog/news platform
- Featured posts and latest news sections
- Category-based post filtering
- Full-text search functionality
- Post view tracking and analytics
- Reading time estimation

### 🔐 Admin Dashboard
- Secure authentication with Supabase Auth
- Create, edit, and delete posts
- Analytics dashboard with charts (Recharts)
- Contact form message management
- Maintenance mode toggle
- User role management

### 🚀 Technical Features
- **React 19** with TypeScript
- **Vite** for fast development and building
- **TailwindCSS v4** for styling
- **Supabase** for backend (Database, Auth, Storage)
- **React Router v6** for navigation
- **i18next** for internationalization
- **Framer Motion** for animations
- **Lucide Icons** for UI icons

## 🏗️ Project Structure

```
yna-news-agency/
├── public/                 # Static assets
├── src/
│   ├── components/         # React components
│   │   ├── common/        # Reusable components
│   │   ├── layout/        # Layout components
│   │   └── ui/            # shadcn/ui components
│   ├── contexts/          # React contexts
│   ├── lib/               # Utilities and configurations
│   ├── pages/             # Page components
│   └── admin/             # Admin dashboard
├── supabase-schema.sql    # Database schema
├── netlify.toml          # Netlify deployment config
└── ...
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Supabase account

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd yna-news-agency
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Setup
Copy the environment file and add your Supabase credentials:
```bash
cp .env.example .env
```

Edit `.env` with your Supabase project details:
```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

### 4. Database Setup
1. Create a new Supabase project
2. Run the SQL commands from `supabase-schema.sql` in your Supabase SQL editor
3. Enable Row Level Security (RLS) policies

### 5. Development
```bash
npm run dev
```

Visit `http://localhost:5173` to see your application.

### 6. Build for Production
```bash
npm run build
```

## 📁 Database Schema

### Tables
- **posts**: Blog posts with bilingual content
- **messages**: Contact form submissions  
- **users**: User profiles (extends auth.users)
- **site_stats**: Analytics and view tracking
- **settings**: Site configuration

### Key Features
- Row Level Security (RLS) policies
- Full-text search indexes
- Automatic timestamps
- View counting with PostgreSQL functions

## 🎯 Pages & Routes

- `/` - Homepage with featured and latest posts
- `/post/:slug` - Individual post viewer
- `/category/:slug` - Category-filtered posts  
- `/about` - About page (من نحن)
- `/contact` - Contact form
- `/admin/*` - Admin dashboard (protected)

## 🔧 Configuration

### Theme Colors
The YNA brand colors are configured in `tailwind.config.js`:
- Primary: `#1A2A72` (Deep Blue)
- Accent: `#FBB03B` (Orange)  
- Navy: `#081C45` (Dark Blue)

### Internationalization
Translations are managed in `src/lib/i18n.ts` with support for:
- English (en)
- Arabic (ar)

### Fonts
- **English**: Inter, Poppins
- **Arabic**: Noto Sans Arabic, Cairo

## 🚀 Deployment

### Netlify (Recommended)
1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Add environment variables in Netlify dashboard
5. Deploy!

The project includes:
- `netlify.toml` for configuration
- `_redirects` for SPA routing
- Optimized headers for security and caching

### Alternative Deployments
- **Vercel**: Works out of the box
- **GitHub Pages**: Requires workflow setup
- **AWS S3 + CloudFront**: Manual configuration needed

## 🔐 Authentication & Security

### Supabase Auth Setup
1. Enable authentication in your Supabase project
2. Configure OAuth providers (optional)
3. Set up user profiles table
4. Configure RLS policies

### Security Features
- Row Level Security (RLS) on all tables
- Input validation and sanitization
- CSRF protection
- Secure headers in Netlify configuration

## 📊 Analytics & SEO

### Built-in Analytics
- Post view tracking
- Popular content identification
- User engagement metrics
- Admin dashboard with charts

### SEO Optimization
- Meta tags for each page
- OpenGraph and Twitter Card support
- Semantic HTML structure
- Fast loading with code splitting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: info@yna.news
- 📱 Twitter: [@YNA_News](https://twitter.com/YNA_News)
- 🌐 Website: [yna.news](https://yna.news)

## 🎉 Acknowledgments

- [React](https://reactjs.org/) - UI Library
- [Supabase](https://supabase.io/) - Backend as a Service
- [TailwindCSS](https://tailwindcss.com/) - CSS Framework
- [shadcn/ui](https://ui.shadcn.com/) - Component Library
- [Lucide](https://lucide.dev/) - Icon Library

---

**Built with ❤️ for the youth community**

*YNA - Empowering young voices, one story at a time.*