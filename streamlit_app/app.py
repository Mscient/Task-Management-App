import streamlit as st

st.set_page_config(page_title="Task Management App", layout="wide")

def main():
    st.title("Task Management System")
    st.write("Welcome to the Task Management App powered by FastAPI and Streamlit.")
    
    if "token" not in st.session_state:
        st.session_state["token"] = None
        
    if st.session_state["token"]:
        st.success("You are currently logged in! Head over to the Dashboard to manage your tasks.")
        if st.button("Logout"):
            st.session_state["token"] = None
            st.rerun()
    else:
        st.info("Please login from the 'Login' page to access your tasks.")

if __name__ == "__main__":
    main()
