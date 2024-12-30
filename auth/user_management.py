from database.db import create_connection

def update_password(username, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    conn.commit()
    conn.close()

def delete_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

# not used in anywhere yet