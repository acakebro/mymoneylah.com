import streamlit as st
from database.db import insert_cashflow_data, get_cashflow_data, delete_cashflow_entry
import datetime
import pandas as pd

def app():
    st.title("Cashflow Tracker")

    # Input fields for cashflow
    date = st.date_input("Date", datetime.date.today())
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    description = st.text_input("Description")

    # Dropdown for cashflow type
    cashflow_type = st.radio("Transaction Type", ("Inflow", "Outflow"))

    # Submit data
    if st.button("Submit"):
        if date and amount and description and cashflow_type:
            # Assuming user ID is stored in session state after login
            user_id = st.session_state["user"]["id"]
            # Insert cashflow data into the database with type (inflow or outflow)
            insert_cashflow_data(user_id, date, amount, description, cashflow_type)
            st.success(f"{cashflow_type} added successfully!")
            st.rerun() # Trigger a refresh to show the newly addd data 
        else:
            st.error("Please fill out all fields.")
    
    # Filters Section: Allow user to filter by date range, transaction type, and number of records
    st.subheader("Filter Your Cashflow Data")

    # Date range filter
    start_date, end_date = st.date_input("Select date range", [datetime.date(2023, 1, 1), datetime.date.today()])
    
    # Transaction type filter
    transaction_type_filter = st.selectbox("Filter by Transaction Type", ["All", "Inflow", "Outflow"])

    # Number of records to display
    num_entries = st.slider("Number of entries to display", min_value=1, max_value=50, step=1, value=20)

    # Get filtered cashflow data
    user_id = st.session_state["user"]["id"]
    cashflow_data = get_cashflow_data(user_id, start_date, end_date, transaction_type_filter, num_entries)

    # Display the filtered cashflow data
    # if cashflow_data:
    #     # Convert data to pandas DataFrame
    #     df = pd.DataFrame(cashflow_data, columns=["ID", "User ID", "Date", "Amount", "Description", "Type"])
        
    #     # Display as an interactive table
    #     st.dataframe(df)  # Use st.table(df) for static table
    if cashflow_data:
        st.subheader("Your Recent Cashflow Data")
        
        # Convert data to pandas DataFrame
        df = pd.DataFrame(cashflow_data, columns=["ID", "User ID", "Date", "Amount", "Description", "Type"])
        # Add Delete Buttons to Each Row
        for index, row in df.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{row['Description']}**: ${row['Amount']} on {row['Date']} ({row['Type']})")
            with col2:
                if st.button(f"Delete", key=f"delete_{row['ID']}"):
                    # Call delete function to remove entry from database
                    delete_cashflow_entry(row["ID"])
                    st.success("Entry deleted successfully!")
                    st.rerun()  # Refresh the page to show updated table        
        # Calculate net output (gain/loss)
        inflow_sum = df[df["Type"] == "Inflow"]["Amount"].sum()
        outflow_sum = df[df["Type"] == "Outflow"]["Amount"].sum()
        net_output = inflow_sum - outflow_sum
        
        # Display summary
        st.metric(label="Total Inflows", value=f"${inflow_sum:,.2f}")
        st.metric(label="Total Outflows", value=f"${outflow_sum:,.2f}")
        st.metric(label="Net Gain/Loss", value=f"${net_output:,.2f}")
        
        # Display as an interactive table
        st.dataframe(df)  # Use st.table(df) for static table
    else:
        st.write("No cashflow data available matching the filters.")
