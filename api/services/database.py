import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.name = os.getenv('DB_NAME', 'postgres')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASS', 'postgres')
        self.port = os.getenv('DB_PORT', '5432')
        self.connection = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.name,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print(f"✅ Successfully connected to PostgreSQL at {self.host}:{self.port}")
            return self.connection
        except Exception as e:
            print(f"❌ Failed to connect to PostgreSQL: {e}")
            return None

    def initialize_db(self):
        """Create the users table if it doesn't exist."""
        conn = self.connect()
        if not conn:
            return
        
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255)
                );
            """)
            conn.commit()
            cur.close()
            print("📦 Database initialized (users table created).")
        except Exception as e:
            print(f"❌ Failed to initialize database: {e}")
        finally:
            conn.close()

    def user_exists(self, username):
        """Check if a user exists in the database."""
        conn = self.connect()
        if not conn:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
            exists = cur.fetchone() is not None
            cur.close()
            return exists
        except Exception as e:
            print(f"❌ Error querying database: {e}")
            return False
        finally:
            conn.close()

    def add_user(self, username, email=None):
        """Add a new user to the database."""
        conn = self.connect()
        if not conn:
            return
        
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING;", (username, email))
            conn.commit()
            cur.close()
        except Exception as e:
            print(f"❌ Error adding user to database: {e}")
        finally:
            conn.close()

db_service = Database()
