import sqlite3
import os

DB_PATH = "users.db"

# --------------------------------------------------------
# INIT DB AND CREATE TABLE IF NOT EXISTS
# --------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT,
            status TEXT
        )
    """)

    # Insert default admin if not exists
    c.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password, role, status) VALUES (?, ?, ?, ?)",
            ("admin", "admin123", "admin", "active")
        )

    conn.commit()
    conn.close()


# --------------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------------
def authenticate(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT username, role, status FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = c.fetchone()
    conn.close()

    if user:
        return {"username": user[0], "role": user[1], "status": user[2]}
    return None


# --------------------------------------------------------
# ADD USER
# --------------------------------------------------------
def add_user(username, password, role):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (username, password, role, status) VALUES (?, ?, ?, ?)",
            (username, password, role, "active")
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


# --------------------------------------------------------
# GET USER LIST
# --------------------------------------------------------
def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, role, status FROM users")
    rows = c.fetchall()
    conn.close()
    return rows


# --------------------------------------------------------
# BLOCK USER
# --------------------------------------------------------
def block_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET status = 'blocked' WHERE username = ?", (username,))
    conn.commit()
    conn.close()


# --------------------------------------------------------
# UNBLOCK USER
# --------------------------------------------------------
def unblock_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET status = 'active' WHERE username = ?", (username,))
    conn.commit()
    conn.close()


# --------------------------------------------------------
# RESET PASSWORD
# --------------------------------------------------------
def reset_password(username, new_pass):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE username = ?", (new_pass, username))
    conn.commit()
    conn.close()
