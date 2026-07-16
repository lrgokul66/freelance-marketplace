# 🚀 FreelanceHub — Freelance Marketplace

A production-ready **Fiverr/Upwork-style** freelance marketplace built with **Python, Flask, MySQL, and Bootstrap 5**.

---

## ✨ Features

| Module | Features |
|--------|----------|
| **Auth** | Register (Client/Freelancer), Login, Logout, Forgot/Reset Password, Delete Account |
| **Projects** | Post, Edit, Close, Public Browse with Filters, Project Detail |
| **Proposals** | Submit, Edit, Withdraw, Shortlist, Hire, Reject, Compare side-by-side |
| **Chat** | Private per-project messaging, AJAX polling, file attachments |
| **Payments** | Razorpay integration, HMAC verification, PDF invoice download |
| **Work** | Submit deliverables, Client review (Approve / Revision / Reject) |
| **Reviews** | 5-star rating + comment after project completion |
| **Notifications** | Real-time badge, mark-read, type-specific icons |
| **Profiles** | Freelancer: Bio, Skills, Portfolio, Education, Experience |
| **UI** | Light/Dark mode (localStorage), responsive, mobile-first |

---

## 🗂️ Project Structure

```
freelance_marketplace/
├── app.py                  # Application factory
├── config.py               # Config (Dev/Prod/Test)
├── database.py             # MySQL connection helper
├── requirements.txt
├── .env                    # Environment variables (do NOT commit)
├── sql/
│   └── schema.sql          # Full 3NF DB schema (22 tables)
└── app/
    ├── models/             # Data access layer
    ├── routes/             # 11 Flask blueprints
    ├── services/           # File, Email, Token services
    ├── static/
    │   ├── css/main.css
    │   ├── js/main.js
    │   └── uploads/        # User-uploaded files
    └── templates/          # Jinja2 templates
        ├── base.html
        ├── auth/
        ├── client/
        ├── freelancer/
        ├── projects/
        ├── proposals/
        ├── chat/
        ├── payment/
        ├── reviews/
        ├── notifications/
        ├── work/
        ├── main/
        └── errors/
```

---

## ⚙️ Setup

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd freelance_marketplace
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```env
SECRET_KEY=your-secret-key-here
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=freelance_marketplace

RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your_app_password
```

### 3. Create the Database

```bash
mysql -u root -p < sql/schema.sql
```

### 4. Run the App

```bash
python app.py
```

Visit **http://localhost:5000**

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key for sessions & CSRF |
| `DB_HOST` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` | MySQL credentials |
| `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` | Razorpay API keys |
| `MAIL_SERVER` / `MAIL_PORT` / `MAIL_USERNAME` / `MAIL_PASSWORD` | SMTP email settings |
| `FLASK_ENV` | `development` or `production` |

---

## 💳 Payment Flow

1. Client opens project → clicks **Make Payment**
2. Backend creates a Razorpay Order via API
3. Frontend opens Razorpay checkout modal
4. On success, HMAC signature is verified server-side
5. Payment record saved, PDF invoice available for download

---

## 🔒 Security

- Passwords hashed with **bcrypt**
- CSRF tokens via **Flask-WTF / itsdangerous** on critical forms
- Role-based access control (`@role_required` decorator)
- File uploads: extension-whitelisted, UUID-renamed
- Razorpay webhooks verified with HMAC-SHA256

---

## 📦 Requirements

```
Flask>=3.0
Flask-WTF
PyMySQL
bcrypt
Razorpay
reportlab
python-dotenv
itsdangerous
```

---

## 🧪 Test Credentials (after running schema.sql)

| Role | Email | Password |
|------|-------|----------|
| Client | client@test.com | Test@1234 |
| Freelancer | freelancer@test.com | Test@1234 |

---

## 📄 License

MIT License — free to use and modify.
