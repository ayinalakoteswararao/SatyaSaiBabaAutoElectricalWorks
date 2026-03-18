# Satya Sai Baba Auto Electrical Works — Web Application

A full-stack Flask + MySQL web application for an auto electrical shop.

---

## Project Structure

```
satya_sai_auto/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── database/
│   └── schema.sql            # MySQL database schema + seed data
├── static/
│   ├── css/main.css          # Main stylesheet (dark automotive theme)
│   └── js/main.js            # JavaScript (SocketIO, search, animations)
└── templates/
    ├── base.html             # Base template (navbar, footer, WhatsApp)
    ├── index.html            # Home page
    ├── about.html            # About Us
    ├── products.html         # Spare Parts catalog
    ├── batteries.html        # Battery section
    ├── services.html         # Services
    ├── brands.html           # Brands
    ├── booking.html          # Service booking form
    ├── booking_success.html  # Booking confirmation
    ├── contact.html          # Contact page
    └── admin/
        ├── base.html         # Admin base template
        ├── login.html        # Admin login
        ├── dashboard.html    # Admin dashboard
        ├── products.html     # Product management
        ├── batteries.html    # Battery management
        ├── bookings.html     # Booking management
        ├── inquiries.html    # Customer inquiries
        └── brands.html       # Brand management
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install packages
pip install -r requirements.txt
```

### 2. Setup MySQL Database

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

### 3. Configure Environment

Create a `.env` file or set environment variables:

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=satya_sai_auto
export SECRET_KEY=your-secret-key-here
```

### 4. Initialize Admin User

The first time you run the app, it creates a default admin:
- **Username**: `admin`
- **Password**: `admin123`

⚠️ Change this password immediately after first login!

### 5. Run the Application

```bash
python app.py
```

Visit: http://localhost:5000

---

## Pages

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/about` | About Us |
| `/products` | Spare Parts catalog (with search & filters) |
| `/batteries` | Battery section |
| `/services` | Services |
| `/brands` | Brands |
| `/booking` | Service booking form |
| `/contact` | Contact page |
| `/admin/login` | Admin login |
| `/admin` | Admin dashboard |
| `/admin/products` | Product management |
| `/admin/batteries` | Battery management |
| `/admin/bookings` | Booking management |
| `/admin/inquiries` | Customer inquiries |
| `/admin/brands` | Brand management |

---

## Features

### Public Features
- **Live product search** with autocomplete
- **Filter by** brand, vehicle type, category
- **Battery catalog** with brand/vehicle filters
- **Service booking** with form validation
- **Contact form** with inquiry tracking
- **WhatsApp float button** for quick contact
- **Google Maps** embed
- **Mobile responsive** design

### Real-Time Features (WebSockets)
- **Live inventory updates** — stock changes reflect instantly
- **New booking notifications** — admin gets real-time alerts
- **New inquiry notifications** — instant admin notification
- **Low stock alerts** — when inventory < 3 units

### Admin Dashboard
- **Booking management** — view, filter, update status
- **Product CRUD** — add, edit, delete products
- **Battery CRUD** — manage battery inventory
- **Brand management** — add/manage brands
- **Inquiry viewer** — read customer messages
- **Low stock alerts** panel
- **Statistics** — pending bookings, unread inquiries, product count

---

## Database Tables

| Table | Purpose |
|-------|---------|
| `admin` | Admin user credentials |
| `brands` | Part brands (Bosch, Lucas TVS, etc.) |
| `categories` | Part categories |
| `products` | Spare parts inventory |
| `batteries` | Battery inventory |
| `services` | Service types offered |
| `customers` | Customer records |
| `bookings` | Service bookings |
| `inquiries` | Contact form messages |
| `inventory_log` | Stock change audit trail |

---

## Deployment (Production)

### Using Gunicorn + Nginx

```bash
# Install gunicorn
pip install gunicorn

# Run with eventlet worker (required for SocketIO)
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app

# Or with the socketio run
gunicorn --worker-class eventlet -w 1 app:socketio
```

### Nginx Config
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

### Environment Variables for Production
```bash
SECRET_KEY=<strong-random-key>
MYSQL_HOST=localhost
MYSQL_USER=satyasai_user
MYSQL_PASSWORD=<strong-password>
MYSQL_DB=satya_sai_auto
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python Flask |
| Database | MySQL |
| Real-time | Flask-SocketIO (WebSockets) |
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Fonts | Rajdhani, Exo 2, Share Tech Mono |
| Icons | Font Awesome 6 |
| Animations | AOS (Animate on Scroll) |
| Auth | Werkzeug password hashing |

---

## Design Theme

- **Colors**: Dark (#0A0A0A) + Yellow (#FFD600) automotive theme
- **Typography**: Rajdhani (headings) + Exo 2 (body) + Share Tech Mono (code/prices)
- **Style**: Industrial/Automotive — dark, bold, technical

---

## Support

For technical issues or customization, contact the developer.
For shop inquiries: +91 954256****
