
# import os
# import time
# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# from dotenv import load_dotenv
# from datetime import datetime
# from gspread.exceptions import WorksheetNotFound

# # 1) Set up Streamlit page config first
# st.set_page_config(page_title="Safebox Tasks Manager", layout="wide")

# # 2) Load config from .env for local testing
# load_dotenv()
# CONFIG = {
#     "USERNAME": os.getenv("APP_USERNAME", ""),
#     "PASSWORD": os.getenv("APP_PASSWORD", ""),
#     "GOOGLE_SHEET_ID": os.getenv("GOOGLE_SHEET_ID", ""),
#     "SMTP_SERVER": os.getenv("SMTP_SERVER", ""),
#     "SMTP_PORT": os.getenv("SMTP_PORT", ""),
#     "SMTP_USER": os.getenv("SMTP_USER", ""),
#     "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", "")
# }

# # 3) Initialize session state variables
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "page" not in st.session_state:
#     st.session_state.page = "landing"  # Options: landing, your_task, edit_team, schedule_monthly

# # --- Helper: Safe Rerun ---
# def safe_rerun():
#     if hasattr(st, "experimental_rerun"):
#         st.experimental_rerun()
#     else:
#         st.stop()

# # --- Helper: Load Google Credentials ---
# def load_google_credentials():
#     try:
#         creds = Credentials.from_service_account_file(
#             "credentials.json",
#             scopes=["https://www.googleapis.com/auth/spreadsheets"]
#         )
#         return creds
#     except Exception as e:
#         st.error("Error loading 'credentials.json'. Please ensure it exists and is valid.")
#         st.error(e)
#         st.stop()

# # --- Helper: Connect to Google Sheet ---
# def connect_google_sheet():
#     creds = load_google_credentials()
#     try:
#         client = gspread.authorize(creds)
#         sheet = client.open_by_key(CONFIG["GOOGLE_SHEET_ID"])
#         return sheet
#     except Exception as e:
#         st.error("Could not connect to Google Sheet. Check your GOOGLE_SHEET_ID and credentials.")
#         st.error(e)
#         st.stop()

# # --- Helper: Get or Create Monthly Sheet ---
# def get_or_create_monthly_sheet(sheet_obj):
#     try:
#         monthly_sheet = sheet_obj.worksheet("MonthlyPlan")
#     except WorksheetNotFound:
#         monthly_sheet = sheet_obj.add_worksheet(title="MonthlyPlan", rows="100", cols="26")
#     return monthly_sheet

# # --- (Optional) Helper: Send Email ---
# # Note: With the new approach, the app no longer sends emails directly.
# # Instead, it writes the supervisor comment to a designated column in the sheet.
# # An external Apps Script is responsible for monitoring that column and triggering emails.

# # 4) Sidebar: Login & Guidelines
# with st.sidebar:
#     st.header("Login")
#     if not st.session_state.logged_in:
#         user_in = st.text_input("Username")
#         pass_in = st.text_input("Password", type="password")
#         if st.button("Login"):
#             if user_in.strip() == CONFIG["USERNAME"].strip() and pass_in.strip() == CONFIG["PASSWORD"].strip():
#                 st.session_state.logged_in = True
#                 st.success("Logged in!")
#             else:
#                 st.error("Invalid username or password.")
#     else:
#         st.info("You are logged in.")
#     st.markdown("---")
#     st.subheader("Guidelines")
#     st.info(
#         "1. Use the buttons on the landing page to select your action.\n"
#         "2. Each page has a back arrow to return to the landing page.\n"
#         "3. All buttons display a 2-second spinner."
#     )

# # 5) Landing Page: Three side-by-side buttons
# def landing_page():
#     st.title("Safebox Tasks Manager - Landing Page")
#     st.write("Choose an action below:")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         if st.button("Your Task"):
#             with st.spinner("Opening Your Task..."):
#                 time.sleep(2)
#             st.session_state.page = "your_task"
#             safe_rerun()
#     with col2:
#         if st.button("Edit Team's Task"):
#             with st.spinner("Opening Edit Team's Task..."):
#                 time.sleep(2)
#             st.session_state.page = "edit_team"
#             safe_rerun()
#     with col3:
#         if st.button("Schedule Monthly Tasks"):
#             with st.spinner("Opening Monthly Tasks..."):
#                 time.sleep(2)
#             st.session_state.page = "schedule_monthly"
#             safe_rerun()

