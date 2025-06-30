-- Sample Data for YNA - Youth News Agency (Fixed Version)
-- Run this AFTER running supabase-schema.sql

-- First, let's create a sample user in the users table directly
-- Note: In production, users should be created through Supabase Auth
INSERT INTO auth.users (
  id,
  instance_id,
  email,
  encrypted_password,
  email_confirmed_at,
  created_at,
  updated_at,
  role,
  aud,
  confirmation_token,
  recovery_token,
  email_change_token_new,
  email_change
) VALUES (
  gen_random_uuid(),
  '00000000-0000-0000-0000-000000000000',
  'admin@yna.news',
  crypt('password123', gen_salt('bf')),
  now(),
  now(),
  now(),
  'authenticated',
  'authenticated',
  '',
  '',
  '',
  ''
) ON CONFLICT (email) DO NOTHING;

-- Create corresponding profile in public.users table
INSERT INTO public.users (
  id,
  full_name,
  email,
  role
) 
SELECT 
  id,
  'YNA Admin',
  email,
  'admin'
FROM auth.users 
WHERE email = 'admin@yna.news'
ON CONFLICT (id) DO NOTHING;

-- Now insert sample posts using the created user
INSERT INTO posts (
  slug, 
  title_en, 
  title_ar, 
  content_en, 
  content_ar, 
  excerpt_en,
  excerpt_ar,
  category, 
  tags, 
  cover_image, 
  status, 
  featured, 
  author_id
) VALUES 
(
  'welcome-to-yna',
  'Welcome to Youth News Agency',
  'مرحباً بكم في وكالة أنباء الشباب',
  'Welcome to YNA - Youth News Agency! We are excited to launch our new platform dedicated to bringing you the latest news and insights from a youth perspective. Our mission is to empower young voices and provide a space where the stories that matter to young people can be heard and shared.

At YNA, we believe that youth perspectives are crucial in understanding and shaping our world. We cover a wide range of topics including technology, politics, culture, sports, environment, and education - all through the lens of what matters most to the younger generation.

Our team consists of passionate young journalists, writers, and content creators who are committed to delivering high-quality, accurate, and engaging content. We strive to be a trusted source of information while also providing a platform for youth to express their opinions and share their experiences.

Stay tuned for exciting content, breaking news, in-depth analysis, and stories that inspire and inform. Welcome to the YNA community!',
  'أهلاً وسهلاً بكم في وكالة أنباء الشباب! نحن متحمسون لإطلاق منصتنا الجديدة المخصصة لتقديم آخر الأخبار والرؤى من منظور الشباب. مهمتنا هي تمكين أصوات الشباب وتوفير مساحة حيث يمكن سماع ومشاركة القصص التي تهم الشباب.

في وكالة أنباء الشباب، نؤمن أن وجهات نظر الشباب أمر بالغ الأهمية في فهم وتشكيل عالمنا. نغطي مجموعة واسعة من المواضيع بما في ذلك التكنولوجيا والسياسة والثقافة والرياضة والبيئة والتعليم - كل ذلك من خلال عدسة ما يهم الجيل الأصغر أكثر.

يتكون فريقنا من صحفيين شباب متحمسين وكتاب ومنشئي محتوى ملتزمين بتقديم محتوى عالي الجودة ودقيق وجذاب. نحن نسعى لأن نكون مصدراً موثوقاً للمعلومات مع توفير منصة للشباب للتعبير عن آرائهم ومشاركة تجاربهم.

ترقبوا محتوى مثيراً وأخباراً عاجلة وتحليلات متعمقة وقصصاً تلهم وتعلم. مرحباً بكم في مجتمع وكالة أنباء الشباب!',
  'We are excited to launch our new platform dedicated to bringing you the latest news and insights from a youth perspective.',
  'نحن متحمسون لإطلاق منصتنا الجديدة المخصصة لتقديم آخر الأخبار والرؤى من منظور الشباب.',
  'General',
  ARRAY['announcement', 'welcome', 'youth', 'news'],
  'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=400&fit=crop',
  'published',
  true,
  (SELECT id FROM public.users WHERE email = 'admin@yna.news' LIMIT 1)
),
(
  'youth-climate-activism',
  'Youth Leading the Climate Movement',
  'الشباب يقودون حركة المناخ',
  'Young people around the world are at the forefront of climate activism, demanding action from governments and corporations to address the climate crisis. From Greta Thunberg''s school strikes to local youth-led initiatives, young climate activists are making their voices heard and creating meaningful change.

Recent studies show that young people are disproportionately affected by climate change, as they will live with its consequences for decades to come. This has motivated a generation of activists who are not willing to wait for others to solve the problem.

Youth-led organizations are organizing protests, lobbying politicians, and developing innovative solutions to environmental challenges. Their fresh perspectives and digital-native approaches are bringing new energy to the climate movement.

From renewable energy projects to sustainable agriculture initiatives, young people are proving that age is not a barrier to making a real impact on environmental issues.',
  'الشباب حول العالم في المقدمة من نشاط المناخ، يطالبون بالعمل من الحكومات والشركات لمعالجة أزمة المناخ. من إضرابات غريتا تونبرغ المدرسية إلى المبادرات المحلية التي يقودها الشباب، النشطاء الشباب يجعلون أصواتهم مسموعة ويحدثون تغييراً ذا معنى.

تظهر الدراسات الحديثة أن الشباب يتأثرون بشكل غير متناسب بتغير المناخ، حيث سيعيشون مع عواقبه لعقود قادمة. هذا حفز جيلاً من النشطاء غير المستعدين للانتظار حتى يحل آخرون المشكلة.

المنظمات التي يقودها الشباب تنظم الاحتجاجات وتضغط على السياسيين وتطور حلولاً مبتكرة للتحديات البيئية. وجهات نظرهم الجديدة ونهجهم الرقمي الأصلي يجلبان طاقة جديدة لحركة المناخ.

من مشاريع الطاقة المتجددة إلى مبادرات الزراعة المستدامة، الشباب يثبتون أن العمر ليس حاجزاً أمام إحداث تأثير حقيقي على القضايا البيئية.',
  'Young climate activists are making their voices heard and creating meaningful change in the fight against climate crisis.',
  'النشطاء الشباب في مجال المناخ يجعلون أصواتهم مسموعة ويحدثون تغييراً ذا معنى في الكفاح ضد أزمة المناخ.',
  'Environment',
  ARRAY['climate', 'environment', 'activism', 'youth'],
  'https://images.unsplash.com/photo-1569163139394-de4e4f43e4e3?w=800&h=400&fit=crop',
  'published',
  true,
  (SELECT id FROM public.users WHERE email = 'admin@yna.news' LIMIT 1)
),
(
  'digital-generation-challenges',
  'Growing Up Digital: Challenges and Opportunities',
  'النمو في العصر الرقمي: التحديات والفرص',
  'The digital generation faces unique challenges and opportunities that previous generations never experienced. Social media, online learning, digital communication, and virtual experiences have fundamentally changed how young people interact with the world.

While technology offers unprecedented access to information, education, and global connections, it also presents challenges such as digital addiction, cyberbullying, privacy concerns, and the pressure to maintain an online presence.

Young people today are digital natives who have grown up with smartphones, social media, and instant access to information. This has shaped their learning styles, communication preferences, and worldview in profound ways.

Experts are studying how to harness the benefits of digital technology while mitigating its potential negative effects on youth development, mental health, and social skills.',
  'الجيل الرقمي يواجه تحديات وفرص فريدة لم تشهدها الأجيال السابقة. وسائل التواصل الاجتماعي والتعلم الإلكتروني والتواصل الرقمي والتجارب الافتراضية غيرت بشكل جذري طريقة تفاعل الشباب مع العالم.

بينما تقدم التكنولوجيا وصولاً غير مسبوق للمعلومات والتعليم والاتصالات العالمية، فإنها تطرح أيضاً تحديات مثل الإدمان الرقمي والتنمر الإلكتروني ومخاوف الخصوصية والضغط للحفاظ على حضور إلكتروني.

الشباب اليوم هم سكان رقميون أصليون نشأوا مع الهواتف الذكية ووسائل التواصل الاجتماعي والوصول الفوري للمعلومات. هذا شكل أساليب تعلمهم وتفضيلات التواصل ونظرتهم للعالم بطرق عميقة.

الخبراء يدرسون كيفية الاستفادة من فوائد التكنولوجيا الرقمية مع تخفيف آثارها السلبية المحتملة على تطور الشباب والصحة النفسية والمهارات الاجتماعية.',
  'Exploring how the digital generation navigates unique challenges and opportunities in our increasingly connected world.',
  'استكشاف كيفية تعامل الجيل الرقمي مع التحديات والفرص الفريدة في عالمنا المترابط بشكل متزايد.',
  'Technology',
  ARRAY['digital', 'technology', 'social-media', 'youth'],
  'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=400&fit=crop',
  'published',
  false,
  (SELECT id FROM public.users WHERE email = 'admin@yna.news' LIMIT 1)
),
(
  'youth-entrepreneurship-trends',
  'The Rise of Young Entrepreneurs',
  'صعود رواد الأعمال الشباب',
  'Young entrepreneurs are reshaping the business landscape with innovative ideas, tech-savvy approaches, and fresh perspectives on traditional industries. From tech startups to social enterprises, young people are proving that age is not a barrier to business success.

The rise of digital platforms, social media marketing, and remote work has lowered the barriers to entry for young entrepreneurs. Many are starting businesses from their dorm rooms or childhood bedrooms, leveraging online tools and networks to build global companies.

Young entrepreneurs often bring unique advantages to their ventures: they understand their generation''s preferences, are comfortable with new technologies, and are willing to take risks that more established business leaders might avoid.

Success stories of young entrepreneurs inspire others to pursue their business ideas and contribute to economic growth and innovation.',
  'رواد الأعمال الشباب يعيدون تشكيل المشهد التجاري بأفكار مبتكرة ونهج تقني متقدم ووجهات نظر جديدة على الصناعات التقليدية. من الشركات الناشئة التقنية إلى المؤسسات الاجتماعية، الشباب يثبتون أن العمر ليس حاجزاً أمام النجاح التجاري.

صعود المنصات الرقمية والتسويق عبر وسائل التواصل الاجتماعي والعمل عن بُعد قلل من حواجز الدخول لرواد الأعمال الشباب. كثيرون يبدأون أعمالهم من غرف السكن الجامعي أو غرف الطفولة، مستفيدين من الأدوات والشبكات الإلكترونية لبناء شركات عالمية.

رواد الأعمال الشباب غالباً ما يجلبون مزايا فريدة لمشاريعهم: يفهمون تفضيلات جيلهم، مرتاحون مع التقنيات الجديدة، ومستعدون لأخذ مخاطر قد يتجنبها قادة الأعمال الأكثر رسوخاً.

قصص نجاح رواد الأعمال الشباب تلهم آخرين لمتابعة أفكارهم التجارية والمساهمة في النمو الاقتصادي والابتكار.',
  'Young entrepreneurs are reshaping business with innovation, proving age is not a barrier to success.',
  'رواد الأعمال الشباب يعيدون تشكيل الأعمال بالابتكار، مثبتين أن العمر ليس حاجزاً أمام النجاح.',
  'Technology',
  ARRAY['entrepreneurship', 'business', 'startups', 'innovation'],
  'https://images.unsplash.com/photo-1556761175-4b46a572b786?w=800&h=400&fit=crop',
  'published',
  true,
  (SELECT id FROM public.users WHERE email = 'admin@yna.news' LIMIT 1)
);

-- Insert settings
INSERT INTO settings (key, value) VALUES
  ('maintenance_mode', 'false'),
  ('default_language', 'en'),
  ('site_title_en', 'YNA - Youth News Agency'),
  ('site_title_ar', 'وكالة أنباء الشباب'),
  ('site_description_en', 'Latest news and insights from a youth perspective'),
  ('site_description_ar', 'آخر الأخبار والرؤى من منظور الشباب')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

-- Add some view statistics
INSERT INTO site_stats (post_id, view_count, date) 
SELECT 
  p.id,
  (random() * 100)::integer + 10,
  CURRENT_DATE - (random() * 30)::integer
FROM posts p;

-- Update post views based on stats
UPDATE posts 
SET views = (
  SELECT COALESCE(SUM(view_count), 0)
  FROM site_stats 
  WHERE site_stats.post_id = posts.id
);