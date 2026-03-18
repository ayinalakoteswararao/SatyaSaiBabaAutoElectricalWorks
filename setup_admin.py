"""
Run this script once to create the default admin user.
Usage: python setup_admin.py
"""
from werkzeug.security import generate_password_hash

username = 'admin'
password = 'admin123'
email = 'admin@satyasaiauto.com'

pw_hash = generate_password_hash(password)

print("="*50)
print("Satya Sai Baba Auto Electrical Works")
print("Admin Setup")
print("="*50)
print(f"\nUsername: {username}")
print(f"Password: {password}")
print(f"Hash: {pw_hash}")
print(f"\nRun this SQL in your MySQL database:")
print(f"""
USE satya_sai_auto;
UPDATE admin SET password_hash='{pw_hash}' WHERE username='admin';

-- Or insert new admin:
INSERT INTO admin (username, password_hash, email)
VALUES ('{username}', '{pw_hash}', '{email}')
ON DUPLICATE KEY UPDATE password_hash='{pw_hash}';
""")
