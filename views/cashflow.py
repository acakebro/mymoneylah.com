import streamlit as st
from database.db import insert_cashflow_data, get_cashflow_data, delete_cashflow_entry, get_last_cashflow_update_entry
import datetime
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

def app():
    st.title("Cashflow Tracker")

    # Initialize a session state flag for success message
    if "success_message" not in st.session_state:
        st.session_state.success_message = None

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
            # Set success message in session state
            st.session_state.success_message = f"{cashflow_type} added successfully! ✅"
            # Refresh the page to show updated data
            st.rerun() # Trigger a refresh to show the newly add data 
        else:
            st.error("Please fill out all fields.")
    
    # Display the success message if available
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        # Clear the message after displaying it
        st.session_state.success_message = None

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

    # Fetch last update timestamp
    last_update = get_last_cashflow_update_entry(user_id)

    if last_update:
        st.info(f"Last Updated: {last_update[0]}")
        # st.info(f"Last Updated: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.info("No entries found.")

    if cashflow_data:
        st.subheader("Your Recent Cashflow Data")

        # Convert data to pandas DataFrame
        df = pd.DataFrame(cashflow_data, columns=["ID", "User ID", "Date", "Amount", "Description", "Type"])

        # Remove default index by resetting it
        df = df.reset_index(drop=True)

        # # Add Delete Buttons to Each Row
        # for index, row in df.iterrows():
        #     col1, col2 = st.columns([3, 1])
        #     with col1:
        #         st.write(f"**{row['Description']}**: ${row['Amount']} on {row['Date']} ({row['Type']})")
        #     with col2:
        #         if st.button(f"Delete", key=f"delete_{row['ID']}"):
        #             # Call delete function to remove entry from database
        #             delete_cashflow_entry(row["ID"])
        #             st.success("Entry deleted successfully!")
        #             st.rerun()  # Refresh the page to show updated table        
        # Calculate net output (gain/loss)
        inflow_sum = df[df["Type"] == "Inflow"]["Amount"].sum()
        outflow_sum = df[df["Type"] == "Outflow"]["Amount"].sum()
        net_output = inflow_sum - outflow_sum
        
        # Display summary
        st.metric(label="Total Inflows", value=f"${inflow_sum:,.2f}")
        st.metric(label="Total Outflows", value=f"${outflow_sum:,.2f}")
        st.metric(label="Net Gain/Loss", value=f"${net_output:,.2f}")
        

        # # Display as an interactive table
        # st.dataframe(df)  # Use st.table(df) for static table


        # Configure AgGrid to display the data without the default index
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
        gb.configure_selection("single")  # Allow selecting a single row
        gb.configure_default_column(
            flex = 1, # make all columns share equal space
            cellStyle = {"textAlign": "center"}, # Center-align all columns
            wrapText = True, # Optional: Wrap text in cells if needed
            # headerStyle={"textAlign": "center"} # Center-align the column headers
        )

        gb.configure_column("ID", hide=True)  # Optionally hide the ID column
        gb.configure_column("User ID", hide=True)  # Optionally hide User ID
        grid_options = gb.build()
        
        # Display the table using AgGrid
        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            height=400,
            update_mode="MODEL_CHANGED",
            fit_columns_on_grid_load=True,
        )

        # # Handle row selection and deletion
        # selected_row = grid_response.get("selected_rows",[])
        # print(len(selected_row))
        # if len(selected_row) > 0:
        #     print("selected")
        #     selected_id = selected_row[0]["ID"]
        #     if st.button("Delete Selected Entry"):
        #         delete_cashflow_entry(selected_id)
        #         st.success("Entry deleted successfully!")
        #         st.rerun()  # Refresh the page to show updated table
        # else:
        #     st.write("No row was selected")
    else:
        st.write("No cashflow data available matching the filters.")