# # 6) Page: Your Task (Write Tasks to the Sheet)
# def page_your_task():
#     st.title("Your Task - Write Tasks to the Sheet")
#     if st.button("← Back to Landing"):
#         with st.spinner("Returning..."):
#             time.sleep(2)
#         st.session_state.page = "landing"
#         safe_rerun()
#     st.markdown("---")
#     sheet_obj = connect_google_sheet()
#     sheet1 = sheet_obj.sheet1

#     # Now include Email in the landing page
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         name = st.text_input("Name")
#     with col2:
#         email = st.text_input("Email")  # New email column added here (will be written to the sheet)
#     with col3:
#         departments = ["STARWOX", "ZUMMEY", "SAFEBOX ENERGY", "CREATIVE", "EXECUTIVE ASSISTANTS", "DEVELOPERS"]
#         department = st.selectbox("Department", departments)
#     with col4:
#         project = st.text_input("Project")
#     with col5:
#         date_val = st.date_input("Date")

#     st.markdown("### Tasks (1 - 6)")
#     colA, colB, colC = st.columns(3)
#     with colA:
#         task1 = st.text_input("Task 1 (10-11am)")
#         task2 = st.text_input("Task 2 (11-12pm)")
#     with colB:
#         task3 = st.text_input("Task 3 (12:40-2pm)")
#         task4 = st.text_input("Task 4 (2-3pm)")
#     with colC:
#         task5 = st.text_input("Task 5 (3-4pm)")
#         task6 = st.text_input("Task 6 (4-5pm)")

#     if st.button("Submit Tasks"):
#         with st.spinner("Submitting tasks..."):
#             time.sleep(2)
#         if not all([name.strip(), email.strip(), department.strip(), project.strip()]):
#             st.error("Please fill in Name, Email, Department, and Project.")
#         else:
#             # Row format: Date, Name, Email, Department, Project, Task1, ..., Task6
#             row_data = [str(date_val), name, email, department, project, task1, task2, task3, task4, task5, task6]
#             try:
#                 sheet1.append_row(row_data)
#                 st.success("Tasks submitted successfully!")
#             except Exception as e:
#                 st.error("Error appending row to the sheet.")
#                 st.error(e)

# # 7) Page: Edit Team's Task (Fetch & Comment)
# def page_edit_team():
#     st.title("Edit Team's Task - Fetch & Comment")
#     if st.button("← Back to Landing"):
#         with st.spinner("Returning..."):
#             time.sleep(2)
#         st.session_state.page = "landing"
#         safe_rerun()
#     st.markdown("---")
#     sheet_obj = connect_google_sheet()
#     # New first row: Name, dropdown for sheet, Date (Email is no longer entered here)
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         name = st.text_input("Name (case-insensitive)")
#     with col2:
#         sheet_options = ["STARWOX", "ZUMMEY", "SAFEBOX ENERGY", "CREATIVE", "EXECUTIVE ASSISTANTS", "DEVELOPERS"]  # Assuming team tasks are on one of these sheets
#         selected_sheet = st.selectbox("Select Sheet", sheet_options)
#     with col3:
#         date_val = st.date_input("Date")
    
