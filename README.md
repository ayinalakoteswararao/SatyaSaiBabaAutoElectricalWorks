<div align="center">
  <h1>⚡ Satya Sai Baba Auto Electrical Works ⚡</h1>
  <p><strong>A full-stack web application designed for an auto electrical shop. Features inventory management, real-time alerts, service bookings, and an interactive customer portal.</strong></p>
</div>

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | 🐍 Python Flask |
| **Database** | 🗄️ MySQL |
| **Real-time** | 🔌 Flask-SocketIO (WebSockets) |
| **Frontend** | 🌐 HTML5, 🎨 CSS3, 👢 Bootstrap 5 |
| **Fonts** | 🔤 Rajdhani, Exo 2, Share Tech Mono |
| **Icons** | 🌟 Font Awesome 6 |
| **Animations** | ✨ AOS (Animate on Scroll) |
| **Auth** | 🔐 Werkzeug password hashing |

---

## ✨ Key Features

### 🌍 Public Features
- 🔍 **Live product search** with autocomplete
- 🎯 **Advanced filters** by brand, vehicle type, and category
- 🔋 **Battery catalog** with brand/vehicle filters
- 📅 **Service booking** with form validation
- ✉️ **Contact form** with inquiry tracking
- 💬 **WhatsApp float button** for quick contact
- 🗺️ **Google Maps** embed
- 📱 **Mobile responsive** design

### ⚡ Real-Time Features (WebSockets)
- 📦 **Live inventory updates** — stock changes reflect instantly
- 🔔 **New booking notifications** — admin gets real-time alerts
- 📩 **New inquiry notifications** — instant admin notification
- ⚠️ **Low stock alerts** — triggers when inventory < 3 units

### 🛡️ Admin Dashboard
- 📋 **Booking management** — view, filter, update status
- 🛒 **Product CRUD** — add, edit, delete products
- 🔋 **Battery CRUD** — manage battery inventory
- 🏷️ **Brand management** — add/manage brands
- 📥 **Inquiry viewer** — read customer messages
- 📊 **Statistics panel** — pending bookings, unread inquiries, product count

---

## 📂 Project Structure

```text
satya_sai_auto/
├── 📄 app.py                    # Main Flask application
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example              # Environment variable template
├── 📁 database/
│   └── 📄 schema.sql            # MySQL database schema + seed data
├── 📁 static/
│   ├── 📁 css/main.css          # Main stylesheet (dark automotive theme)
│   └── 📁 js/main.js            # JavaScript (SocketIO, search, animations)
└── 📁 templates/
    ├── 📄 base.html             # Base template (navbar, footer, WhatsApp)
    ├── 📄 index.html            # Home page
    ├── 📄 about.html            # About Us
    ├── 📄 products.html         # Spare Parts catalog
    ├── 📄 batteries.html        # Battery section
    ├── 📄 services.html         # Services
    ├── 📄 brands.html           # Brands
    ├── 📄 booking.html          # Service booking form
    ├── 📄 contact.html          # Contact page
    └── 📁 admin/
        ├── 📄 dashboard.html    # Admin dashboard
        └── ...                  # Other admin templates
```

---

## 🚀 Setup Instructions

### 1️⃣ Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Setup MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Run schema
source database/schema.sql
```
Or import directly:
```bash
mysql -u root -p < database/schema.sql
```

### 3️⃣ Configure Environment

Create a `.env` file or set environment variables:

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=satya_sai_auto
export SECRET_KEY=your-secret-key-here
```

### 4️⃣ Initialize Admin User

The first time you run the app, it creates a default admin:
- 👤 **Username**: `admin`
- 🔑 **Password**: `admin123`

> ⚠️ **IMPORTANT**: Change this password immediately after first login!

### 5️⃣ Run the Application

```bash
python app.py
```
🌐 Visit: [http://localhost:5000](http://localhost:5000)

---

## 🗺️ Pages Overview

| URL | Description |
|-----|-------------|
| 🏠 `/` | Home page |
| ℹ️ `/about` | About Us |
| ⚙️ `/products` | Spare Parts catalog (with search & filters) |
| 🔋 `/batteries` | Battery section |
| 🛠️ `/services` | Services |
| 🏷️ `/brands` | Brands |
| 📅 `/booking` | Service booking form |
| 📞 `/contact` | Contact page |
| 🛡️ `/admin` | Admin dashboard & management panels |

---

## 🗄️ Database Tables

| Table | Purpose |
|-------|---------|
| 👑 `admin` | Admin user credentials |
| 🏷️ `brands` | Part brands (Bosch, Lucas TVS, etc.) |
| 🗂️ `categories` | Part categories |
| 📦 `products` | Spare parts inventory |
| 🔋 `batteries` | Battery inventory |
| 🛠️ `services` | Service types offered |
| 👥 `customers` | Customer records |
| 📅 `bookings` | Service bookings |
| 📩 `inquiries` | Contact form messages |
| 📜 `inventory_log` | Stock change audit trail |

---

## 🌐 Deployment (Production)

### Using Gunicorn + Nginx

```bash
# Install gunicorn
pip install gunicorn

# Run with eventlet worker (required for SocketIO)
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app
```

### Nginx Config Example
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🎨 Design Theme
- 🎨 **Colors**: Dark (`#0A0A0A`) + Yellow (`#FFD600`) automotive theme
- 🔤 **Typography**: Rajdhani (headings), Exo 2 (body), Share Tech Mono (code/prices)
- ⚙️ **Style**: Industrial/Automotive — dark, bold, technical

---

## 📞 Support
- 🛠️ For technical issues or customization, contact the developer.
- 📞 For shop inquiries: `+91 954256****`
