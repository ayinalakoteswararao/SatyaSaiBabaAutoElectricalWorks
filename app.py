"""
Satya Sai Baba Auto Electrical Works - Main Flask Application
============================================================
A full-stack web application for an auto electrical shop.
"""

import os
import json
import threading
from datetime import datetime, date, timedelta
from functools import wraps

from flask import (Flask, render_template, request, jsonify, redirect,
                   url_for, session, flash)
from flask.json.provider import DefaultJSONProvider
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import MySQLdb.cursors

# Custom JSON Provider to handle timedelta and other non-serializable types
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, timedelta):
            # Convert timedelta to HH:MM:SS string
            total_seconds = int(obj.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# Load environment variables from .env file
load_dotenv()

# ─── App Setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'satya-sai-secret-key-2024-auto-electrical')
app.json = CustomJSONProvider(app)

# ─── MySQL Config ─────────────────────────────────────────────────────────────
app.config['MYSQL_HOST']     = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_PORT']     = int(os.environ.get('MYSQL_PORT', 3306))
app.config['MYSQL_USER']     = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB']       = os.environ.get('MYSQL_DB', 'satya_sai_auto')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql   = MySQL(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ─── Helpers ──────────────────────────────────────────────────────────────────
def get_cursor():
    return mysql.connection.cursor()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please login to access admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

def log_inventory_change(item_type, item_id, action, qty_change, qty_before, qty_after, notes=''):
    try:
        cur = get_cursor()
        cur.execute("""INSERT INTO inventory_log
                       (item_type,item_id,action,quantity_change,quantity_before,quantity_after,notes)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (item_type, item_id, action, qty_change, qty_before, qty_after, notes))
        mysql.connection.commit()
        # Emit real-time update
        socketio.emit('inventory_update', {
            'item_type': item_type,
            'item_id': item_id,
            'quantity_after': qty_after,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Inventory log error: {e}")

# ─── PUBLIC ROUTES ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    cur = get_cursor()
    cur.execute("SELECT * FROM services WHERE is_active=1 LIMIT 6")
    services = cur.fetchall()
    cur.execute("SELECT * FROM brands WHERE is_active=1")
    brands = cur.fetchall()
    cur.execute("SELECT COUNT(*) as cnt FROM products WHERE is_active=1")
    product_count = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM bookings WHERE status='completed'")
    completed_jobs = cur.fetchone()['cnt']
    return render_template('index.html', services=services, brands=brands,
                           product_count=product_count, completed_jobs=completed_jobs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    cur = get_cursor()
    cur.execute("SELECT * FROM services WHERE is_active=1")
    services = cur.fetchall()
    return render_template('services.html', services=services)

@app.route('/products')
def products():
    cur = get_cursor()
    brand_id = request.args.get('brand')
    vehicle_type = request.args.get('vehicle')
    category_id = request.args.get('category')
    search = request.args.get('q', '')

    query = """SELECT p.*, b.name as brand_name, c.name as category_name
               FROM products p
               LEFT JOIN brands b ON p.brand_id = b.id
               LEFT JOIN categories c ON p.category_id = c.id
               WHERE p.is_active=1"""
    params = []

    if brand_id:
        query += " AND p.brand_id=%s"; params.append(brand_id)
    if vehicle_type:
        query += " AND (p.vehicle_type=%s OR p.vehicle_type='universal')"; params.append(vehicle_type)
    if category_id:
        query += " AND p.category_id=%s"; params.append(category_id)
    if search:
        query += " AND (p.name LIKE %s OR p.part_number LIKE %s OR p.description LIKE %s)"
        params += [f'%{search}%', f'%{search}%', f'%{search}%']

    query += " ORDER BY p.name"
    cur.execute(query, params)
    products = cur.fetchall()

    cur.execute("SELECT * FROM brands WHERE is_active=1")
    brands = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    return render_template('products.html', products=products, brands=brands,
                           categories=categories, filters={'brand': brand_id,
                           'vehicle': vehicle_type, 'category': category_id, 'q': search})

@app.route('/batteries')
def batteries():
    cur = get_cursor()
    vehicle_type = request.args.get('vehicle')
    brand = request.args.get('brand')

    query = "SELECT * FROM batteries WHERE is_active=1"
    params = []
    if vehicle_type:
        query += " AND vehicle_type=%s"; params.append(vehicle_type)
    if brand:
        query += " AND brand=%s"; params.append(brand)
    query += " ORDER BY brand, price"
    cur.execute(query, params)
    batteries = cur.fetchall()

    cur.execute("SELECT DISTINCT brand FROM batteries WHERE is_active=1")
    battery_brands = [r['brand'] for r in cur.fetchall()]

    return render_template('batteries.html', batteries=batteries,
                           battery_brands=battery_brands,
                           filters={'vehicle': vehicle_type, 'brand': brand})

@app.route('/inverters')
def inverters():
    return render_template('inverters.html')

@app.route('/brands')
def brands():
    cur = get_cursor()
    cur.execute("SELECT * FROM brands WHERE is_active=1")
    brands = cur.fetchall()
    return render_template('brands.html', brands=brands)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        try:
            cur = get_cursor()
            # Save or find customer
            cur.execute("SELECT id FROM customers WHERE phone=%s", (request.form['phone'],))
            customer = cur.fetchone()
            if not customer:
                cur.execute("""INSERT INTO customers (name,phone,email,vehicle_type,vehicle_number)
                               VALUES (%s,%s,%s,%s,%s)""",
                            (request.form['name'], request.form['phone'],
                             request.form.get('email',''),
                             request.form['vehicle_type'], request.form.get('vehicle_number','')))
                mysql.connection.commit()
                customer_id = cur.lastrowid
            else:
                customer_id = customer['id']

            cur.execute("""INSERT INTO bookings
                           (customer_id,service_id,booking_date,booking_time,vehicle_type,
                            vehicle_number,vehicle_make,vehicle_model,problem_description)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (customer_id, request.form.get('service_id') or None,
                         request.form['booking_date'], request.form.get('booking_time',''),
                         request.form['vehicle_type'], request.form.get('vehicle_number',''),
                         request.form.get('vehicle_make',''), request.form.get('vehicle_model',''),
                         request.form.get('problem_description','')))
            mysql.connection.commit()
            booking_id = cur.lastrowid

            # Emit real-time notification to admin
            socketio.emit('new_booking', {
                'booking_id': booking_id,
                'customer': request.form['name'],
                'service': request.form.get('service_name',''),
                'date': request.form['booking_date'],
                'timestamp': datetime.now().isoformat()
            }, room='admin')

            flash('Booking confirmed! We will contact you shortly.', 'success')
            return redirect(url_for('booking_success', booking_id=booking_id))
        except Exception as e:
            print(f"Booking error: {e}")
            flash('Booking failed. Please try again or call us directly.', 'error')

    cur = get_cursor()
    cur.execute("SELECT * FROM services WHERE is_active=1")
    services = cur.fetchall()
    return render_template('booking.html', services=services)

@app.route('/booking/success/<int:booking_id>')
def booking_success(booking_id):
    cur = get_cursor()
    cur.execute("""SELECT b.*, c.name as customer_name, c.phone, s.name as service_name
                   FROM bookings b
                   LEFT JOIN customers c ON b.customer_id=c.id
                   LEFT JOIN services s ON b.service_id=s.id
                   WHERE b.id=%s""", (booking_id,))
    booking = cur.fetchone()
    return render_template('booking_success.html', booking=booking)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            cur = get_cursor()
            cur.execute("""INSERT INTO inquiries (name,phone,email,subject,message)
                           VALUES (%s,%s,%s,%s,%s)""",
                        (request.form['name'], request.form.get('phone',''),
                         request.form.get('email',''), request.form.get('subject',''),
                         request.form['message']))
            mysql.connection.commit()

            socketio.emit('new_inquiry', {
                'name': request.form['name'],
                'subject': request.form.get('subject',''),
                'timestamp': datetime.now().isoformat()
            }, room='admin')

            flash('Message sent! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            print(f"Contact error: {e}")
            flash('Failed to send message. Please call us directly.', 'error')

    return render_template('contact.html')

# ─── API Endpoints ────────────────────────────────────────────────────────────

@app.route('/api/products/search')
def api_search_products():
    q = request.args.get('q', '')
    cur = get_cursor()
    cur.execute("""SELECT p.id, p.name, p.part_number, p.price, b.name as brand_name
                   FROM products p LEFT JOIN brands b ON p.brand_id=b.id
                   WHERE p.is_active=1 AND (p.name LIKE %s OR p.part_number LIKE %s)
                   LIMIT 10""", (f'%{q}%', f'%{q}%'))
    return jsonify(cur.fetchall())

@app.route('/api/inventory/status')
def api_inventory_status():
    cur = get_cursor()
    cur.execute("SELECT id,name,stock_quantity FROM products WHERE is_active=1 AND stock_quantity<5")
    low_stock = cur.fetchall()
    cur.execute("SELECT id,brand,model,stock_quantity FROM batteries WHERE is_active=1 AND stock_quantity<3")
    low_batteries = cur.fetchall()
    return jsonify({'low_stock_products': low_stock, 'low_stock_batteries': low_batteries})

# ─── ADMIN ROUTES ─────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        cur = get_cursor()
        cur.execute("SELECT * FROM admin WHERE username=%s", (request.form['username'],))
        admin = cur.fetchone()
        if admin and check_password_hash(admin['password_hash'], request.form['password']):
            session['admin_logged_in'] = True
            session['admin_id'] = admin['id']
            session['admin_username'] = admin['username']
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials.', 'error')

    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    cur = get_cursor()
    stats = {}
    cur.execute("SELECT COUNT(*) as cnt FROM products WHERE is_active=1"); stats['products'] = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM bookings WHERE status='pending'"); stats['pending_bookings'] = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM inquiries WHERE is_read=0"); stats['unread_inquiries'] = cur.fetchone()['cnt']
    cur.execute("SELECT COUNT(*) as cnt FROM customers"); stats['customers'] = cur.fetchone()['cnt']

    cur.execute("""SELECT b.*, c.name as customer_name, c.phone, s.name as service_name
                   FROM bookings b LEFT JOIN customers c ON b.customer_id=c.id
                   LEFT JOIN services s ON b.service_id=s.id
                   ORDER BY b.created_at DESC LIMIT 10""")
    recent_bookings = cur.fetchall()

    cur.execute("SELECT * FROM inquiries ORDER BY created_at DESC LIMIT 5")
    recent_inquiries = cur.fetchall()

    cur.execute("SELECT * FROM products WHERE stock_quantity<5 AND is_active=1 LIMIT 10")
    low_stock = cur.fetchall()

    return render_template('admin/dashboard.html', stats=stats,
                           recent_bookings=recent_bookings,
                           recent_inquiries=recent_inquiries, low_stock=low_stock)

# Admin: Products
@app.route('/admin/products')
@login_required
def admin_products():
    cur = get_cursor()
    cur.execute("""SELECT p.*, b.name as brand_name, c.name as category_name
                   FROM products p LEFT JOIN brands b ON p.brand_id=b.id
                   LEFT JOIN categories c ON p.category_id=c.id
                   ORDER BY p.name""")
    products = cur.fetchall()
    cur.execute("SELECT * FROM brands WHERE is_active=1")
    brands = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    return render_template('admin/products.html', products=products, brands=brands, categories=categories)

@app.route('/admin/products/add', methods=['POST'])
@login_required
def admin_add_product():
    cur = get_cursor()
    cur.execute("""INSERT INTO products (name,brand_id,category_id,vehicle_type,part_number,
                   price,stock_quantity,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (request.form['name'], request.form.get('brand_id') or None,
                 request.form.get('category_id') or None, request.form['vehicle_type'],
                 request.form.get('part_number',''), request.form.get('price',0),
                 request.form.get('stock_quantity',0), request.form.get('description','')))
    mysql.connection.commit()
    flash('Product added successfully!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/edit/<int:pid>', methods=['POST'])
@login_required
def admin_edit_product(pid):
    cur = get_cursor()
    cur.execute("SELECT stock_quantity FROM products WHERE id=%s", (pid,))
    old = cur.fetchone()
    new_qty = int(request.form.get('stock_quantity', 0))

    cur.execute("""UPDATE products SET name=%s,brand_id=%s,category_id=%s,vehicle_type=%s,
                   part_number=%s,price=%s,stock_quantity=%s,description=%s WHERE id=%s""",
                (request.form['name'], request.form.get('brand_id') or None,
                 request.form.get('category_id') or None, request.form['vehicle_type'],
                 request.form.get('part_number',''), request.form.get('price',0),
                 new_qty, request.form.get('description',''), pid))
    mysql.connection.commit()

    if old and old['stock_quantity'] != new_qty:
        log_inventory_change('product', pid, 'set',
                             new_qty - old['stock_quantity'],
                             old['stock_quantity'], new_qty, 'Admin update')

    flash('Product updated!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/products/delete/<int:pid>', methods=['POST'])
@login_required
def admin_delete_product(pid):
    cur = get_cursor()
    cur.execute("UPDATE products SET is_active=0 WHERE id=%s", (pid,))
    mysql.connection.commit()
    flash('Product removed.', 'success')
    return redirect(url_for('admin_products'))

# Admin: Bookings
@app.route('/admin/bookings')
@login_required
def admin_bookings():
    cur = get_cursor()
    status_filter = request.args.get('status', '')
    query = """SELECT b.*, c.name as customer_name, c.phone, s.name as service_name
               FROM bookings b LEFT JOIN customers c ON b.customer_id=c.id
               LEFT JOIN services s ON b.service_id=s.id"""
    if status_filter:
        query += " WHERE b.status=%s"
        cur.execute(query + " ORDER BY b.booking_date DESC", (status_filter,))
    else:
        cur.execute(query + " ORDER BY b.booking_date DESC")
    bookings = cur.fetchall()
    return render_template('admin/bookings.html', bookings=bookings, status_filter=status_filter)

@app.route('/admin/bookings/update/<int:bid>', methods=['POST'])
@login_required
def admin_update_booking(bid):
    cur = get_cursor()
    cur.execute("UPDATE bookings SET status=%s, notes=%s WHERE id=%s",
                (request.form['status'], request.form.get('notes',''), bid))
    mysql.connection.commit()
    flash('Booking status updated!', 'success')
    return redirect(url_for('admin_bookings'))

# Admin: Batteries
@app.route('/admin/batteries')
@login_required
def admin_batteries():
    cur = get_cursor()
    cur.execute("SELECT * FROM batteries ORDER BY brand, model")
    batteries = cur.fetchall()
    return render_template('admin/batteries.html', batteries=batteries)

@app.route('/admin/batteries/add', methods=['POST'])
@login_required
def admin_add_battery():
    cur = get_cursor()
    cur.execute("""INSERT INTO batteries (brand,model,capacity_ah,voltage,vehicle_type,
                   warranty_months,price,stock_quantity,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (request.form['brand'], request.form['model'], request.form.get('capacity_ah',0),
                 request.form.get('voltage',12), request.form['vehicle_type'],
                 request.form.get('warranty_months',12), request.form.get('price',0),
                 request.form.get('stock_quantity',0), request.form.get('description','')))
    mysql.connection.commit()
    flash('Battery added!', 'success')
    return redirect(url_for('admin_batteries'))

@app.route('/admin/batteries/edit/<int:bid>', methods=['POST'])
@login_required
def admin_edit_battery(bid):
    cur = get_cursor()
    cur.execute("SELECT stock_quantity FROM batteries WHERE id=%s", (bid,))
    old = cur.fetchone()
    new_qty = int(request.form.get('stock_quantity', 0))

    cur.execute("""UPDATE batteries SET brand=%s,model=%s,capacity_ah=%s,voltage=%s,vehicle_type=%s,
                   warranty_months=%s,price=%s,stock_quantity=%s,description=%s WHERE id=%s""",
                (request.form['brand'], request.form['model'], request.form.get('capacity_ah',0),
                 request.form.get('voltage',12), request.form['vehicle_type'],
                 request.form.get('warranty_months',12), request.form.get('price',0),
                 new_qty, request.form.get('description',''), bid))
    mysql.connection.commit()

    if old and old['stock_quantity'] != new_qty:
        log_inventory_change('battery', bid, 'set',
                             new_qty - old['stock_quantity'],
                             old['stock_quantity'], new_qty, 'Admin update')

    flash('Battery updated!', 'success')
    return redirect(url_for('admin_batteries'))

# Admin: Inquiries
@app.route('/admin/inquiries')
@login_required
def admin_inquiries():
    cur = get_cursor()
    cur.execute("SELECT * FROM inquiries ORDER BY created_at DESC")
    inquiries = cur.fetchall()
    cur.execute("UPDATE inquiries SET is_read=1")
    mysql.connection.commit()
    return render_template('admin/inquiries.html', inquiries=inquiries)

# Admin: Brands
@app.route('/admin/brands')
@login_required
def admin_brands():
    cur = get_cursor()
    cur.execute("SELECT * FROM brands")
    brands = cur.fetchall()
    return render_template('admin/brands.html', brands=brands)

@app.route('/admin/brands/add', methods=['POST'])
@login_required
def admin_add_brand():
    cur = get_cursor()
    cur.execute("INSERT INTO brands (name,description) VALUES (%s,%s)",
                (request.form['name'], request.form.get('description','')))
    mysql.connection.commit()
    flash('Brand added!', 'success')
    return redirect(url_for('admin_brands'))

# ─── SocketIO Events ──────────────────────────────────────────────────────────

@socketio.on('join_admin')
def on_join_admin():
    from flask_socketio import join_room
    join_room('admin')
    emit('connected', {'msg': 'Joined admin room'})

@socketio.on('connect')
def on_connect():
    emit('connected', {'status': 'ok'})

# ─── Init DB & Default Admin ──────────────────────────────────────────────────

def init_db():
    """Create default admin if none exists."""
    try:
        with app.app_context():
            cur = get_cursor()
            cur.execute("SELECT COUNT(*) as cnt FROM admin")
            if cur.fetchone()['cnt'] == 0:
                pw_hash = generate_password_hash('admin123')
                cur.execute("INSERT INTO admin (username,password_hash,email) VALUES (%s,%s,%s)",
                            ('admin', pw_hash, 'admin@satyasai.com'))
                mysql.connection.commit()
                print("Default admin created: admin / admin123")
    except Exception as e:
        print(f"DB init note: {e}")

# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
