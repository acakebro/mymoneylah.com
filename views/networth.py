import streamlit as st
from views.shared_data import page_data

def app():
    st.title("Net Worth Tracker")

    # Inputs
    assets = st.number_input("Valuation of Assets", min_value=0)
    liabilities = st.number_input("Amount of Liabilities", min_value=0)

    # Save data to shared dictionary
    if st.button("Save Net Worth Data"):
        page_data["Networth"]["assets"] = assets
        page_data["Networth"]["liabilities"] = liabilities
        st.success("Cashflow data updated!")

# Ensure the app function is executed when the script is run directly
if __name__ == "__main__":
    app()
