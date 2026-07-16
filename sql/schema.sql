-- ============================================================
-- Freelance Marketplace System — MySQL Schema (3NF)
-- Run this script against a fresh MySQL instance.
-- ============================================================

CREATE DATABASE IF NOT EXISTS freelance_marketplace
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE freelance_marketplace;

-- ─────────────────────────────────────────────────────────────
-- USERS  (core auth table — shared by Client & Freelancer)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            ENUM('client','freelancer') NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    is_verified     TINYINT(1) NOT NULL DEFAULT 0,
    is_active       TINYINT(1) NOT NULL DEFAULT 1,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role  (role)
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- CLIENT PROFILES
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS client_profiles (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL UNIQUE,
    company     VARCHAR(200),
    website     VARCHAR(255),
    location    VARCHAR(200),
    phone       VARCHAR(30),
    description TEXT,
    avatar      VARCHAR(255),
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- FREELANCER PROFILES
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS freelancer_profiles (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL UNIQUE,
    headline        VARCHAR(255),
    bio             TEXT,
    hourly_rate     DECIMAL(10,2) DEFAULT 0.00,
    availability    ENUM('full_time','part_time','not_available') DEFAULT 'full_time',
    avatar          VARCHAR(255),
    resume          VARCHAR(255),
    languages       VARCHAR(500),
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- SKILLS  (normalized lookup)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS skills (
    id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100) NOT NULL UNIQUE,
    INDEX idx_skill_name (name)
) ENGINE=InnoDB;

-- Freelancer ↔ Skill (many-to-many)
CREATE TABLE IF NOT EXISTS freelancer_skills (
    freelancer_id   INT UNSIGNED NOT NULL,
    skill_id        INT UNSIGNED NOT NULL,
    PRIMARY KEY (freelancer_id, skill_id),
    FOREIGN KEY (freelancer_id) REFERENCES freelancer_profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id)      REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- PORTFOLIO
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS portfolio (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    freelancer_id   INT UNSIGNED NOT NULL,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    image           VARCHAR(255),
    link            VARCHAR(500),
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (freelancer_id) REFERENCES freelancer_profiles(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- EDUCATION
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS education (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    freelancer_id   INT UNSIGNED NOT NULL,
    degree          VARCHAR(200) NOT NULL,
    institution     VARCHAR(200) NOT NULL,
    year            YEAR,
    description     TEXT,
    FOREIGN KEY (freelancer_id) REFERENCES freelancer_profiles(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- EXPERIENCE
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS experience (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    freelancer_id   INT UNSIGNED NOT NULL,
    title           VARCHAR(200) NOT NULL,
    company         VARCHAR(200) NOT NULL,
    years           VARCHAR(50),
    description     TEXT,
    FOREIGN KEY (freelancer_id) REFERENCES freelancer_profiles(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- CERTIFICATIONS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS certifications (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    freelancer_id   INT UNSIGNED NOT NULL,
    name            VARCHAR(200) NOT NULL,
    issuer          VARCHAR(200),
    year            YEAR,
    FOREIGN KEY (freelancer_id) REFERENCES freelancer_profiles(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- PROJECTS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    client_id       INT UNSIGNED NOT NULL,
    title           VARCHAR(255) NOT NULL,
    category        VARCHAR(100) NOT NULL,
    description     TEXT NOT NULL,
    budget_min      DECIMAL(12,2) NOT NULL DEFAULT 0,
    budget_max      DECIMAL(12,2) NOT NULL DEFAULT 0,
    experience_level ENUM('entry','intermediate','expert') NOT NULL DEFAULT 'intermediate',
    duration        VARCHAR(100),
    deadline        DATE,
    status          ENUM('open','hiring','in_progress','completed','closed') NOT NULL DEFAULT 'open',
    hired_freelancer_id INT UNSIGNED DEFAULT NULL,
    views           INT UNSIGNED DEFAULT 0,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (hired_freelancer_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_status   (status),
    INDEX idx_category (category),
    INDEX idx_client   (client_id)
) ENGINE=InnoDB;

-- Project ↔ Skill (many-to-many)
CREATE TABLE IF NOT EXISTS project_skills (
    project_id  INT UNSIGNED NOT NULL,
    skill_id    INT UNSIGNED NOT NULL,
    PRIMARY KEY (project_id, skill_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id)   REFERENCES skills(id)   ON DELETE CASCADE
) ENGINE=InnoDB;

-- Project attachments
CREATE TABLE IF NOT EXISTS project_files (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id      INT UNSIGNED NOT NULL,
    filename        VARCHAR(255) NOT NULL,
    original_name   VARCHAR(255) NOT NULL,
    uploaded_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Freelancer saved / bookmarked projects
CREATE TABLE IF NOT EXISTS saved_projects (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    freelancer_id   INT UNSIGNED NOT NULL,
    project_id      INT UNSIGNED NOT NULL,
    saved_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_saved (freelancer_id, project_id),
    FOREIGN KEY (freelancer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id)    REFERENCES projects(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- PROPOSALS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS proposals (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id      INT UNSIGNED NOT NULL,
    freelancer_id   INT UNSIGNED NOT NULL,
    cover_letter    TEXT NOT NULL,
    bid_amount      DECIMAL(12,2) NOT NULL,
    delivery_days   INT UNSIGNED NOT NULL,
    portfolio_links TEXT,
    status          ENUM('pending','shortlisted','accepted','rejected','withdrawn') NOT NULL DEFAULT 'pending',
    client_note     TEXT,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_proposal (project_id, freelancer_id),
    FOREIGN KEY (project_id)    REFERENCES projects(id)  ON DELETE CASCADE,
    FOREIGN KEY (freelancer_id) REFERENCES users(id)     ON DELETE CASCADE,
    INDEX idx_proposal_status (status)
) ENGINE=InnoDB;

-- Proposal attachments
CREATE TABLE IF NOT EXISTS proposal_files (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    proposal_id INT UNSIGNED NOT NULL,
    filename    VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proposal_id) REFERENCES proposals(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- MESSAGES (private chat)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sender_id   INT UNSIGNED NOT NULL,
    receiver_id INT UNSIGNED NOT NULL,
    project_id  INT UNSIGNED NOT NULL,
    content     TEXT,
    file_path   VARCHAR(500),
    file_name   VARCHAR(255),
    is_read     TINYINT(1) NOT NULL DEFAULT 0,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id)   REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id)  REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_msg_conversation (project_id, sender_id, receiver_id),
    INDEX idx_msg_read (receiver_id, is_read)
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- WORK SUBMISSIONS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS work_submissions (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id      INT UNSIGNED NOT NULL,
    freelancer_id   INT UNSIGNED NOT NULL,
    file_path       VARCHAR(500) NOT NULL,
    original_name   VARCHAR(255) NOT NULL,
    notes           TEXT,
    status          ENUM('submitted','approved','rejected','revision_requested') NOT NULL DEFAULT 'submitted',
    client_feedback TEXT,
    submitted_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewed_at     DATETIME,
    FOREIGN KEY (project_id)    REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (freelancer_id) REFERENCES users(id)    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- PAYMENTS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id                      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id              INT UNSIGNED NOT NULL,
    client_id               INT UNSIGNED NOT NULL,
    freelancer_id           INT UNSIGNED NOT NULL,
    amount                  DECIMAL(12,2) NOT NULL,
    currency                VARCHAR(10) NOT NULL DEFAULT 'INR',
    status                  ENUM('pending','completed','failed','refunded') NOT NULL DEFAULT 'pending',
    razorpay_order_id       VARCHAR(200),
    razorpay_payment_id     VARCHAR(200),
    razorpay_signature      VARCHAR(500),
    refund_id               VARCHAR(200),
    created_at              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id)    REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id)     REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (freelancer_id) REFERENCES users(id)    ON DELETE CASCADE,
    INDEX idx_payment_status (status)
) ENGINE=InnoDB;

-- Transaction log
CREATE TABLE IF NOT EXISTS transactions (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payment_id  INT UNSIGNED NOT NULL,
    type        ENUM('payment','refund','fee') NOT NULL,
    amount      DECIMAL(12,2) NOT NULL,
    note        VARCHAR(500),
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- REVIEWS & RATINGS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reviews (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    project_id  INT UNSIGNED NOT NULL,
    reviewer_id INT UNSIGNED NOT NULL,
    reviewee_id INT UNSIGNED NOT NULL,
    rating      TINYINT UNSIGNED NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment     TEXT,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_review (project_id, reviewer_id),
    FOREIGN KEY (project_id)  REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (reviewee_id) REFERENCES users(id)    ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- NOTIFICATIONS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    type        VARCHAR(50) NOT NULL,
    title       VARCHAR(255) NOT NULL,
    message     TEXT NOT NULL,
    link        VARCHAR(500),
    is_read     TINYINT(1) NOT NULL DEFAULT 0,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_notif_user_read (user_id, is_read)
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- PASSWORD RESET TOKENS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    token       VARCHAR(500) NOT NULL UNIQUE,
    expires_at  DATETIME NOT NULL,
    used        TINYINT(1) NOT NULL DEFAULT 0,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_token (token(100))
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- EMAIL VERIFICATION TOKENS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS email_verification_tokens (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL UNIQUE,
    token       VARCHAR(500) NOT NULL UNIQUE,
    expires_at  DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────────────────────
-- SEED — common skills
-- ─────────────────────────────────────────────────────────────
INSERT IGNORE INTO skills (name) VALUES
('Python'), ('JavaScript'), ('PHP'), ('Java'), ('C++'), ('C#'), ('Go'), ('Ruby'),
('HTML'), ('CSS'), ('React'), ('Angular'), ('Vue.js'), ('Node.js'), ('TypeScript'),
('MySQL'), ('PostgreSQL'), ('MongoDB'), ('Redis'), ('Docker'), ('Kubernetes'),
('AWS'), ('Azure'), ('GCP'), ('Linux'), ('Git'),
('Graphic Design'), ('UI/UX Design'), ('Figma'), ('Photoshop'), ('Illustrator'),
('Content Writing'), ('Copywriting'), ('SEO'), ('Digital Marketing'), ('Social Media'),
('Video Editing'), ('Animation'), ('3D Modeling'), ('WordPress'), ('Shopify'),
('Mobile Development'), ('iOS'), ('Android'), ('Flutter'), ('React Native'),
('Data Science'), ('Machine Learning'), ('AI'), ('Blockchain'), ('Cybersecurity');
