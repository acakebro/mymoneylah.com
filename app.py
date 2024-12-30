import streamlit as st
from auth.authentication import login, logout, signup
from views.home import app as home_app
from views.cashflow import app as cashflow_app
from views.portfolio import app as portfolio_app
from views.networth import app as networth_app
from views.financialgoals import app as financialgoals_app
from database.db import create_cashflow_table, create_portfolio_table,create_networth_table

st.set_page_config(
    page_title="MyMoneyLah",
    layout="wide",
)


# Main logic for checking if the user is logged in
def main():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        st.write(f"Welcome, {st.session_state.user['username']}!")
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Home", "Cashflow", "Portfolio", "Net Worth", "Financial Goals"])

        # Page navigation
        if page == "Home":
            home_app()
        elif page == "Cashflow":
            cashflow_app()
        elif page == "Portfolio":
            portfolio_app()
        elif page == "Net Worth":
            networth_app()
        elif page == "Financial Goals":
            financialgoals_app()
        
        st.sidebar.button("Logout", on_click=logout)
    else:
        st.write("You need to log in or register if you do not have an account first.")
        # Offer the option to log in or register
        page = st.sidebar.radio("Select a page", ["Login", "Register"])

        if page == "Login":
            login()
        else:
            signup()

if __name__ == "__main__":
    main()





