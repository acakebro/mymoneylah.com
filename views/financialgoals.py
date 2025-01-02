import streamlit as st

def app():
    st.title("My Financial Goals")
    task = st.text_input("Financial Goal:",)
    image = st.file_uploader("Insert Image of your Goal!")
    goal_amount = st.number_input("Amount to Save:")
    date_of_completion = st.date_input("When do you want to achieve this by?")  
    amount_to_save = st.number_input("How much do you want to save?")
    frequency = st.selectbox("Frequency", ("Weekly", "Monthly","Annually"))


# Ensure the app function is executed when the script is run directly
if __name__ == "__main__":
    app()
