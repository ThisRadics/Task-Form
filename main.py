import json
import time
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from gspread.exceptions import WorksheetNotFound

# 1) Set up Streamlit page config first
st.set_page_config(page_title="Safebox Tasks Manager", layout="wide")

# 2) Load config from st.secrets
CONFIG = {
    "USERNAME":       st.secrets["general"]["APP_USERNAME"],
    "PASSWORD":       st.secrets["general"]["APP_PASSWORD"],
    "GOOGLE_SHEET_ID":st.secrets["general"]["GOOGLE_SHEET_ID"],
    "SMTP_SERVER":    st.secrets["smtp"]["SMTP_SERVER"],
    "SMTP_PORT":      st.secrets["smtp"]["SMTP_PORT"],
    "SMTP_USER":      st.secrets["smtp"]["SMTP_USER"],
    "SMTP_PASSWORD":  st.secrets["smtp"]["SMTP_PASSWORD"],
}

# Global spinner duration
SPINNER_TIME = 5  # seconds

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "landing"

def safe_rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.stop()

def load_google_credentials():
    try:
        creds_dict = st.secrets["google_credentials"]
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        return creds
    except Exception as e:
        st.error("Error loading Google credentials from secrets.")
        st.error(e)
        st.stop()

def connect_google_sheet():
    creds = load_google_credentials()
    try:
        client = gspread.authorize(creds)
        sheet = client.open_by_key(CONFIG["GOOGLE_SHEET_ID"])
        return sheet
    except Exception as e:
        st.error("Could not connect to Google Sheet.")
        st.error(e)
        st.stop()

def get_or_create_monthly_sheet(sheet_obj):
    try:
        return sheet_obj.worksheet("MonthlyPlan")
    except WorksheetNotFound:
        return sheet_obj.add_worksheet(title="MonthlyPlan", rows="100", cols="26")

# 4) Sidebar: Login & Guidelines
with st.sidebar:
    st.header("Login")
    if not st.session_state.logged_in:
        user_in = st.text_input("Username")
        pass_in = st.text_input("Password", type="password")
        if st.button("Login"):
            if (
                user_in.strip() == CONFIG["USERNAME"].strip()
                and pass_in.strip() == CONFIG["PASSWORD"].strip()
            ):
                st.session_state.logged_in = True
                st.success("Logged in!")
            else:
                st.error("Invalid credentials.")
    else:
        st.info("You are logged in.")
    st.markdown("---")
    st.subheader("Guidelines")
    st.info(
    
        "• Use the back button to return to the homepage."
    )

# 5) Landing Page
def landing_page():
    st.title("Safebox Tasks Manager")
    cols = st.columns(3)
    if cols[0].button("Your Task"):
        with st.spinner("Opening Your Task..."):
            time.sleep(SPINNER_TIME)
        st.session_state.page = "your_task"
        safe_rerun()
    if cols[1].button("Edit Team's Task"):
        with st.spinner("Opening Edit Team's Task..."):
            time.sleep(SPINNER_TIME)
        st.session_state.page = "edit_team"
        safe_rerun()
    if cols[2].button("Schedule Monthly Tasks"):
        with st.spinner("Opening Monthly Tasks..."):
            time.sleep(SPINNER_TIME)
        st.session_state.page = "schedule_monthly"
        safe_rerun()

# 6) Your Task Page
def page_your_task():
    st.title("Your Task")
    if st.button("← Back"):
        with st.spinner("Returning..."):
            time.sleep(SPINNER_TIME)
        st.session_state.page = "landing"
        safe_rerun()

    sheet1 = connect_google_sheet().sheet1
    cols = st.columns(5)
    name  = cols[0].text_input("Name")
    email = cols[1].text_input("Email")
    dept  = cols[2].selectbox("Department", ["STARWOX","ZUMMEY","SAFEBOX ENERGY","CREATIVE","EXEC ASSISTANTS","DEVELOPERS"])
    proj  = cols[3].text_input("Project")
    date  = cols[4].date_input("Date")

    st.markdown("### Tasks")
    ta, tb, tc = st.columns(3)
    t1 = ta.text_input("Task 1")
    t2 = ta.text_input("Task 2")
    t3 = tb.text_input("Task 3")
    t4 = tb.text_input("Task 4")
    t5 = tc.text_input("Task 5")
    t6 = tc.text_input("Task 6")

    if st.button("Submit Tasks"):
        with st.spinner("Submitting tasks..."):
            time.sleep(SPINNER_TIME)
        if not all([name,email,dept,proj]):
            st.error("Fill Name, Email, Department, and Project.")
        else:
            row = [str(date), name, email, dept, proj, t1,t2,t3,t4,t5,t6]
            try:
                sheet1.append_row(row)
                st.success("Tasks submitted!✅")
            except Exception as e:
                st.error("Error appending row.")
                st.error(e)

