#!/usr/bin/env python3
"""Reset admin password and add Valeo brand."""
import MySQLdb
from MySQLdb import cursors

# Database credentials
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASS = 'Koti@6102'
DB_NAME = 'satya_sai_auto'

# Admin credentials
ADMIN_USER = 'admin'
ADMIN_PASS_HASH = 'scrypt:32768:8:1$xtR7WnJcXmjiRdbW$cc2e219e0589ca1a187d4e5b3b33179f5cb7b45be9ea1a213b5c3a80c8a1d26d4f7afb06cc7831e811adf801415cea9e260d45fa404c717a1e49d67365fc8e2b'
ADMIN_EMAIL = 'admin@satyasaiauto.com'

def main():
    try:
        conn = MySQLdb.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=cursors.DictCursor
        )
        
        with conn.cursor() as cur:
            # Insert/Update admin
            sql = """
                INSERT INTO admin (username, password_hash, email)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE password_hash=%s
            """
            cur.execute(sql, (ADMIN_USER, ADMIN_PASS_HASH, ADMIN_EMAIL, ADMIN_PASS_HASH))
            conn.commit()
            print(f"✓ Admin user '{ADMIN_USER}' created/updated successfully!")
            print(f"  Username: {ADMIN_USER}")
            print(f"  Password: admin123")
            
            # Check admin
            cur.execute("SELECT id, username, email FROM admin WHERE username=%s", (ADMIN_USER,))
            admin = cur.fetchone()
            if admin:
                print(f"  Admin ID: {admin['id']}")
            
            # Add Valeo brand if not exists
            cur.execute("SELECT * FROM brands WHERE name='Valeo'")
            valeo = cur.fetchone()
            
            if not valeo:
                cur.execute(
                    "INSERT INTO brands (name, description, is_active) VALUES (%s, %s, %s)",
                    ('Valeo', 'French multinational automotive supplier with innovative solutions.', 1)
                )
                conn.commit()
                print("\n✓ Valeo brand added successfully!")
            else:
                print(f"\n✓ Valeo brand already exists (ID: {valeo['id']})")
            
            # List all brands
            cur.execute("SELECT id, name, is_active FROM brands WHERE is_active=1")
            brands = cur.fetchall()
            print(f"\n✓ Active brands ({len(brands)}):")
            for b in brands:
                print(f"  - {b['name']} (ID: {b['id']})")
                
        conn.close()
        print("\n✓ Done! You can now login at http://127.0.0.1:5000/admin/login")
        print("  Username: admin")
        print("  Password: admin123")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
