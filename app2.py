# import os
# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# from dotenv import load_dotenv
# import smtplib
# from email.mime.text import MIMEText

# # --- SET PAGE CONFIG FIRST ---
# st.set_page_config(page_title="Safebox Task Supervisor App", layout="wide")

# # --- Load Configuration from .env ---
# load_dotenv()

# # For local testing, all values come from .env.
# # For production on Streamlit Cloud, you can move these to the Secrets UI.
# CONFIG = {
#     "APP2_USERNAME": os.getenv("APP2_USERNAME"),  # Do not hard-code; set in .env or secrets.
#     "APP2_PASSWORD": os.getenv("APP2_PASSWORD"),
#     "GOOGLE_SHEET_ID": os.getenv("GOOGLE_SHEET_ID", ""),
#     "SMTP_SERVER": os.getenv("SMTP_SERVER", ""),
#     "SMTP_PORT": os.getenv("SMTP_PORT", ""),
#     "SMTP_USER": os.getenv("SMTP_USER", ""),
#     "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", "")
# }

# # --- Helper: Send Email ---
# def send_email(to_address, subject, body):
#     smtp_server = CONFIG["SMTP_SERVER"]
#     smtp_port = CONFIG["SMTP_PORT"]
#     smtp_user = CONFIG["SMTP_USER"]
#     smtp_password = CONFIG["SMTP_PASSWORD"]

#     if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
#         st.warning("SMTP credentials not configured. Email will be simulated.")
#         st.write(f"Simulated email to {to_address}:\nSubject: {subject}\n\n{body}")
#         return

#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = smtp_user
#     msg["To"] = to_address

#     try:
#         with smtplib.SMTP_SSL(smtp_server, int(smtp_port)) as server:
#             server.login(smtp_user, smtp_password)
#             server.sendmail(smtp_user, [to_address], msg.as_string())
#         st.success(f"Email sent to {to_address} successfully.")
#     except Exception as e:
#         st.error(f"Error sending email: {e}")

# # --- Session State Initialization ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "form_submitted" not in st.session_state:
#     st.session_state.form_submitted = False

# # --- SIDEBAR: Login and Guidelines ---
# with st.sidebar:
#     st.header("Login")
#     if not st.session_state.logged_in:
#         # Username and password are loaded from .env (or secrets)
#         user_input = st.text_input("Username")
#         pass_input = st.text_input("Password", type="password")
#         if st.button("Login"):
#             if user_input.strip() == (CONFIG["APP2_USERNAME"] or "").strip() and pass_input.strip() == (CONFIG["APP2_PASSWORD"] or "").strip():
#                 st.session_state.logged_in = True
#                 st.success("Logged in!")
#             else:
#                 st.error("Invalid credentials.")
#     else:
#         st.info("Logged in successfully.")

#     st.markdown("---")
#     st.subheader("Guidelines")
#     st.info("1. Enter your Name, Email, and Date below.\n"
#             "2. Click 'Fetch Tasks' to retrieve tasks from the Google Sheet.\n"
#             "3. Review the tasks, add your supervisor comment, and click 'Send Comments' to email your comment.")

# # --- MAIN PAGE CONTENT (One-Page Functionality) ---
# if st.session_state.logged_in:
#     st.title("Safebox Task Supervisor App")

#     # Landing form: side-by-side inputs for Name, Email, Date
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         name = st.text_input("Name (case-insensitive)")
#     with col2:
#         email = st.text_input("Email Address")
#     with col3:
#         date_val = st.date_input("Date")

#     # Fetch Tasks button (highly responsive, no artificial delay)
#     if st.button("Fetch Tasks"):
#         if not name.strip() or not email.strip():
#             st.error("Please enter both Name and Email.")
#         else:
#             # Save the landing values in session state
#             st.session_state.landing_name = name.strip()
#             st.session_state.landing_email = email.strip()
#             st.session_state.landing_date = str(date_val)
#             st.session_state.form_submitted = True  # Mark that the form has been submitted

#     # If the form has been submitted, fetch tasks and display the supervisor comment box
#     if st.session_state.get("form_submitted", False):
#         st.subheader("Fetched Tasks")
#         # Load Google Sheets credentials from a local file for offline testing.
#         try:
#             credentials = Credentials.from_service_account_file(
#                 "credentials.json",
#                 scopes=["https://www.googleapis.com/auth/spreadsheets"]
#             )
#         except Exception as e:
#             st.error("Error loading credentials from 'credentials.json'.")
#             st.error(e)
#             st.stop()

#         try:
#             client = gspread.authorize(credentials)
#             sheet = client.open_by_key(CONFIG["GOOGLE_SHEET_ID"]).sheet1
#         except Exception as e:
#             st.error("Error connecting to Google Sheets. Check your GOOGLE_SHEET_ID and credentials.")
#             st.error(e)
#             st.stop()

