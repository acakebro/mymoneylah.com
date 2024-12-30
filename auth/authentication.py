import streamlit as st
from database.db import get_user, register_user, create_user_table

# Ensure the table is created when the app runs
create_user_table()

# create functions
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = get_user(username, password)
        if user:
            st.session_state.logged_in = True  # Set logged-in status to True
            # st.session_state["user"] = user
            st.session_state.user = user
            st.success("Logged in successfully!")
            st.rerun()  # Refresh the page to update session state
        else:
            st.error("Invalid credentials")

def signup():
    st.title("Sign Up")
    username = st.text_input("Type Your Username")
    password = st.text_input("Create Your Password", type="password")
    if st.button("Sign Up"):
        if username and password:
            register_user(username, password)
        else:
            st.error("Please fill out both fields.")

    pass

def logout():
    st.session_state.logged_in = False
    # st.session_state["user"] = None # username remove from session state
    st.session_state.user = None
    # st.rerun()  # Refresh the page to update session state
    st.success("Logged out successfully!")
