import os
import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
from dotenv import load_dotenv

def main():
    # Load environment variables from .env for non-sensitive values (optional)
    load_dotenv()
    
    # Optionally, load GOOGLE_SHEET_ID from secrets as well, if you want to keep it out of .env:
    google_sheet_id = st.secrets["general"]["GOOGLE_SHEET_ID"] if "general" in st.secrets and "GOOGLE_SHEET_ID" in st.secrets["general"] else os.getenv("GOOGLE_SHEET_ID")

    # Set up Streamlit page config
    st.set_page_config(page_title="Safebox Task and Accountability Form", layout="wide")

    # Sidebar with instructions
    st.sidebar.title("Instructions")
    st.sidebar.info(
        """
        1. Fill in your **Name**, **Project**, and select your **Department** and **Date**.
        2. Enter your tasks in the matrix below:
           - First row: Task 1 (10-11), Task 2 (11-12), Task 3 (12:40-2).
           - Second row: Task 4 (2-3), Task 5 (3-4), Task 6 (4-5).
        3. If you have already submitted for the selected date, your previous submission will be updated.
        4. **All fields must be filled** before submission.
        5. Click the **Submit** button to record your entry.
        """
    )

    # Main title
    st.markdown(
        """
        <h1 style="text-align: center;">SAFEBOX TASK AND ACCOUNTABILITY FORM</h1>
        """, unsafe_allow_html=True
    )

    # Connect to Google Sheets using credentials from Streamlit secrets.
    # Replace file-based credentials with credentials loaded from st.secrets.
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict)
    client = gspread.authorize(creds)

    # Top section: Name, Department, Project, Date
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            name = st.text_input("Name")
        with col2:
            department_options = [
                "STARWOX", 
                "ZUMMEY", 
                "SAFEBOX ENERGY", 
                "CREATIVE", 
                "EXECUTIVE ASSISTANTS", 
                "DEVELOPERS"
            ]
            department = st.selectbox("Department", department_options)
        with col3:
            project = st.text_input("Project")
        with col4:
            date = st.date_input("Date")

    # Tasks section: 3x2 matrix layout
    st.markdown("### Tasks")
    col1, col2, col3 = st.columns(3)
    with col1:
        task1 = st.text_input("Task 1 (10am-11am)")
    with col2:
        task2 = st.text_input("Task 2 (11am-12pm)")
    with col3:
        task3 = st.text_input("Task 3 (12:40pm - 2pm)")

    col4, col5, col6 = st.columns(3)
    with col4:
        task4 = st.text_input("Task 4 (2pm-3pm)")
    with col5:
        task5 = st.text_input("Task 5 (3pm-4pm)")
    with col6:
        task6 = st.text_input("Task 6 (4pm-5pm)")

    # Centralized Submit Button with validation
    submit_cols = st.columns(3)
    with submit_cols[1]:
        if st.button("Submit"):
            # Validate that all required fields are filled (trim whitespace)
            if not all([
                name.strip(), 
                project.strip(), 
                task1.strip(), 
                task2.strip(), 
                task3.strip(), 
                task4.strip(), 
                task5.strip(), 
                task6.strip()
            ]):
                st.error("Please fill in all fields before submitting.")
            else:
                # Prepare row data (9 columns): Date, Name, Project, Task1, Task2, Task3, Task4, Task5, Task6
                row_data = [
                    str(date),
                    name,
                    project,
                    task1,
                    task2,
                    task3,
                    task4,
                    task5,
                    task6
                ]

                # Open the worksheet corresponding to the selected department
                worksheet = client.open_by_key(google_sheet_id).worksheet(department)
                all_rows = worksheet.get_all_values()

                # Check if an entry exists (matching Date and Name; assuming header is in the first row)
                row_to_update = None
                for idx, row in enumerate(all_rows[1:], start=2):
                    if row and len(row) >= 2:
                        if row[0] == str(date) and row[1].strip().lower() == name.strip().lower():
                            row_to_update = idx
                            break

                if row_to_update:
                    # Update the existing row (columns A to I for 9 columns)
                    worksheet.update(f'A{row_to_update}:I{row_to_update}', [row_data])
                    st.success("Your existing submission for this date has been updated.")
                else:
                    # Append as a new row
                    worksheet.append_row(row_data)
                    st.success("Submitted.")