#     if st.button("Fetch Tasks"):
#         with st.spinner("Fetching tasks..."):
#             time.sleep(2)
#         if not name.strip():
#             st.error("Please enter a name.")
#         else:
#             try:
#                 sheet_to_fetch = sheet_obj.worksheet(selected_sheet)
#                 all_rows = sheet_to_fetch.get_all_values()
#                 matched_row = None
#                 row_index = None
#                 for idx, row in enumerate(all_rows, start=1):
#                     if idx == 1:  # skip header row
#                         continue
#                     if len(row) >= 2:
#                         if row[0].strip() == str(date_val) and row[1].strip().lower() == name.strip().lower():
#                             matched_row = row
#                             row_index = idx
#                             break
#                 if matched_row and row_index:
#                     st.success("Tasks found:")
#                     tasks = matched_row[5:11]  # Assuming tasks start from column F (after Date, Name, Email, Department, Project)
#                     while len(tasks) < 6:
#                         tasks.append("")
#                     colA, colB, colC = st.columns(3)
#                     new_task1 = colA.text_input("Task 1", value=tasks[0], key="edit_task1")
#                     new_task2 = colB.text_input("Task 2", value=tasks[1], key="edit_task2")
#                     new_task3 = colC.text_input("Task 3", value=tasks[2], key="edit_task3")
#                     colD, colE, colF = st.columns(3)
#                     new_task4 = colD.text_input("Task 4", value=tasks[3], key="edit_task4")
#                     new_task5 = colE.text_input("Task 5", value=tasks[4], key="edit_task5")
#                     new_task6 = colF.text_input("Task 6", value=tasks[5], key="edit_task6")
#                     # Save the row index in session state for later update
#                     st.session_state.matched_row_index = row_index
#                 else:
#                     st.warning("No matching tasks found for that Name & Date.")
#             except Exception as e:
#                 st.error("Error fetching tasks from the sheet.")
#                 st.error(e)
#     st.markdown("---")
#     supervisor_comment = st.text_area("Supervisor's Comment")
#     if st.button("Send Comments"):
#         with st.spinner("Submitting comment..."):
#             time.sleep(2)
#         if not supervisor_comment.strip():
#             st.error("Please enter a comment before sending.")
#         else:
#             # Instead of sending an email directly, write the supervisor comment to a designated column.
#             # Assume the "Supervisor's Comment" is stored in column L (12th column).
#             try:
#                 if "matched_row_index" in st.session_state:
#                     sheet_to_update = sheet_obj.worksheet(selected_sheet)
#                     sheet_to_update.update_cell(st.session_state.matched_row_index, 12, supervisor_comment)
#                     st.success("Supervisor's comment submitted successfully!")
#                 else:
#                     st.error("No matching task row found to update the comment.")
#             except Exception as e:
#                 st.error("Error updating supervisor comment in the sheet.")
#                 st.error(e)

# # 8) Page: Schedule Monthly Tasks
# def page_schedule_monthly():
#     st.title("Schedule Monthly Tasks")
#     if st.button("← Back to Landing"):
#         with st.spinner("Returning..."):
#             time.sleep(2)
#         st.session_state.page = "landing"
#         safe_rerun()
#     st.markdown("---")
#     monthly_date = st.date_input("Select a Date (month used for submission)")
#     month_name = datetime.strftime(monthly_date, "%B")
#     st.write(f"Submitting data for {month_name}.")
    
#     st.write("**MONTHLY GOALS:** (Enter goals for each month separated by commas)")
#     monthly_goals = st.text_area("Monthly Goals:", height=100)
#     st.write("**KPI'S:**")
#     kpis = st.text_area("KPI's:", height=70)
#     st.write("**PLANS:**")
#     plans = st.text_area("Plans:", height=70)
#     st.markdown("---")
#     st.subheader("Weeks Breakdown (2x2 Matrix)")
#     # Top row: Week 1 and Week 2
#     col_week_top = st.columns(2)
#     with col_week_top[0]:
#         st.write("**WEEK 1**")
#         wk1_goals = st.text_input("Week 1 Goals:", key="wk1_goals")
#         wk1_plans = st.text_input("Week 1 Plans:", key="wk1_plans")
#         wk1_individual = st.text_input("Week 1 Individual Task:", key="wk1_individual")
#         wk1_completed = st.text_input("Week 1 Task Completed:", key="wk1_completed")
#     with col_week_top[1]:
#         st.write("**WEEK 2**")
#         wk2_goals = st.text_input("Week 2 Goals:", key="wk2_goals")
#         wk2_plans = st.text_input("Week 2 Plans:", key="wk2_plans")
#         wk2_individual = st.text_input("Week 2 Individual Task:", key="wk2_individual")
#         wk2_completed = st.text_input("Week 2 Task Completed:", key="wk2_completed")
#     # Bottom row: Week 3 and Week 4
#     col_week_bottom = st.columns(2)
#     with col_week_bottom[0]:
#         st.write("**WEEK 3**")
#         wk3_goals = st.text_input("Week 3 Goals:", key="wk3_goals")
#         wk3_plans = st.text_input("Week 3 Plans:", key="wk3_plans")
#         wk3_individual = st.text_input("Week 3 Individual Task:", key="wk3_individual")
#         wk3_completed = st.text_input("Week 3 Task Completed:", key="wk3_completed")
#     with col_week_bottom[1]:
#         st.write("**WEEK 4**")
#         wk4_goals = st.text_input("Week 4 Goals:", key="wk4_goals")
#         wk4_plans = st.text_input("Week 4 Plans:", key="wk4_plans")
#         wk4_individual = st.text_input("Week 4 Individual Task:", key="wk4_individual")
#         wk4_completed = st.text_input("Week 4 Task Completed:", key="wk4_completed")
    
