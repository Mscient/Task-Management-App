import streamlit as st
import api
import json

st.set_page_config(page_title="Login/Register", layout="centered")

def render():
    st.title("Login or Register")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to your account")
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                if login_username and login_password:
                    res = api.login_user(login_username, login_password)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state["token"] = data.get("token")
                        st.success("Login successful! Go to Dashboard.")
                    else:
                        try:
                            error_detail = res.json().get("detail", "Login failed")
                        except:
                            error_detail = "Login failed"
                        st.error(error_detail)
                else:
                    st.warning("Please provide username and password")
    
    with tab2:
        st.subheader("Create a new account")
        with st.form("register_form"):
            reg_name = st.text_input("Name")
            reg_username = st.text_input("Username")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            submit_register = st.form_submit_button("Register")
            
            if submit_register:
                if reg_name and reg_username and reg_email and reg_password:
                    res = api.register_user(reg_name, reg_username, reg_email, reg_password)
                    if res.status_code == 201:
                        st.success("Registration successful! You can now login.")
                    else:
                        try:
                            error_detail = res.json().get("detail", "Registration failed")
                        except:
                            error_detail = "Registration failed"
                        st.error(error_detail)
                else:
                    st.warning("Please fill out all fields.")

if __name__ == "__main__":
    render()
