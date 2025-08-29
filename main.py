import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
from app import run_app

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- Initialize session state ---
if "user" not in st.session_state:
    st.session_state["user"] = None

st.title("🔐 Supabase Auth with Streamlit")

# --- Logout ---
if st.session_state["user"]:
    st.success(f"Welcome, {st.session_state['user'].email}")
    run_app(supabase)
    if st.button("Logout"):
        st.session_state["user"] = None
        st.rerun()

else:
    tab1, tab2 = st.tabs(["Login", "Signup"])

    # ---------------- LOGIN ----------------
    with tab1:
        login_email = st.text_input("Email (login)", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            try:
                res = supabase.auth.sign_in_with_password(
                    {"email": login_email, "password": login_password}
                )
                user_id= res.user.id
                # print("User_ID:", user_id)
                st.session_state["user_id"]=user_id
                st.session_state["user"] = res.user
                # print("Logged in user:", st.session_state["user"])
                st.success("✅ Logged in successfully")
                
                st.rerun()
               
            except Exception as e:
                st.error(f"Login failed: {e}")

    # ---------------- SIGNUP ----------------
    with tab2:
        signup_email = st.text_input("Email (signup)", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Signup"):
            try:
                res = supabase.auth.sign_up(
                    {"email": signup_email, "password": signup_password}
                )
                st.success("✅ Signup successful! Check your email for confirmation.")
            except Exception as e:
                st.error(f"Signup failed: {e}")

# --- Protected Content Example ---
# if st.session_state["user"]:
#     st.write("🎉 This is protected content, only visible when logged in.")
#     run_app(supabase)
