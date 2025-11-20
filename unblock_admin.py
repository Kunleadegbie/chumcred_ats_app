import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("UPDATE users SET status = 'active' WHERE username = 'admin'")
conn.commit()
conn.close()

print("Admin unblocked successfully!")