#     if st.button("Submit Monthly Schedule"):
#         with st.spinner("Submitting schedule..."):
#             time.sleep(2)
#         sheet_obj = connect_google_sheet()
#         monthly_sheet = get_or_create_monthly_sheet(sheet_obj)
#         header = monthly_sheet.row_values(1)
#         target_col = None
#         # Search the entire header row for the month name (ignoring case)
#         for idx, cell_val in enumerate(header, start=1):
#             if cell_val.strip().lower() == month_name.lower():
#                 target_col = idx
#                 break
#         if target_col is None:
#             st.error(f"Could not find a column for {month_name} in the header: {header}")
#             return
#         try:
#             # Write monthly data starting from row 2, skipping rows 4, 9, 14, and 19.
#             monthly_sheet.update_cell(2, target_col, monthly_goals)
#             monthly_sheet.update_cell(3, target_col, kpis)
#             # Week 1: rows 5-8
#             monthly_sheet.update_cell(5, target_col, st.session_state.get("wk1_goals", "")) 
#             monthly_sheet.update_cell(6, target_col, st.session_state.get("wk1_plans", ""))
#             monthly_sheet.update_cell(7, target_col, st.session_state.get("wk1_individual", ""))
#             monthly_sheet.update_cell(8, target_col, st.session_state.get("wk1_completed", ""))
            
#             # Week 2: rows 10-13
#             monthly_sheet.update_cell(10, target_col, st.session_state.get("wk2_goals", "")) 
#             monthly_sheet.update_cell(11, target_col, st.session_state.get("wk2_plans", ""))
#             monthly_sheet.update_cell(12, target_col, st.session_state.get("wk2_individual", ""))
#             monthly_sheet.update_cell(13, target_col, st.session_state.get("wk2_completed", ""))
            
#             # Week 3: rows 15-18
#             monthly_sheet.update_cell(15, target_col, st.session_state.get("wk3_goals", "")) 
#             monthly_sheet.update_cell(16, target_col, st.session_state.get("wk3_plans", ""))
#             monthly_sheet.update_cell(17, target_col, st.session_state.get("wk3_individual", ""))
#             monthly_sheet.update_cell(18, target_col, st.session_state.get("wk3_completed", ""))
            
#             # Week 4: rows 20-23
#             monthly_sheet.update_cell(20, target_col, st.session_state.get("wk4_goals", "")) 
#             monthly_sheet.update_cell(21, target_col, st.session_state.get("wk4_plans", ""))
#             monthly_sheet.update_cell(22, target_col, st.session_state.get("wk4_individual", ""))
#             monthly_sheet.update_cell(23, target_col, st.session_state.get("wk4_completed", ""))
#             st.success("Monthly schedule submitted successfully!")
#         except Exception as e:
#             st.error("Error updating monthly schedule in the sheet.")
#             st.error(e)

