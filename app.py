import streamlit as st
import pandas as pd
from backend import *

st.set_page_config(page_title="Student Management System", layout="centered")

USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN SYSTEM ----------------
if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()  # Stop app if not logged in


load_students()


st.title("🎓 Student Management System")


if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

menu = ["Add Student", "View Students", "Search Student", "Delete Student"]
choice = st.sidebar.selectbox("Menu", menu)


if choice == "Add Student":
    st.subheader("Add Student")

    name = st.text_input("Enter Name")
    roll = st.text_input("Enter Roll Number")
    marks = st.text_input("Enter Marks")

    if st.button("Add Student"):
        if not name.strip():
            st.error("Name cannot be empty")
        else:
            result = add_student(name, int(roll), float(marks))

            if "successfully" in result:
                st.success(result)
            else:
                st.error(result)


elif choice == "View Students":
    st.subheader("All Students")

    students_list = get_all_students()

    if not students_list:
        st.warning("No students found")
    else:
        data = []
        for s in students_list:
            data.append({
                "Name": s.name,
                "Roll": s.roll,
                "Marks": s.marks,
                "Grade": s.get_grade()
            })

        df = pd.DataFrame(data)

        df.insert(0, "No.", range(1, len(df) + 1))

        st.dataframe(df, hide_index=True)

        # CSV Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="students.csv",
            mime="text/csv"
        )


elif choice == "Search Student":
    st.subheader("Search Student")

    roll = st.text_input("Enter Roll Number")

    if st.button("Search"):
        student = search_student(int(roll))

        if student:
            st.success("Student Found")
            st.write({
                "Name": student.name,
                "Roll": student.roll,
                "Marks": student.marks,
                "Grade": student.get_grade()
            })
        else:
            st.error("Student not found")


elif choice == "Delete Student":
    st.subheader("Delete Student")

    roll = st.text_input("Enter Roll Number")

    if st.button("Delete"):
        result = delete_student(int(roll))

        if "successfully" in result:
            st.success(result)
        else:
            st.error(result)