# 7) Edit Team's Task Page
def page_edit_team():
    st.title("Edit Team's Task")
    if st.button("← Back"):
        with st.spinner("Returning..."):
            time.sleep(SPINNER_TIME)
        st.session_state.page = "landing"
        safe_rerun()

    sheet_obj = connect_google_sheet()
    cols = st.columns(3)
    name = cols[0].text_input("Name")
    ws   = cols[1].selectbox("Sheet", ["STARWOX","ZUMMEY","SAFEBOX ENERGY","CREATIVE","EXEC ASSISTANTS","DEVELOPERS"])
    date = cols[2].date_input("Date")

    if st.button("Fetch Tasks"):
        with st.spinner("Fetching..."):
            time.sleep(SPINNER_TIME)
        sht  = sheet_obj.worksheet(ws)
        rows = sht.get_all_values()
        match, idx = None, None
        for i, r in enumerate(rows[1:], start=2):
            if r[0]==str(date) and r[1].lower()==name.lower():
                match, idx = r, i
                break
        if not match:
            st.warning("No matching row.")
            return

        tasks = (match[5:11] + [""]*6)[:6]
        c1,c2,c3 = st.columns(3)
        nt1 = c1.text_input("Task 1", value=tasks[0], key="t1")
        nt2 = c2.text_input("Task 2", value=tasks[1], key="t2")
        nt3 = c3.text_input("Task 3", value=tasks[2], key="t3")
        nt4 = c1.text_input("Task 4", value=tasks[3], key="t4")
        nt5 = c2.text_input("Task 5", value=tasks[4], key="t5")
        nt6 = c3.text_input("Task 6", value=tasks[5], key="t6")
        st.session_state.row_idx = idx

    if st.button("Send Comments"):
        with st.spinner("Submitting comment..."):
            time.sleep(SPINNER_TIME)
        comment = st.text_area("Supervisor's Comment")
        if not comment.strip():
            st.error("Enter a comment.")
        else:
            try:
                sheet_obj.worksheet(ws).update_cell(st.session_state.row_idx, 12, comment)
                st.success("Comment submitted!✅")
            except Exception as e:
                st.error("Error updating comment.")
                st.error(e)

# 8) Schedule Monthly Tasks Page
def page_schedule_monthly():
    st.title("Schedule Monthly Tasks")
    if st.button("← Back"):
        with st.spinner("Returning..."):
            time.sleep(SPINNER_TIME)
        st.session_state.page = "landing"
        safe_rerun()

    date = st.date_input("Month Date")
    month = date.strftime("%B")
    st.write(f"Preparing {month}")

    goals = st.text_area("Monthly Goals")
    kpis  = st.text_area("KPIs")
    plans = st.text_area("Plans")

    weeks = ["wk1","wk2","wk3","wk4"]
    for i, w in enumerate(weeks, start=1):
        st.markdown(f"**Week {i}**")
        st.text_input(f"{w}_goals", key=f"{w}_goals")
        st.text_input(f"{w}_plans", key=f"{w}_plans")
        st.text_input(f"{w}_individual", key=f"{w}_individual")
        st.text_input(f"{w}_completed", key=f"{w}_completed")

    if st.button("Submit Monthly Schedule"):
        with st.spinner("Submitting schedule..."):
            time.sleep(SPINNER_TIME)
        ms = get_or_create_monthly_sheet(connect_google_sheet())
        header = ms.row_values(1)
        col_idx = next((i for i,v in enumerate(header,1) if v.lower()==month.lower()), None)
        if not col_idx:
            st.error(f"No column for {month}: {header}")
            return
        try:
            ms.update_cell(2, col_idx, goals)
            ms.update_cell(3, col_idx, kpis)
            # fill weeks 1–4 rows in blocks of 4, skipping separators
            base_rows = {1:5, 2:10, 3:15, 4:20}
            for i, w in enumerate(weeks, start=1):
                r0 = base_rows[i]
                ms.update_cell(r0,   col_idx, st.session_state[f"{w}_goals"])
                ms.update_cell(r0+1, col_idx, st.session_state[f"{w}_plans"])
                ms.update_cell(r0+2, col_idx, st.session_state[f"{w}_individual"])
                ms.update_cell(r0+3, col_idx, st.session_state[f"{w}_completed"])
            st.success("Monthly schedule submitted!✅")
        except Exception as e:
            st.error("Error updating monthly schedule.")
            st.error(e)

# 9) Render pages
if st.session_state.logged_in:
    {
        "landing":           landing_page,
        "your_task":         page_your_task,
        "edit_team":         page_edit_team,
        "schedule_monthly":  page_schedule_monthly,
    }[st.session_state.page]()
else:
    st.warning("Please log in from the sidebar to continue.")


