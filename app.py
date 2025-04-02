import time
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from gspread.exceptions import WorksheetNotFound

# 1) Set up Streamlit page config
st.set_page_config(page_title="Safebox Tasks Manager", layout="wide")

# 2) Load config from Streamlit secrets (replacing local .env)
CONFIG = {
    "USERNAME": st.secrets["general"]["APP_USERNAME"],
    "PASSWORD": st.secrets["general"]["APP_PASSWORD"],
    "GOOGLE_SHEET_ID": st.secrets["general"]["GOOGLE_SHEET_ID"],
}

# 3) Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Helper: Load Google Credentials ---
def load_google_credentials():
    try:
        creds_info = st.secrets["google_credentials"]
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        return creds
    except Exception as e:
        st.error("Error loading Google credentials from secrets. Please ensure your credentials are valid.")
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
        st.error("Could not connect to Google Sheet. Check your GOOGLE_SHEET_ID and credentials.")
        st.error(e)
        st.stop()

# --- Helper: Get or Create Worksheet for Department ---
def get_department_sheet(sheet_obj, department_name):
    try:
        return sheet_obj.worksheet(department_name)
    except WorksheetNotFound:
        # Create a new worksheet if it doesn't exist
        return sheet_obj.add_worksheet(title=department_name, rows="100", cols="26")

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
        "1. Fill in all the required fields on the page.\n"
        "2. Each action displays a 2-second spinner for processing."
    )

# 5) Standalone Page: Tasks and Accountability Form
def page_your_task():
    st.title("Your Task - Write Tasks to the Sheet")
    st.markdown("---")
    sheet_obj = connect_google_sheet()
    
    # Input fields arranged in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        name = st.text_input("Name")
    with col2:
        email = st.text_input("Email")
    with col3:
        departments = ["STARWOX", "ZUMMEY", "SAFEBOX ENERGY", "CREATIVE", "EXECUTIVE ASSISTANTS", "DEVELOPERS"]
        department = st.selectbox("Department", departments)
    with col4:
        project = st.text_input("Project")
    with col5:
        date_val = st.date_input("Date")

    st.markdown("### Tasks (1 - 6)")
    colA, colB, colC = st.columns(3)
    with colA:
        task1 = st.text_input("Task 1 (10-11am)")
        task2 = st.text_input("Task 2 (11-12pm)")
    with colB:
        task3 = st.text_input("Task 3 (12:40-2pm)")
        task4 = st.text_input("Task 4 (2-3pm)")
    with colC:
        task5 = st.text_input("Task 5 (3-4pm)")
        task6 = st.text_input("Task 6 (4-5pm)")

    if st.button("Submit Tasks"):
        with st.spinner("Submitting tasks..."):
            time.sleep(2)
        if not all([name.strip(), email.strip(), department.strip(), project.strip()]):
            st.error("Please fill in Name, Email, Department, and Project.")
        else:
            # Row format: Date, Name, Email, Department, Project, Task1, ..., Task6
            row_data = [str(date_val), name, email, department, project, task1, task2, task3, task4, task5, task6]
            try:
                # Get or create the worksheet based on the selected department
                department_sheet = get_department_sheet(sheet_obj, department)
                department_sheet.append_row(row_data)
                st.success("Tasks submitted successfully!")
            except Exception as e:
                st.error("Error appending row to the sheet.")
                st.error(e)

# 6) Render the "Your Task" page if logged in; otherwise prompt for login.
if st.session_state.logged_in:
    page_your_task()
else:
    st.warning("Please log in from the sidebar to continue.")










