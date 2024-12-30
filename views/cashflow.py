import streamlit as st
from views.shared_data import page_data

def app():
    st.title("Cashflow Tracker")

    # Inputs
    income = st.number_input("Monthly Income", min_value=0)
    expenses = st.number_input("Monthly Expenses", min_value=0)

    # Save data to shared dictionary
    if st.button("Save Cashflow Data"):
        page_data["Cashflow"]["income"] = income
        page_data["Cashflow"]["expenses"] = expenses
        st.success("Cashflow data updated!")

# Ensure the app function is executed when the script is run directly
if __name__ == "__main__":
    app()