# # 9) Render Page Based on session_state.page
# if st.session_state.logged_in:
#     if st.session_state.page == "landing":
#         landing_page()
#     elif st.session_state.page == "your_task":
#         page_your_task()
#     elif st.session_state.page == "edit_team":
#         page_edit_team()
#     elif st.session_state.page == "schedule_monthly":
#         page_schedule_monthly()
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

# 2) Load config from st.secrets (configured via Streamlit Cloud)
# Your secrets.toml should define these keys at the root level:
# APP_USERNAME, APP_PASSWORD, GOOGLE_SHEET_ID, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
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
        # Instead of reading credentials.json, load credentials from st.secrets["google_credentials"]
        creds_dict = json.loads(st.secrets["google_credentials"])
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        return creds
    except Exception as e:
        st.error("Error loading Google credentials from st.secrets. Please ensure they are correctly configured.")
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

# --- Helper: Get or Create Monthly Sheet ---
def get_or_create_monthly_sheet(sheet_obj):
    try:
        monthly_sheet = sheet_obj.worksheet("MonthlyPlan")
    except WorksheetNotFound:
        monthly_sheet = sheet_obj.add_worksheet(title="MonthlyPlan", rows="100", cols="26")
    return monthly_sheet

# --- (Optional) Helper: Send Email ---
# Note: With the new approach, the app no longer sends emails directly.
# Instead, it writes the supervisor comment to a designated column in the sheet.
# An external Apps Script will monitor that column and trigger emails.

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

# 5) Landing Page: Three side-by-side buttons
def landing_page():
    st.title("Safebox Tasks Manager - Landing Page")
    st.write("Choose an action below:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Your Task"):
            with st.spinner("Opening Your Task..."):
                time.sleep(2)
            st.session_state.page = "your_task"
            safe_rerun()
    with col2:
        if st.button("Edit Team's Task"):
            with st.spinner("Opening Edit Team's Task..."):
                time.sleep(2)
            st.session_state.page = "edit_team"
            safe_rerun()
    with col3:
        if st.button("Schedule Monthly Tasks"):
            with st.spinner("Opening Monthly Tasks..."):
                time.sleep(2)
            st.session_state.page = "schedule_monthly"
            safe_rerun()

# 6) Page: Your Task (Write Tasks to the Sheet)
def page_your_task():
    st.title("Your Task - Write Tasks to the Sheet")
    if st.button("← Back to Landing"):
        with st.spinner("Returning..."):
            time.sleep(2)
        st.session_state.page = "landing"
        safe_rerun()
    st.markdown("---")
    sheet_obj = connect_google_sheet()
    sheet1 = sheet_obj.sheet1

    # Now include Email in the landing page
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        name = st.text_input("Name")
    with col2:
        email = st.text_input("Email")  # Email column will be written to the sheet
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
                sheet1.append_row(row_data)
                st.success("Tasks submitted successfully!")
            except Exception as e:
                st.error("Error appending row to the sheet.")
                st.error(e)

