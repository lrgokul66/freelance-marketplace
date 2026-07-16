
-- ============================================================
-- FreelanceHub Sample Data
-- All passwords are: Password123!
-- Run AFTER schema.sql on an existing freelance_marketplace DB
-- ============================================================

USE freelance_marketplace;

SET FOREIGN_KEY_CHECKS = 0;

-- ─────────────────────────────────────────────────────────────
-- USERS  (5 clients: id 101-105 | 10 freelancers: id 106-115)
-- ─────────────────────────────────────────────────────────────
INSERT INTO users (id, email, password_hash, role, first_name, last_name, is_verified, is_active) VALUES
(101, 'arjun.sharma@nexatech.in',      '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'client',     'Arjun',     'Sharma',    1, 1),
(102, 'priya.mehta@cloudbridge.co',    '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'client',     'Priya',     'Mehta',     1, 1),
(103, 'vikram.nair@infospark.io',      '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'client',     'Vikram',    'Nair',      1, 1),
(104, 'sunita.agarwal@digiventure.in', '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'client',     'Sunita',    'Agarwal',   1, 1),
(105, 'rohit.pillai@zestmedia.com',    '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'client',     'Rohit',     'Pillai',    1, 1),
(106, 'deepak.verma@gmail.com',        '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Deepak',    'Verma',     1, 1),
(107, 'kavita.rao@gmail.com',          '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Kavita',    'Rao',       1, 1),
(108, 'sanjay.gupta@outlook.com',      '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Sanjay',    'Gupta',     1, 1),
(109, 'ananya.krishnan@gmail.com',     '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Ananya',    'Krishnan',  1, 1),
(110, 'rahul.joshi@yahoo.com',         '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Rahul',     'Joshi',     1, 1),
(111, 'meera.patel@gmail.com',         '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Meera',     'Patel',     1, 1),
(112, 'suresh.iyer@gmail.com',         '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Suresh',    'Iyer',      1, 1),
(113, 'pooja.singh@outlook.com',       '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Pooja',     'Singh',     1, 1),
(114, 'aditya.bose@gmail.com',         '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Aditya',    'Bose',      1, 1),
(115, 'lakshmi.nambiar@gmail.com',     '$2b$12$GajOs36PbJc8FXR0VT62ZOrbFL9RCax9uT5I12wyp/JSxNweWO1gG', 'freelancer', 'Lakshmi',   'Nambiar',   1, 1);

-- ─────────────────────────────────────────────────────────────
-- CLIENT PROFILES
-- ─────────────────────────────────────────────────────────────
INSERT INTO client_profiles (id, user_id, company, website, location, phone, description) VALUES
(101, 101, 'NexaTech Solutions',    'https://nexatech.in',       'Bengaluru, Karnataka',   '+91 98400 11001', 'IT product company building SaaS tools for SMEs across India.'),
(102, 102, 'CloudBridge Pvt Ltd',   'https://cloudbridge.co',    'Mumbai, Maharashtra',    '+91 98201 22002', 'Cloud infrastructure and DevOps consulting firm.'),
(103, 103, 'InfoSpark Technologies','https://infospark.io',      'Hyderabad, Telangana',   '+91 99001 33003', 'Data analytics and AI solutions for e-commerce brands.'),
(104, 104, 'DigiVenture India',     'https://digiventure.in',    'Delhi, NCR',             '+91 98111 44004', 'Digital marketing agency focused on growth for D2C brands.'),
(105, 105, 'ZestMedia Studios',     'https://zestmedia.com',     'Chennai, Tamil Nadu',    '+91 94401 55005', 'Creative media production house specialising in short-form content.');

-- ─────────────────────────────────────────────────────────────
-- FREELANCER PROFILES
-- ─────────────────────────────────────────────────────────────
INSERT INTO freelancer_profiles (id, user_id, headline, bio, hourly_rate, availability, languages) VALUES
(106, 106, 'Full-Stack MERN Developer',       'Passionate developer with 6 years building scalable web apps using React, Node.js and MongoDB. Love clean code and test-driven development.',  1800.00, 'full_time',  'English, Hindi, Marathi'),
(107, 107, 'UI/UX Designer & Figma Expert',   'Creative designer with 5 years crafting user-centric interfaces. Expert in Figma, Adobe XD and translating wireframes to pixel-perfect HTML.', 1500.00, 'part_time',  'English, Kannada'),
(108, 108, 'Python & Data Science Specialist','Data scientist with 7 years in ML/AI. Proficient in scikit-learn, TensorFlow, pandas and building production-ready ML pipelines.',              2200.00, 'full_time',  'English, Hindi, Telugu'),
(109, 109, 'Android & Flutter Developer',     'Mobile developer building cross-platform apps with Flutter and native Android. Delivered 20+ apps on Play Store.',                             1600.00, 'full_time',  'English, Tamil'),
(110, 110, 'DevOps & Cloud Engineer',         'AWS-certified DevOps engineer. Expert in Docker, Kubernetes, Terraform and CI/CD pipelines. 5 years in production infrastructure.',           2000.00, 'full_time',  'English, Hindi'),
(111, 111, 'WordPress & PHP Developer',       'Web developer specialising in WordPress, WooCommerce and custom PHP solutions. Delivered 50+ client websites.',                                  800.00, 'part_time',  'English, Hindi, Gujarati'),
(112, 112, 'Content Writer & SEO Strategist', 'SEO-focused content writer with 6 years producing blog posts, whitepapers and case studies for SaaS and tech brands.',                          700.00, 'full_time',  'English, Bengali, Hindi'),
(113, 113, 'Graphic Designer & Brand Expert', 'Brand identity designer with 5 years creating logos, packaging and social media assets. Expert in Illustrator, Photoshop and Canva Pro.',       1100.00, 'part_time',  'English, Hindi'),
(114, 114, 'React.js & TypeScript Developer', 'Frontend engineer with 4 years building performant SPAs and micro-frontends using React, Redux and TypeScript.',                                1700.00, 'full_time',  'English, Bengali, Hindi'),
(115, 115, 'iOS & Swift Developer',           'iOS engineer with 5 years developing Swift apps, integrating REST APIs and publishing to the App Store. Core Data and SwiftUI expert.',         1900.00, 'full_time',  'English, Malayalam');

-- ─────────────────────────────────────────────────────────────
-- FREELANCER SKILLS
-- ─────────────────────────────────────────────────────────────
INSERT INTO freelancer_skills (freelancer_id, skill_id) VALUES
(106,  2),(106, 11),(106, 14),(106, 18),(106, 15),(106, 10),(106,  9),(106, 26),
(107, 28),(107, 29),(107,  9),(107, 10),(107, 30),(107, 31),(107, 37),(107, 27),
(108,  1),(108, 47),(108, 48),(108, 49),(108, 16),(108, 18),(108, 26),(108, 24),
(109, 45),(109, 44),(109, 46),(109,  2),(109, 15),(109, 18),(109, 26),
(110, 20),(110, 21),(110, 22),(110, 25),(110,  7),(110, 26),(110, 23),(110, 24),
(111, 40),(111,  3),(111, 41),(111, 10),(111,  9),(111, 34),(111, 35),
(112, 32),(112, 33),(112, 34),(112, 35),(112, 36),(112,  9),
(113, 27),(113, 31),(113, 30),(113, 37),(113, 38),(113, 28),(113, 29),
(114, 11),(114, 15),(114,  2),(114, 14),(114, 10),(114,  9),(114, 18),(114, 26),
(115, 43),(115, 14),(115, 15),(115, 26),(115, 22);

-- ─────────────────────────────────────────────────────────────
-- PORTFOLIO
-- ─────────────────────────────────────────────────────────────
INSERT INTO portfolio (id, freelancer_id, title, description, link) VALUES
(1,  106, 'E-Commerce Platform',       'Built a full MERN stack e-commerce site with cart, payments and admin panel.', 'https://github.com/deepakverma/ecommerce'),
(2,  106, 'Real-time Chat App',        'Socket.io-powered group chat with rooms, file sharing and emoji support.',     'https://github.com/deepakverma/chatapp'),
(3,  106, 'Task Manager SaaS',         'Multi-tenant SaaS task manager with Kanban board and time-tracking.',          'https://taskmanager.deepakverma.dev'),
(4,  107, 'FinTech Mobile UI Kit',     'Comprehensive Figma UI kit for fintech apps — 60+ screens, dark & light.',      'https://figma.com/kavitarao/fintech'),
(5,  107, 'Healthcare App Redesign',   'End-to-end UX research and visual redesign for a telemedicine Android app.',   'https://behance.net/kavitarao/healthcare'),
(6,  107, 'Brand Guidebook — Bloom',  'Complete brand identity: logo, typography, colour palette and usage guidelines.','https://behance.net/kavitarao/bloom'),
(7,  108, 'Customer Churn Predictor',  'ML pipeline predicting telecom churn with 92% accuracy; deployed on AWS.',      'https://github.com/sanjaygupta/churn'),
(8,  108, 'Image Classification API',  'Fast CNN model served via FastAPI — 95% accuracy on custom dataset.',           'https://github.com/sanjaygupta/imgclassify'),
(9,  108, 'NLP Sentiment Dashboard',  'Bert-fine-tuned sentiment analyser with interactive Streamlit dashboard.',       'https://github.com/sanjaygupta/sentiment'),
(10, 109, 'Grocery Delivery App',     'Flutter grocery app with live order tracking, push notifications and Razorpay.', 'https://play.google.com/store/apps/grocery'),
(11, 109, 'Fitness Tracker',          'Native Android app for workout logging with BLE heart-rate monitor integration.', 'https://play.google.com/store/apps/fitness'),
(12, 109, 'Language Learning App',    'Cross-platform Flutter app with spaced-repetition flashcards and speech input.',  'https://github.com/ananyak/langlearn'),
(13, 110, 'Kubernetes Cluster Setup', 'Automated multi-node K8s cluster on AWS EKS with Helm charts and monitoring.',    'https://github.com/rahul/k8s-cluster'),
(14, 110, 'CI/CD Pipeline Template',  'Reusable GitHub Actions + ArgoCD template for zero-downtime deployments.',        'https://github.com/rahul/cicd-template'),
(15, 111, 'Organic Food WooCommerce', 'Custom WooCommerce store with subscription products and membership plugin.',       'https://organicfood.in'),
(16, 111, 'Ayurveda Clinic Website',  'WordPress site with online booking, blog and Razorpay payment gateway.',          'https://ayurvedaclinic.in'),
(17, 112, 'SaaS Content Library',     '80-article content library for a B2B SaaS company — all SEO-optimised.',         'https://medium.com/@sureshiyer'),
(18, 113, 'Tech Startup Logo Suite',  'Brand identity — logo, card, letterhead, social assets for 3 startups.',          'https://behance.net/poojasingh'),
(19, 114, 'Dashboard Analytics App',  'React + TypeScript SPA with recharts, multi-tenant auth and role-based views.',   'https://github.com/adityabose/analytics'),
(20, 115, 'Banking iOS App',          'Swift app with Face ID, Core Data and REST integration for a regional bank.',      'https://apps.apple.com/banking-app');

-- ─────────────────────────────────────────────────────────────
-- EDUCATION
-- ─────────────────────────────────────────────────────────────
INSERT INTO education (id, freelancer_id, degree, institution, year) VALUES
(1,  106, 'B.E. Computer Engineering',   'Pune University',                    2018),
(2,  107, 'B.Des Interaction Design',    'National Institute of Design, Pune', 2019),
(3,  108, 'M.Tech Data Science',         'IIT Hyderabad',                      2017),
(4,  109, 'B.Tech Information Technology','SRM Institute of Technology',       2020),
(5,  110, 'B.Tech Computer Science',     'BITS Pilani',                        2019),
(6,  111, 'BCA',                         'Gujarat University',                  2020),
(7,  112, 'BA English Literature',       'Presidency University, Kolkata',     2018),
(8,  113, 'B.Des Visual Communication', 'NIFT Jaipur',                         2019),
(9,  114, 'B.Tech Computer Science',     'Jadavpur University',                2020),
(10, 115, 'MCA',                         'Cochin University of Science & Technology', 2019);

-- ─────────────────────────────────────────────────────────────
-- EXPERIENCE
-- ─────────────────────────────────────────────────────────────
INSERT INTO experience (id, freelancer_id, title, company, years, description) VALUES
(1,  106, 'Senior Full-Stack Developer', 'TCS Digital',             '2020-2023', 'Led a team of 4 building microservices on AWS. Delivered 3 major product releases.'),
(2,  106, 'Junior Developer',            'Wipro Ltd',               '2018-2020', 'Developed REST APIs using Node.js and maintained MySQL databases.'),
(3,  107, 'Lead UI Designer',            'Infosys BPM',             '2021-2023', 'Designed end-to-end workflows for 2 banking portals used by 1M+ customers.'),
(4,  107, 'UX Intern',                   'Thought Works',           '2019-2021', 'Conducted user research, wireframing and usability testing for a FinTech client.'),
(5,  108, 'Data Scientist',              'Amazon India',            '2019-2023', 'Built recommendation engine increasing CTR by 18%. Owned NLP sentiment pipeline.'),
(6,  108, 'ML Engineer Intern',          'IIT Hyderabad Research Lab','2017-2019','Worked on image recognition models using PyTorch; published paper in IEEE.'),
(7,  109, 'Android Developer',           'Zoho Corporation',        '2020-2023', 'Shipped 4 production Android apps. Mentored 2 junior developers.'),
(8,  110, 'DevOps Engineer',             'HCL Technologies',        '2019-2023', 'Managed 200-node Kubernetes cluster, reduced infra costs by 32% via autoscaling.'),
(9,  111, 'WordPress Developer',         'WebCraft Agency Ahmedabad','2020-2023', 'Delivered 35+ client WordPress websites with custom plugins and WooCommerce.'),
(10, 112, 'Senior Content Strategist',   'Moengage (SaaS)',         '2020-2023', 'Produced 200+ SEO articles ranking on page 1. Grew organic traffic by 140%.'),
(11, 113, 'Graphic Designer',            'Ogilvy India',            '2019-2023', 'Created brand assets and campaign visuals for FMCG and retail clients.'),
(12, 114, 'Frontend Engineer',           'Freshworks',              '2020-2023', 'Built React micro-frontends used by 50,000+ B2B users across 15 countries.'),
(13, 115, 'iOS Developer',               'Tata Consultancy Services','2019-2023', 'Developed 3 iOS apps for banking and insurance domains with 100K+ downloads.');

-- ─────────────────────────────────────────────────────────────
-- CERTIFICATIONS
-- ─────────────────────────────────────────────────────────────
INSERT INTO certifications (id, freelancer_id, name, issuer, year) VALUES
(1,  106, 'MongoDB Certified Developer',   'MongoDB University',    2021),
(2,  106, 'AWS Certified Cloud Practitioner','Amazon Web Services', 2022),
(3,  107, 'Google UX Design Certificate',  'Google / Coursera',     2021),
(4,  107, 'Figma Advanced Certification',  'Figma',                 2022),
(5,  108, 'TensorFlow Developer Certificate','Google',              2020),
(6,  108, 'AWS Machine Learning Specialty', 'Amazon Web Services',  2021),
(7,  109, 'Google Associate Android Developer','Google',            2021),
(8,  109, 'Flutter Certified Application Developer','Google',       2022),
(9,  110, 'AWS Certified DevOps Engineer', 'Amazon Web Services',   2021),
(10, 110, 'Certified Kubernetes Administrator','CNCF',              2022),
(11, 111, 'WordPress Developer Certification','Automattic',         2021),
(12, 112, 'HubSpot Content Marketing',     'HubSpot Academy',       2020),
(13, 112, 'Google Analytics Individual',   'Google',                2021),
(14, 113, 'Adobe Certified Professional',  'Adobe',                 2021),
(15, 114, 'Meta Front-End Developer',      'Meta / Coursera',       2022),
(16, 115, 'Apple Certified iOS Developer', 'Apple',                 2020);

-- ─────────────────────────────────────────────────────────────
-- PROJECTS
-- ─────────────────────────────────────────────────────────────
INSERT INTO projects (id, client_id, title, category, description, budget_min, budget_max, experience_level, duration, deadline, status, hired_freelancer_id) VALUES
(1,  101, 'Build a SaaS Invoicing Tool',         'Web Development', 'Need a React + Node.js SaaS invoicing app with Razorpay integration, PDF export and multi-tenant auth.', 50000, 120000, 'expert',       '3 months', '2026-09-30', 'in_progress', 106),
(2,  101, 'Company Website Redesign',             'Web Development', 'Redesign our corporate website in Next.js — mobile-first, SEO-friendly, CMS-backed.',                    30000,  80000, 'intermediate', '2 months', '2026-08-31', 'open',        NULL),
(3,  101, 'HR Analytics Dashboard',               'Data Science',    'Build a Python dashboard using our HR data to visualise attrition, headcount and performance KPIs.',      40000,  90000, 'expert',       '2 months', '2026-08-15', 'hiring',      NULL),
(4,  102, 'AWS Infrastructure Migration',         'Cloud/DevOps',    'Migrate our on-premise services to AWS — EC2, RDS, S3, CloudFront. IaC via Terraform.',                   60000, 150000, 'expert',       '4 months', '2026-10-31', 'in_progress', 110),
(5,  102, 'Mobile App for Fleet Tracking',        'Mobile Dev',      'Flutter app for real-time GPS fleet tracking with driver dashboards and alert notifications.',              45000, 100000, 'expert',       '3 months', '2026-09-15', 'completed',   109),
(6,  102, 'Brand Identity Package',               'Design',          'Full brand identity: logo, colour palette, typography, business cards and social media kit.',               15000,  40000, 'intermediate', '6 weeks',  '2026-07-31', 'completed',   113),
(7,  103, 'Customer Churn ML Model',              'Data Science',    'Develop an ML model predicting customer churn for our subscription product. Flask API endpoint needed.',    55000, 130000, 'expert',       '3 months', '2026-09-01', 'in_progress', 108),
(8,  103, 'E-Commerce Android App',               'Mobile Dev',      'Native Android app for our Shopify store. Product browsing, cart, push notifications and payments.',        35000,  80000, 'intermediate', '2 months', '2026-08-01', 'open',        NULL),
(9,  103, 'SEO Content Campaign (20 Articles)',   'Content Writing', 'Need 20 long-form SEO articles (1500-2500 words each) on data analytics topics targeting SaaS audience.',    14000,  30000, 'intermediate', '6 weeks',  '2026-07-20', 'completed',   112),
(10, 104, 'D2C Brand Launch Website',             'Web Development', 'Shopify plus WordPress landing page for skincare D2C brand. Must integrate with Klaviyo and Meta Pixel.',   25000,  60000, 'intermediate', '6 weeks',  '2026-08-15', 'open',        NULL),
(11, 104, 'Social Media Design Pack',             'Design',          '30 social media templates in Canva + Illustrator for Instagram, Facebook and LinkedIn.',                     10000,  25000, 'entry',        '3 weeks',  '2026-07-10', 'completed',   113),
(12, 104, 'Google Ads + SEO Strategy',            'Digital Marketing','Develop a comprehensive SEO and PPC strategy with keyword research and 6-month content calendar.',          18000,  45000, 'intermediate', '2 months', '2026-08-30', 'hiring',      NULL),
(13, 105, 'Video Editing — YouTube Series',       'Video/Media',     '10 YouTube episodes (20-30 mins each) need professional edit: colour grade, motion titles, sound mix.',      20000,  55000, 'intermediate', '2 months', '2026-08-20', 'open',        NULL),
(14, 105, 'iOS App for Event Ticketing',          'Mobile Dev',      'Swift iOS app with QR ticket generation, Razorpay checkout and event organiser admin panel.',                50000, 110000, 'expert',       '3 months', '2026-10-01', 'in_progress', 115),
(15, 105, 'React Dashboard for Analytics',        'Web Development', 'React + TypeScript dashboard with recharts, real-time WebSocket data and role-based access control.',         40000,  90000, 'expert',       '2 months', '2026-08-31', 'completed',   114);

-- ─────────────────────────────────────────────────────────────
-- PROJECT SKILLS
-- ─────────────────────────────────────────────────────────────
INSERT INTO project_skills (project_id, skill_id) VALUES
(1, 11),(1, 14),(1,  2),(1, 18),
(2, 11),(2,  9),(2, 10),(2, 34),
(3,  1),(3, 47),(3, 48),(3, 16),
(4, 22),(4, 20),(4, 21),(4, 25),
(5, 45),(5, 44),(5, 18),(5,  2),
(6, 27),(6, 29),(6, 30),(6, 31),
(7,  1),(7, 47),(7, 48),(7, 49),
(8, 44),(8,  4),(8, 18),
(9, 32),(9, 34),(9, 33),
(10, 40),(10,  3),(10, 41),(10, 34),
(11, 27),(11, 31),(11, 35),
(12, 34),(12, 35),(12, 33),
(13, 37),(13, 38),
(14, 43),(14, 14),(14, 22),
(15, 11),(15, 15),(15,  2);

-- ─────────────────────────────────────────────────────────────
-- PROJECT FILES
-- ─────────────────────────────────────────────────────────────
INSERT INTO project_files (id, project_id, filename, original_name) VALUES
(1,  1, 'pf_101_brief.pdf',      'SaaS_Invoicing_Brief.pdf'),
(2,  4, 'pf_102_infra_docs.pdf', 'AWS_Migration_Arch.pdf'),
(3,  7, 'pf_103_churn_data.csv', 'Churn_Dataset_Sample.csv'),
(4, 14, 'pf_105_wireframes.pdf', 'iOS_Ticketing_Wireframes.pdf');

-- ─────────────────────────────────────────────────────────────
-- SAVED PROJECTS
-- ─────────────────────────────────────────────────────────────
INSERT INTO saved_projects (id, freelancer_id, project_id) VALUES
(1, 106,  2),(2, 106, 10),
(3, 107,  6),(4, 107, 11),
(5, 108,  3),(6, 108,  8),
(7, 109, 13),(8, 109,  8),
(9, 110,  4),(10,111, 10),
(11,112, 12),(12,113,  6),
(13,114,  2),(14,115, 13);

-- ─────────────────────────────────────────────────────────────
-- PROPOSALS
-- ─────────────────────────────────────────────────────────────
INSERT INTO proposals (id, project_id, freelancer_id, cover_letter, bid_amount, delivery_days, status) VALUES
(1, 1, 106, 'I have 6 years of MERN experience and have built 3 SaaS products with Razorpay integration. I can deliver a production-ready invoicing tool with full test coverage.', 95000, 75, 'accepted'),
(2, 1, 114, 'I specialize in React and TypeScript SPAs. I can handle the frontend while collaborating on the Node.js API layer. Let us schedule a discovery call.', 105000, 80, 'rejected'),
(3, 2, 106, 'I have redesigned 5 corporate websites in Next.js with CMS integration. I can deliver SEO-optimised, mobile-first code meeting your brief exactly.', 65000, 55, 'pending'),
(4, 3, 108, 'Building Python analytics dashboards is my core strength. I built a similar HR dashboard for Amazon India. I can start immediately.', 78000, 60, 'pending'),
(5, 4, 110, 'I am AWS-certified and managed a 200-node Kubernetes cluster at HCL. I will architect, migrate and document the full infrastructure using Terraform IaC.', 130000, 100, 'accepted'),
(6, 4, 106, 'While primarily a full-stack dev, I have hands-on AWS experience. I can contribute to the migration alongside your DevOps team.', 90000, 90, 'rejected'),
(7, 5, 109, 'I have published 4 Flutter apps integrating GPS and push notifications. The fleet-tracking app aligns perfectly with my portfolio.', 88000, 70, 'accepted'),
(8, 6, 113, 'Brand identity is my speciality. I delivered complete brand kits for 3 tech startups. I will share my detailed brand process doc.', 35000, 30, 'accepted'),
(9, 7, 108, 'I built a churn prediction model at Amazon with 92% accuracy. I can replicate and improve that for your subscription data.', 120000, 75, 'accepted'),
(10, 9, 112, 'I have produced 200+ SEO-optimised SaaS articles. All 20 articles will be researched, keyword-mapped and interlinked for maximum ranking impact.', 28000, 35, 'accepted'),
(11, 11, 113, 'I create social media templates daily for FMCG brands at Ogilvy. 30 polished, brand-consistent templates delivered within 3 weeks.', 22000, 21, 'accepted'),
(12, 12, 112, 'SEO strategy is central to my work. I will produce a full keyword research report, competitor analysis and 6-month content calendar.', 38000, 50, 'pending'),
(13, 14, 115, 'I built 3 iOS apps with Razorpay integration at TCS. I will deliver a fully tested Swift app with QR ticketing and an Xcode project handoff.', 100000, 80, 'accepted'),
(14, 15, 114, 'This project matches my exact expertise. I delivered a very similar React + TypeScript dashboard at Freshworks. I can start this week.', 82000, 60, 'accepted');

-- ─────────────────────────────────────────────────────────────
-- PROPOSAL FILES
-- ─────────────────────────────────────────────────────────────
INSERT INTO proposal_files (id, proposal_id, filename, original_name) VALUES
(1, 1,  'prf_1_deepak_portfolio.pdf', 'Deepak_Verma_Portfolio.pdf'),
(2, 5,  'prf_5_rahul_cv.pdf',         'Rahul_Joshi_CV.pdf'),
(3, 9,  'prf_9_sanjay_case.pdf',      'Sanjay_Churn_CaseStudy.pdf'),
(4, 13, 'prf_13_lakshmi_cv.pdf',      'Lakshmi_Nambiar_CV.pdf');

-- ─────────────────────────────────────────────────────────────
-- MESSAGES
-- ─────────────────────────────────────────────────────────────
INSERT INTO messages (id, sender_id, receiver_id, project_id, content, is_read) VALUES
(1,  101, 106, 1, 'Hi Deepak, welcome on board! Let us start with the invoice module first. Can you share your week-1 plan?', 1),
(2,  106, 101, 1, 'Absolutely Arjun! I have set up the project repo on GitHub and drafted the DB schema. I will share the link shortly.', 1),
(3,  101, 106, 1, 'Great. Let us do a quick standup every Monday at 10 AM IST. Does that work for you?', 1),
(4,  106, 101, 1, 'Works perfectly. I have already pushed the auth module. Please review when you get a chance.', 0),
(5,  102, 110, 4, 'Rahul, can you confirm the migration timeline for the RDS cluster? The compliance audit is in October.', 1),
(6,  110, 102, 4, 'Hi Priya, I have completed the Terraform scripts for VPC and EC2. RDS migration is scheduled for next week.', 1),
(7,  102, 110, 4, 'Perfect. Please keep me updated on any downtime windows. We need 48 hours notice for the team.', 0),
(8,  102, 109, 5, 'Ananya, the Flutter app looks great! Can you add an offline map cache so drivers see routes without internet?', 1),
(9,  109, 102, 5, 'That is a great point. I will add the offline tile cache using the flutter_map package. Should be ready by Friday.', 1),
(10, 103, 108, 7, 'Sanjay, our data team has prepared the CSV export of 3 years of subscription data. I will send the link via email.', 1),
(11, 108, 103, 7, 'Received it, Vikram. Initial EDA shows strong signals for the churn model. I will have a first-pass accuracy report by end of week.', 1),
(12, 104, 113, 6, 'Pooja, we love the first draft of the logo! Can you try a version with a darker shade of the primary green?', 1),
(13, 113, 104, 6, 'Absolutely! I have uploaded 3 revised variants to the shared Figma link. Please check and let me know your preference.', 1),
(14, 105, 115, 14,'Lakshmi, the beta build on TestFlight looks clean. One request: can you add haptic feedback when the QR code is scanned?', 1),
(15, 115, 105, 14,'Sure Rohit! I will add UIImpactFeedbackGenerator for the scan animation and push an updated build today.', 0),
(16, 105, 114, 15,'Aditya, the real-time charts are exactly what we needed. Please add a date-range filter to the revenue widget next.', 1),
(17, 114, 105, 15,'On it! I will wire up the DateRangePicker and filter the WebSocket subscription by timestamp. Done by tomorrow.', 1);

-- ─────────────────────────────────────────────────────────────
-- WORK SUBMISSIONS
-- ─────────────────────────────────────────────────────────────
INSERT INTO work_submissions (id, project_id, freelancer_id, file_path, original_name, notes, status, client_feedback) VALUES
(1,  5, 109, 'uploads/ws_fleet_v1.zip',   'FleetApp_v1.0_build.zip', 'First APK build — full GPS tracking and push notifications implemented.', 'approved', 'Great work Ananya! The GPS accuracy is impressive. Approved for production.'),
(2,  6, 113, 'uploads/ws_brand_kit.zip',  'Bloom_Brand_Kit.zip', 'Complete brand kit: SVG logos, colour swatches, typography guide and social templates.', 'approved', 'Exactly what we needed! Approved. Please invoice us.'),
(3,  9, 112, 'uploads/ws_articles.zip',   'SEO_Articles_20.zip', 'All 20 articles with SEO metadata, internal links and featured image suggestions included.', 'approved', 'Excellent quality. Every article is well-researched and perfectly structured.'),
(4, 11, 113, 'uploads/ws_social_pack.zip','Social_30_Templates.zip', '30 Canva + Illustrator templates across all 3 platforms. Editable source files included.', 'approved', 'Stunning templates! Very on-brand. Approved immediately.'),
(5, 15, 114, 'uploads/ws_dashboard.zip',  'Analytics_Dashboard_v2.zip', 'React build with full role-based access, WebSocket real-time data and 8 chart types.', 'approved', 'Aditya, the dashboard exceeds our expectations. Superb work!'),
(6,  1, 106, 'uploads/ws_invoice_alpha.zip','Invoicing_Alpha.zip', 'Auth module, invoice CRUD, PDF export and Razorpay webhook handler complete.', 'revision_requested', 'Client requested a revision on your work submission for "SaaS Invoicing Tool".');

-- ─────────────────────────────────────────────────────────────
-- PAYMENTS
-- ─────────────────────────────────────────────────────────────
INSERT INTO payments (id, project_id, client_id, freelancer_id, amount, currency, status, razorpay_order_id, razorpay_payment_id) VALUES
(1,  5, 102, 109,  88000.00, 'INR', 'completed', 'order_fleet_101', 'pay_fleet_101'),
(2,  6, 102, 113,  35000.00, 'INR', 'completed', 'order_brand_102', 'pay_brand_102'),
(3,  9, 103, 112,  28000.00, 'INR', 'completed', 'order_seo_103',   'pay_seo_103'),
(4, 11, 104, 113,  22000.00, 'INR', 'completed', 'order_soc_104',   'pay_soc_104'),
(5, 15, 105, 114,  82000.00, 'INR', 'completed', 'order_dash_105',  'pay_dash_105'),
(6,  4, 102, 110,  65000.00, 'INR', 'pending',   'order_aws_106',   NULL),
(7,  1, 101, 106,  47500.00, 'INR', 'pending',   'order_saas_107',  NULL),
(8, 14, 105, 115,  50000.00, 'INR', 'pending',   'order_ios_108',   NULL),
(9,  7, 103, 108,  60000.00, 'INR', 'pending',   'order_ml_109',    NULL);

-- ─────────────────────────────────────────────────────────────
-- TRANSACTIONS
-- ─────────────────────────────────────────────────────────────
INSERT INTO transactions (id, payment_id, type, amount, note) VALUES
(1, 1, 'payment', 88000.00, 'Full payment for Fleet Tracking Flutter app'),
(2, 1, 'fee',      4400.00, 'Platform fee 5% on payment #1'),
(3, 2, 'payment', 35000.00, 'Full payment for Bloom brand identity kit'),
(4, 2, 'fee',      1750.00, 'Platform fee 5% on payment #2'),
(5, 3, 'payment', 28000.00, 'Full payment for 20 SEO articles'),
(6, 3, 'fee',      1400.00, 'Platform fee 5% on payment #3'),
(7, 4, 'payment', 22000.00, 'Full payment for 30 social media templates'),
(8, 4, 'fee',      1100.00, 'Platform fee 5% on payment #4'),
(9, 5, 'payment', 82000.00, 'Full payment for Analytics React Dashboard'),
(10,5, 'fee',      4100.00, 'Platform fee 5% on payment #5');

-- ─────────────────────────────────────────────────────────────
-- REVIEWS
-- ─────────────────────────────────────────────────────────────
INSERT INTO reviews (id, project_id, reviewer_id, reviewee_id, rating, comment) VALUES
(1,  5, 102, 109, 5, 'Ananya delivered beyond expectations. The Flutter GPS tracking is silky smooth. Highly recommended!'),
(2,  5, 109, 102, 5, 'Priya was an amazing client — clear brief, prompt feedback and paid on time. Would love to work again.'),
(3,  6, 102, 113, 5, 'Pooja created a stunning brand identity. Creative, responsive and delivered on schedule.'),
(4,  6, 113, 102, 4, 'Great client with a clear vision. Feedback was constructive. Minor delays in approvals but overall wonderful.'),
(5,  9, 103, 112, 5, 'Suresh wrote exceptional SEO articles. All 20 ranked on page 1 within 6 weeks. Outstanding writer!'),
(6,  9, 112, 103, 5, 'Vikram had a very precise brief and gave detailed keyword targets. Made my job easy.'),
(7, 11, 104, 113, 5, 'Pooja designed 30 gorgeous templates perfectly matching our brand. Lightning fast turnaround.'),
(8, 11, 113, 104, 5, 'Sunita is a dream client — fast approvals, clear feedback and very fair payment.'),
(9, 15, 105, 114, 5, 'Aditya built our analytics dashboard to perfection. TypeScript code is clean and well-documented.'),
(10,15, 114, 105, 4, 'Rohit had a solid project brief. The scope expanded mid-project but he was fair in adjusting the budget.');

-- ─────────────────────────────────────────────────────────────
-- NOTIFICATIONS
-- ─────────────────────────────────────────────────────────────
INSERT INTO notifications (id, user_id, type, title, message, link, is_read) VALUES
(1,  106, 'proposal_accepted',  'Proposal Accepted',          'Your proposal for "Build a SaaS Invoicing Tool" has been accepted!',          '/freelancer/dashboard', 1),
(2,  110, 'proposal_accepted',  'Proposal Accepted',          'Your proposal for "AWS Infrastructure Migration" has been accepted!',           '/freelancer/dashboard', 1),
(3,  109, 'proposal_accepted',  'Proposal Accepted',          'Your proposal for "Mobile App for Fleet Tracking" has been accepted!',          '/freelancer/dashboard', 1),
(4,  113, 'proposal_accepted',  'Proposal Accepted',          'Your proposal for "Brand Identity Package" has been accepted!',                 '/freelancer/dashboard', 1),
(5,  108, 'proposal_accepted',  'Proposal Accepted',          'Your proposal for "Customer Churn ML Model" has been accepted!',                '/freelancer/dashboard', 1),
(6,  112, 'proposal_accepted',  'Proposal Accepted',          'Your proposal for "SEO Content Campaign" has been accepted!',                   '/freelancer/dashboard', 1),
(7,  115, 'proposal_accepted',  'Proposal Accepted',          'Your proposal for "iOS App for Event Ticketing" has been accepted!',            '/freelancer/dashboard', 1),
(8,  114, 'proposal_accepted',  'Proposal Accepted',          'Your proposal for "React Dashboard for Analytics" has been accepted!',          '/freelancer/dashboard', 1),
(9,  101, 'new_proposal',       'New Proposal Received',      'Deepak Verma submitted a proposal on "Build a SaaS Invoicing Tool".',           '/client/dashboard',    1),
(10, 102, 'new_proposal',       'New Proposal Received',      'Rahul Joshi submitted a proposal on "AWS Infrastructure Migration".',           '/client/dashboard',    1),
(11, 106, 'revision_requested', 'Revision Requested',         'Client requested a revision on your work submission for "SaaS Invoicing Tool".', '/freelancer/dashboard', 0),
(12, 102, 'payment_complete',   'Payment Released',           'Payment of ₹88,000 released for "Mobile App for Fleet Tracking".',              '/payment/history',     1),
(13, 109, 'payment_complete',   'Payment Received',           'You received ₹88,000 for completing "Mobile App for Fleet Tracking".',          '/payment/history',     1),
(14, 103, 'payment_complete',   'Payment Released',           'Payment of ₹28,000 released for "SEO Content Campaign".',                      '/payment/history',     1),
(15, 107, 'new_message',        'New Message',                'Priya Mehta sent you a message about your proposal.',                           '/chat/inbox',          0);

-- ─────────────────────────────────────────────────────────────
-- PASSWORD RESET TOKENS  (sample / expired — safe to include)
-- ─────────────────────────────────────────────────────────────
INSERT INTO password_reset_tokens (id, user_id, token, expires_at, used) VALUES
(1, 106, 'prt_deepak_abc123def456ghi789jkl012mno345pqr678stu901vwx234', '2026-07-01 10:00:00', 1),
(2, 109, 'prt_ananya_zyx987wvu654tsr321qpo098nml765kji432hgf109edc876', '2026-07-02 12:00:00', 1);

-- ─────────────────────────────────────────────────────────────
-- EMAIL VERIFICATION TOKENS  (sample / already used)
-- ─────────────────────────────────────────────────────────────
INSERT INTO email_verification_tokens (id, user_id, token, expires_at) VALUES
(1, 101, 'evt_101_arjun_aaaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllll', '2026-07-10 09:00:00'),
(2, 102, 'evt_102_priya_mmmmnnnnoooapppqqqrrrrssssttttuuuuvvvvwwwwxxxxyyy', '2026-07-10 09:00:00'),
(3, 106, 'evt_106_deepak_111122223333444455556666777788889999aaaabbbbcccc', '2026-07-10 09:00:00'),
(4, 108, 'evt_108_sanjay_ddddeeeeffffgggghhhhiiiijjjjkkkkllllmmmmnnnnooooo', '2026-07-10 09:00:00');

SET FOREIGN_KEY_CHECKS = 1;