if __name__ == "__main__":
    main()





# import os
# import streamlit as st
# from google.oauth2.service_account import Credentials
# import gspread
# from dotenv import load_dotenv

# def main():
#     # Load environment variables from .env
#     load_dotenv()
#     google_sheet_id = os.getenv("GOOGLE_SHEET_ID")

#     # Set up Streamlit page config
#     st.set_page_config(page_title="Safebox Task and Accountability Form", layout="wide")

#     # Sidebar with instructions
#     st.sidebar.title("Instructions")
#     st.sidebar.info(
#         """
#         1. Fill in your **Name**, **Project**, and select your **Department** and **Date**.
#         2. Enter your tasks in the matrix below:
#            - First row: Task 1 (10-11), Task 2 (11-12), Task 3 (12:40-2).
#            - Second row: Task 4 (2-3), Task 5 (3-4), Task 6 (4-5).
#         3. If you have already submitted for the selected date, your previous submission will be updated.
#         4. Click the **Submit** button to record your entry.
#         """
#     )

#     # Main title
#     st.markdown(
#         """
#         <h1 style="text-align: center;">SAFEBOX TASK AND ACCOUNTABILITY FORM</h1>
#         """, unsafe_allow_html=True
#     )

#     # Connect to Google Sheets using the service account credentials
#     creds = Credentials.from_service_account_file(
#         'credentials.json',
#         scopes=["https://www.googleapis.com/auth/spreadsheets"]
#     )
#     client = gspread.authorize(creds)

#     # Top section: Name, Department, Project, Date
#     with st.container():
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             name = st.text_input("Name")
#         with col2:
#             department_options = [
#                 "STARWOX", 
#                 "ZUMMEY", 
#                 "SAFEBOX ENERGY", 
#                 "CREATIVE", 
#                 "EXECUTIVE ASSISTANTS", 
#                 "DEVELOPERS"
#             ]
#             department = st.selectbox("Department", department_options)
#         with col3:
#             project = st.text_input("Project")
#         with col4:
#             date = st.date_input("Date")

#     # Tasks section: 3x2 matrix layout
#     st.markdown("### Tasks")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         task1 = st.text_input("Task 1 (10am -11am)")
#     with col2:
#         task2 = st.text_input("Task 2 (11am - 12pm)")
#     with col3:
#         task3 = st.text_input("Task 3 (12:40pm - 2pm)")

#     col4, col5, col6 = st.columns(3)
#     with col4:
#         task4 = st.text_input("Task 4 (2pm-3pm)")
#     with col5:
#         task5 = st.text_input("Task 5 (3pm-4pm)")
#     with col6:
#         task6 = st.text_input("Task 6 (4pm-5pm)")

#     # Centralized Submit Button
#     submit_cols = st.columns(3)
#     with submit_cols[1]:
#         if st.button("Submit"):
#             # Prepare row data (9 columns): Date, Name, Project, Task1, Task2, Task3, Task4, Task5, Task6
#             row_data = [
#                 str(date),
#                 name,
#                 project,
#                 task1,
#                 task2,
#                 task3,
#                 task4,
#                 task5,
#                 task6
#             ]

#             # Open the worksheet corresponding to the selected department
#             worksheet = client.open_by_key(google_sheet_id).worksheet(department)
#             all_rows = worksheet.get_all_values()

#             # Initialize variable to track if an entry exists.
#             # Assuming the first row is header, we check from row 2 onward.
#             row_to_update = None
#             for idx, row in enumerate(all_rows[1:], start=2):
#                 # Compare Date (as string) and Name (case-insensitive, trimmed)
#                 if row and len(row) >= 2:
#                     if row[0] == str(date) and row[1].strip().lower() == name.strip().lower():
#                         row_to_update = idx
#                         break

#             if row_to_update:
#                 # Update existing row (columns A to I for 9 columns)
#                 worksheet.update(f'A{row_to_update}:I{row_to_update}', [row_data])
#                 st.success("Your existing submission for today has been updated.")
#             else:
#                 # Append as a new row
#                 worksheet.append_row(row_data)
#                 st.success("submitted.")

# if __name__ == "__main__":
#     main()