# 7) Page: Edit Team's Task (Fetch & Comment)
def page_edit_team():
    st.title("Edit Team's Task - Fetch & Comment")
    if st.button("← Back to Landing"):
        with st.spinner("Returning..."):
            time.sleep(2)
        st.session_state.page = "landing"
        safe_rerun()
    st.markdown("---")
    sheet_obj = connect_google_sheet()
    # New first row: Name, dropdown for sheet, Date (Email is now stored only on Your Task page)
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Name (case-insensitive)")
    with col2:
        # Use the same department list as on Your Task page (assuming team tasks are on these sheets)
        sheet_options = ["STARWOX", "ZUMMEY", "SAFEBOX ENERGY", "CREATIVE", "EXECUTIVE ASSISTANTS", "DEVELOPERS"]
        selected_sheet = st.selectbox("Select Sheet", sheet_options)
    with col3:
        date_val = st.date_input("Date")
    
    if st.button("Fetch Tasks"):
        with st.spinner("Fetching tasks..."):
            time.sleep(2)
        if not name.strip():
            st.error("Please enter a name.")
        else:
            try:
                sheet_to_fetch = sheet_obj.worksheet(selected_sheet)
                all_rows = sheet_to_fetch.get_all_values()
                matched_row = None
                row_index = None
                for idx, row in enumerate(all_rows, start=1):
                    if idx == 1:  # skip header row
                        continue
                    if len(row) >= 2:
                        if row[0].strip() == str(date_val) and row[1].strip().lower() == name.strip().lower():
                            matched_row = row
                            row_index = idx
                            break
                if matched_row and row_index:
                    st.success("Tasks found:")
                    tasks = matched_row[5:11]  # Assuming tasks start from column F (after Date, Name, Email, Department, Project)
                    while len(tasks) < 6:
                        tasks.append("")
                    colA, colB, colC = st.columns(3)
                    new_task1 = colA.text_input("Task 1", value=tasks[0], key="edit_task1")
                    new_task2 = colB.text_input("Task 2", value=tasks[1], key="edit_task2")
                    new_task3 = colC.text_input("Task 3", value=tasks[2], key="edit_task3")
                    colD, colE, colF = st.columns(3)
                    new_task4 = colD.text_input("Task 4", value=tasks[3], key="edit_task4")
                    new_task5 = colE.text_input("Task 5", value=tasks[4], key="edit_task5")
                    new_task6 = colF.text_input("Task 6", value=tasks[5], key="edit_task6")
                    # Save the row index in session state for later update
                    st.session_state.matched_row_index = row_index
                else:
                    st.warning("No matching tasks found for that Name & Date.")
            except Exception as e:
                st.error("Error fetching tasks from the sheet.")
                st.error(e)
    st.markdown("---")
    supervisor_comment = st.text_area("Supervisor's Comment")
    if st.button("Send Comments"):
        with st.spinner("Submitting comment..."):
            time.sleep(2)
        if not supervisor_comment.strip():
            st.error("Please enter a comment before sending.")
        else:
            # Write the supervisor comment to column L (12th column)
            try:
                if "matched_row_index" in st.session_state:
                    sheet_to_update = sheet_obj.worksheet(selected_sheet)
                    sheet_to_update.update_cell(st.session_state.matched_row_index, 12, supervisor_comment)
                    st.success("Supervisor's comment submitted successfully!")
                else:
                    st.error("No matching task row found to update the comment.")
            except Exception as e:
                st.error("Error updating supervisor comment in the sheet.")
                st.error(e)

