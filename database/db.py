import sqlite3
import streamlit as st

def create_connection():
    conn = sqlite3.connect("mymoneylah.db")
    return conn

# Function to create the database and user table
def create_user_table():
    conn = create_connection()
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')

    conn.commit()
    conn.close()


# Function to register a new user
def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        st.error("Username already exists. Please choose a different username.")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success("Registration successful! You can now log in.")

        # Automatically log in the new user
        st.session_state.logged_in = True  # Set logged-in status to True
        st.session_state.username = username  # Store the username in session_state
        # st.experimental_set_query_params(rerun=True)  # Refresh the page to update session state
        st.rerun()
    
    conn.close()

def get_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    row = cursor.fetchone() # fetches the top row
    conn.close()
    if row:
        # Map the tuple to a dictionary
        return {"id": row[0], "username": row[1], "password": row[2]}
    return None

## Create new function for each DB in other pages

# Function to create the 'cashflow' table
def create_cashflow_table():
    conn = create_connection()
    cursor = conn.cursor()

# First, drop the table if it exists
    # cursor.execute("DROP TABLE IF EXISTS cashflow")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cashflow (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        amount REAL,
        description TEXT,
        type TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

# Function to insert cashflow data
def insert_cashflow_data(user_id, date, amount, description, cashflow_type):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO cashflow (user_id, date, amount, description, type) VALUES (?, ?, ?, ?, ?)",
                   (user_id, date, amount, description, cashflow_type))

    conn.commit()
    conn.close()

# Function to get the most recent entries for cashflow
def get_cashflow_data(user_id, start_date, end_date, transaction_type, num_entries):
    conn = create_connection()
    cursor = conn.cursor()

    # Build dynamic query based on filters
    query = "SELECT * FROM cashflow WHERE user_id = ? AND date BETWEEN ? AND ?"
    params = [user_id, start_date, end_date]

    # Add transaction type filter
    if transaction_type != "All":
        query += " AND type = ?"
        params.append(transaction_type)

    # Limit the number of entries
    query += " ORDER BY date DESC LIMIT ?"
    params.append(num_entries)

    cursor.execute(query, tuple(params))
    cashflow_data = cursor.fetchall()

    conn.close()
    return cashflow_data

# Function to delete  for cashflow
def delete_cashflow_entry(entry_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cashflow WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


# Function to create the 'portfolio' table
def create_portfolio_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        asset_name TEXT,
        quantity REAL,
        price REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()

# Function to create the 'networth' table
def create_networth_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS networth (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        total_assets REAL,
        total_liabilities REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    conn.commit()
    conn.close()



