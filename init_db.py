"""
Database initialization script
Run once to create all tables and seed initial data
"""
import os
import MySQLdb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DB = os.environ.get('MYSQL_DB', 'satya_sai_auto')

print("=" * 60)
print("Satya Sai Baba Auto Electrical Works - Database Setup")
print("=" * 60)
print(f"\nConnecting to MySQL at {MYSQL_HOST}:{MYSQL_PORT}...")

try:
    # Connect to MySQL (without specifying database first)
    connection = MySQLdb.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWORD
    )
    
    cursor = connection.cursor()
    print("✓ Connected to MySQL")
    
    # Read and execute schema
    with open('database/schema.sql', 'r') as f:
        schema = f.read()
    
    # Execute schema statements
    print("\nExecuting schema...")
    for statement in schema.split(';'):
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"Warning: {e}")
    
    connection.commit()
    print("✓ Database schema created successfully")
    
    # Close connection
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 60)
    print("Database initialization complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run: python setup_admin.py")
    print("2. Add some seed data via admin panel")
    print("3. Start the app: python app.py")
    
except MySQLdb.Error as e:
    print(f"✗ MySQL Error: {e}")
    print("\nTroubleshooting:")
    print("1. Verify MySQL is running")
    print("2. Check credentials in .env file")
    print("3. Ensure the database user has CREATE privileges")
except FileNotFoundError:
    print("✗ Error: database/schema.sql not found")
except Exception as e:
    print(f"✗ Error: {e}")