# 8) Page: Schedule Monthly Tasks
def page_schedule_monthly():
    st.title("Schedule Monthly Tasks")
    if st.button("← Back to Landing"):
        with st.spinner("Returning..."):
            time.sleep(2)
        st.session_state.page = "landing"
        safe_rerun()
    st.markdown("---")
    monthly_date = st.date_input("Select a Date (month used for submission)")
    month_name = datetime.strftime(monthly_date, "%B")
    st.write(f"Submitting data for {month_name}.")
    
    st.write("**MONTHLY GOALS:** (Enter goals for each month separated by commas)")
    monthly_goals = st.text_area("Monthly Goals:", height=100)
    st.write("**KPI'S:**")
    kpis = st.text_area("KPI's:", height=70)
    st.write("**PLANS:**")
    plans = st.text_area("Plans:", height=70)
    st.markdown("---")
    st.subheader("Weeks Breakdown (2x2 Matrix)")
    # Top row: Week 1 and Week 2
    col_week_top = st.columns(2)
    with col_week_top[0]:
        st.write("**WEEK 1**")
        wk1_goals = st.text_input("Week 1 Goals:", key="wk1_goals")
        wk1_plans = st.text_input("Week 1 Plans:", key="wk1_plans")
        wk1_individual = st.text_input("Week 1 Individual Task:", key="wk1_individual")
        wk1_completed = st.text_input("Week 1 Task Completed:", key="wk1_completed")
    with col_week_top[1]:
        st.write("**WEEK 2**")
        wk2_goals = st.text_input("Week 2 Goals:", key="wk2_goals")
        wk2_plans = st.text_input("Week 2 Plans:", key="wk2_plans")
        wk2_individual = st.text_input("Week 2 Individual Task:", key="wk2_individual")
        wk2_completed = st.text_input("Week 2 Task Completed:", key="wk2_completed")
    # Bottom row: Week 3 and Week 4
    col_week_bottom = st.columns(2)
    with col_week_bottom[0]:
        st.write("**WEEK 3**")
        wk3_goals = st.text_input("Week 3 Goals:", key="wk3_goals")
        wk3_plans = st.text_input("Week 3 Plans:", key="wk3_plans")
        wk3_individual = st.text_input("Week 3 Individual Task:", key="wk3_individual")
        wk3_completed = st.text_input("Week 3 Task Completed:", key="wk3_completed")
    with col_week_bottom[1]:
        st.write("**WEEK 4**")
        wk4_goals = st.text_input("Week 4 Goals:", key="wk4_goals")
        wk4_plans = st.text_input("Week 4 Plans:", key="wk4_plans")
        wk4_individual = st.text_input("Week 4 Individual Task:", key="wk4_individual")
        wk4_completed = st.text_input("Week 4 Task Completed:", key="wk4_completed")
    
    if st.button("Submit Monthly Schedule"):
        with st.spinner("Submitting schedule..."):
            time.sleep(2)
        sheet_obj = connect_google_sheet()
        monthly_sheet = get_or_create_monthly_sheet(sheet_obj)
        header = monthly_sheet.row_values(1)
        target_col = None
        # Search the entire header row for the month name (ignoring case)
        for idx, cell_val in enumerate(header, start=1):
            if cell_val.strip().lower() == month_name.lower():
                target_col = idx
                break
        if target_col is None:
            st.error(f"Could not find a column for {month_name} in the header: {header}")
            return
        try:
            # Write monthly data starting from row 2, skipping rows 4, 9, 14, and 19.
            monthly_sheet.update_cell(2, target_col, monthly_goals)
            monthly_sheet.update_cell(3, target_col, kpis)
            # Week 1: rows 5-8
            monthly_sheet.update_cell(5, target_col, st.session_state.get("wk1_goals", "")) 
            monthly_sheet.update_cell(6, target_col, st.session_state.get("wk1_plans", ""))
            monthly_sheet.update_cell(7, target_col, st.session_state.get("wk1_individual", ""))
            monthly_sheet.update_cell(8, target_col, st.session_state.get("wk1_completed", ""))
            
            # Week 2: rows 10-13
            monthly_sheet.update_cell(10, target_col, st.session_state.get("wk2_goals", "")) 
            monthly_sheet.update_cell(11, target_col, st.session_state.get("wk2_plans", ""))
            monthly_sheet.update_cell(12, target_col, st.session_state.get("wk2_individual", ""))
            monthly_sheet.update_cell(13, target_col, st.session_state.get("wk2_completed", ""))
            
            # Week 3: rows 15-18
            monthly_sheet.update_cell(15, target_col, st.session_state.get("wk3_goals", "")) 
            monthly_sheet.update_cell(16, target_col, st.session_state.get("wk3_plans", ""))
            monthly_sheet.update_cell(17, target_col, st.session_state.get("wk3_individual", ""))
            monthly_sheet.update_cell(18, target_col, st.session_state.get("wk3_completed", ""))
            
            # Week 4: rows 20-23
            monthly_sheet.update_cell(20, target_col, st.session_state.get("wk4_goals", "")) 
            monthly_sheet.update_cell(21, target_col, st.session_state.get("wk4_plans", ""))
            monthly_sheet.update_cell(22, target_col, st.session_state.get("wk4_individual", ""))
            monthly_sheet.update_cell(23, target_col, st.session_state.get("wk4_completed", ""))
            st.success("Monthly schedule submitted successfully!")
        except Exception as e:
            st.error("Error updating monthly schedule in the sheet.")
            st.error(e)

# 9) Render Page Based on session_state.page
if st.session_state.logged_in:
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "your_task":
        page_your_task()
    elif st.session_state.page == "edit_team":
        page_edit_team()
    elif st.session_state.page == "schedule_monthly":
        page_schedule_monthly()
else:
    st.warning("Please log in from the sidebar to continue.")
