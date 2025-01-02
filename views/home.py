import streamlit as st
from views.shared_data import get_page_data

def app():
    st.title("Here is an overview of your financial data:")

    # Fetch shared data
    data = get_page_data()

    # Display data from each page
    st.subheader("Cashflow Overview")
    st.write(f"Total Inflows: ${data['Cashflow']['Total Inflows']}")
    st.write(f"Total Outflows: ${data['Cashflow']['Total Outflows']}")
    st.write(f"Net Gain/Loss: ${data['Cashflow']['Net Gain/Loss']}")


    st.subheader("Portfolio Overview")
    st.write(f"Portfolio Value: ${data['Portfolio']['value']}")
    st.write(f"Portfolio Returns: {data['Portfolio']['returns']}%")

    st.subheader("Networth Overview")
    st.write(f"Assets: ${data['Networth']['assets']}")
    st.write(f"Liabilities: ${data['Networth']['liabilities']}")

# Ensure the app function is executed when the script is run directly
if __name__ == "__main__":
    app()



# Dynamic loader for each page

# import streamlit as st
# import os
# import importlib

# # Get all page files from the "pages" directory
# page_files = [f for f in os.listdir("pages") if f.endswith(".py")]

# # Sidebar navigation
# page_names = [f.replace(".py", "").replace("_", " ") for f in page_files]
# selected_page = st.sidebar.selectbox("Select a Page", page_names)

# # Dynamically import and run the selected page
# page_index = page_names.index(selected_page)
# module_name = f"pages.{page_files[page_index].replace('.py', '')}"
# page_module = importlib.import_module(module_name)
# page_module.app()