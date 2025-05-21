import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    
    # Create prices table
    cursor.execute('''CREATE TABLE IF NOT EXISTS prices (
                        id INTEGER PRIMARY KEY,
                        product_name TEXT,
                        url TEXT,
                        price REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_login DATETIME)''')
    
    # Create user_prices table for tracking which users are tracking which products
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_prices (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        price_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (price_id) REFERENCES prices (id))''')
    
    conn.commit()
    conn.close()

def create_user(username, email, password):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    
    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute('''INSERT INTO users (username, email, password)
                         VALUES (?, ?, ?)''', (username, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
        # Update last login
        cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
        conn.commit()
        return user[0]  # Return user ID
    return None

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
