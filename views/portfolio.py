import streamlit as st
from views.shared_data import page_data

def app():
    st.title("Portfolio Tracker")

    # Inputs
    portfolio_value = st.number_input("Portfolio Value", min_value=0.0)
    portfolio_returns = st.number_input("Portfolio Returns (%)", min_value=0.0)

    # Save data to shared dictionary
    if st.button("Save Portfolio Data"):
        page_data["Portfolio"]["value"] = portfolio_value
        page_data["Portfolio"]["returns"] = portfolio_returns
        st.success("Portfolio data updated!")

# Ensure the app function is executed when the script is run directly
if __name__ == "__main__":
    app()