#         landing_name = st.session_state.landing_name
#         landing_date = st.session_state.landing_date

#         matched_row = None
#         try:
#             rows = sheet.get_all_values()
#             for row in rows[1:]:
#                 if len(row) >= 2:
#                     if row[0].strip() == landing_date and row[1].strip().lower() == landing_name.lower():
#                         matched_row = row
#                         break
#         except Exception as e:
#             st.error("Error fetching data from the sheet.")
#             st.error(e)

#         if matched_row:
#             st.success("Tasks found:")
#             tasks = matched_row[3:9]  # Assume tasks are in columns 4 to 9
#             colA, colB, colC = st.columns(3)
#             with colA:
#                 st.write(f"**Task 1:** {tasks[0] if len(tasks)>0 else ''}")
#                 st.write(f"**Task 4:** {tasks[3] if len(tasks)>3 else ''}")
#             with colB:
#                 st.write(f"**Task 2:** {tasks[1] if len(tasks)>1 else ''}")
#                 st.write(f"**Task 5:** {tasks[4] if len(tasks)>4 else ''}")
#             with colC:
#                 st.write(f"**Task 3:** {tasks[2] if len(tasks)>2 else ''}")
#                 st.write(f"**Task 6:** {tasks[5] if len(tasks)>5 else ''}")
#         else:
#             st.warning("No matching tasks found for the given Name and Date.")

#         st.markdown("---")
#         # Supervisor Comment box and Send button
#         comment = st.text_area("Enter Supervisor Comment")
#         if st.button("Send Comments"):
#             if not comment.strip():
#                 st.error("Please enter a comment before sending.")
#             else:
#                 subject = f"Supervisor Comment for {landing_name} on {landing_date}"
#                 body = f"Supervisor's Comment:\n\n{comment}"
#                 send_email(st.session_state.landing_email, subject, body)
# else:
#     st.warning("Please log in from the sidebar to continue.")
import json
import time
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from gspread.exceptions import WorksheetNotFound

# 1) Set up Streamlit page config first
st.set_page_config(page_title="Safebox Tasks Manager", layout="wide")

# 2) Load Secrets from Streamlit Cloud
CONFIG = {
    "USERNAME": st.secrets["APP_USERNAME"],
    "PASSWORD": st.secrets["APP_PASSWORD"],
    "GOOGLE_SHEET_ID": st.secrets["GOOGLE_SHEET_ID"],
    "SMTP_SERVER": st.secrets["SMTP_SERVER"],
    "SMTP_PORT": st.secrets["SMTP_PORT"],
    "SMTP_USER": st.secrets["SMTP_USER"],
    "SMTP_PASSWORD": st.secrets["SMTP_PASSWORD"]
}

# 3) Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "landing"  # Options: landing, your_task, edit_team, schedule_monthly

# --- Helper: Safe Rerun ---
def safe_rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.stop()

# --- Helper: Load Google Credentials ---
def load_google_credentials():
    try:
        google_creds = json.loads(st.secrets["google_credentials"])
        creds = Credentials.from_service_account_info(
            google_creds, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        return creds
    except Exception as e:
        st.error("Error loading Google credentials from Streamlit secrets.")
        st.error(e)
        st.stop()

# --- Helper: Connect to Google Sheet ---
def connect_google_sheet():
    creds = load_google_credentials()
    try:
        client = gspread.authorize(creds)
        sheet = client.open_by_key(CONFIG["GOOGLE_SHEET_ID"])
        return sheet
    except Exception as e:
        st.error("Could not connect to Google Sheet. Check your GOOGLE_SHEET_ID.")
        st.error(e)
        st.stop()

# --- Helper: Get or Create Monthly Sheet ---
def get_or_create_monthly_sheet(sheet_obj):
    try:
        monthly_sheet = sheet_obj.worksheet("MonthlyPlan")
    except WorksheetNotFound:
        monthly_sheet = sheet_obj.add_worksheet(title="MonthlyPlan", rows="100", cols="26")
    return monthly_sheet

# 4) Sidebar: Login & Guidelines
with st.sidebar:
    st.header("Login")
    if not st.session_state.logged_in:
        user_in = st.text_input("Username")
        pass_in = st.text_input("Password", type="password")
        if st.button("Login"):
            if user_in.strip() == CONFIG["USERNAME"].strip() and pass_in.strip() == CONFIG["PASSWORD"].strip():
                st.session_state.logged_in = True
                st.success("Logged in!")
            else:
                st.error("Invalid username or password.")
    else:
        st.info("You are logged in.")
    st.markdown("---")
    st.subheader("Guidelines")
    st.info(
        "1. Use the buttons on the landing page to select your action.\n"
        "2. Each page has a back arrow to return to the landing page.\n"
        "3. All buttons display a 2-second spinner."
    )

# --- (Rest of the script remains unchanged) ---
