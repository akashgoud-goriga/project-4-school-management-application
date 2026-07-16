from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="School Management Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern, polished aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    div[data-testid="metric-container"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATABASE & OOP BACKEND LOGIC
# -----------------------------------------------------------------------------
DATABASE_FILE = "school_data.json"

def load_data():
    if Path(DATABASE_FILE).exists():
        try:
            with open(DATABASE_FILE, "r") as f:
                content = f.read()
                if content:
                    return json.loads(content)
        except Exception as e:
            st.error(f"Error reading database: {e}")
    return {"students": [], "teachers": []}

def save_data(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Person(ABC):
    @abstractmethod
    def get_role(self):
        pass
    
    @staticmethod
    def email_verification(email):
        return "@" in email and "." in email

class StudentManager(Person):
    def __init__(self, data):
        self.data = data

    def get_role(self):
        return "student"

    def register(self, name, stu_class, section, roll_no, email):
        if not self.email_verification(email):
            return False, "Invalid email format. Must contain '@' and '.'."
        
        for student in self.data['students']:
            if student["roll_no"] == roll_no:
                return False, f"Student with Roll No {roll_no} already exists!"
                
        self.data['students'].append({
            "name": name,
            "Class": stu_class,
            "roll_no": roll_no,
            "section": section,
            "email": email,
            "grades": {},
            "attendance": {}
        })
        save_data(self.data)
        return True, f"Student '{name}' registered successfully!"

    def get_details(self, roll_no):
        for student in self.data['students']:
            if student["roll_no"] == roll_no:
                return student
        return None

    def add_grade(self, roll_no, subject, marks):
        for student in self.data['students']:
            if student["roll_no"] == roll_no:
                student["grades"][subject] = marks
                save_data(self.data)
                return True, f"Grade added successfully for {subject}!"
        return False, "Student not found."

    def add_attendance(self, roll_no, month, attendance_days):
        for student in self.data['students']:
            if student["roll_no"] == roll_no:
                student["attendance"][month] = attendance_days
                save_data(self.data)
                return True, f"Attendance logged for {month}!"
        return False, "Student not found."

class TeacherManager(Person):
    def __init__(self, data):
        self.data = data

    def get_role(self):
        return "teacher"

    def register(self, name, subject, emp_id, email):
        if not self.email_verification(email):
            return False, "Invalid email format. Must contain '@' and '.'."
            
        for teacher in self.data['teachers']:
            if teacher["employee_id"] == emp_id:
                return False, f"Teacher with Employee ID {emp_id} already exists!"
                
        self.data['teachers'].append({
            "name": name,
            "subject": subject,
            "employee_id": emp_id,
            "email": email,
            "attendance": {}
        })
        save_data(self.data)
        return True, f"Teacher '{name}' registered successfully!"

    def get_details(self, emp_id):
        for teacher in self.data['teachers']:
            if teacher["employee_id"] == emp_id:
                return teacher
        return None

    def add_attendance(self, emp_id, month, attendance_days):
        for teacher in self.data['teachers']:
            if teacher["employee_id"] == emp_id:
                teacher["attendance"][month] = attendance_days
                save_data(self.data)
                return True, f"Attendance logged for {month}!"
        return False, "Teacher not found."

# -----------------------------------------------------------------------------
# 3. STREAMLIT USER INTERFACE
# -----------------------------------------------------------------------------

# Initialize data in session state
if 'db' not in st.session_state:
    st.session_state.db = load_data()

db = st.session_state.db
stu_mgr = StudentManager(db)
teach_mgr = TeacherManager(db)

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=70)
    st.markdown("### School Dashboard")
    menu = st.radio(
        "Navigation",
        ["📊 Overview & Analytics", "🎓 Student Portal", "👨‍🏫 Teacher Portal"],
        index=0
    )
    st.divider()
    st.caption("Database Status: Connected 🟢")
    st.caption(f"Storage File: `{DATABASE_FILE}`")

# --- VIEW 1: OVERVIEW & ANALYTICS ---
if menu == "📊 Overview & Analytics":
    st.markdown('<div class="main-header">📊 School Overview & Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">View high-level metrics and current rosters stored in the database.</div>', unsafe_allow_html=True)
    
    # Metric Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Enrolled Students", value=len(db["students"]))
    with col2:
        st.metric(label="Total Faculty Members", value=len(db["teachers"]))
    with col3:
        total_records = len(db["students"]) + len(db["teachers"])
        st.metric(label="Total Database Records", value=total_records)
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🎓 Student Roster")
        if db["students"]:
            df_stu = pd.DataFrame(db["students"])[["roll_no", "name", "Class", "section", "email"]]
            st.dataframe(df_stu, use_container_width=True, hide_index=True)
        else:
            st.info("No students registered yet.")
            
    with col_b:
        st.subheader("👨‍🏫 Teacher Roster")
        if db["teachers"]:
            df_teach = pd.DataFrame(db["teachers"])[["employee_id", "name", "subject", "email"]]
            st.dataframe(df_teach, use_container_width=True, hide_index=True)
        else:
            st.info("No teachers registered yet.")

# --- VIEW 2: STUDENT PORTAL ---
elif menu == "🎓 Student Portal":
    st.markdown('<div class="main-header">🎓 Student Management Portal</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Register Student", "🔍 View Details", "📝 Add Grades", "📅 Manage Attendance"])
    
    # TAB 1: Register
    with tab1:
        st.subheader("Register a New Student")
        with st.form("student_reg_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *")
                roll_no = st.number_input("Roll Number *", min_value=1, step=1)
                email = st.text_input("Email Address *")
            with col2:
                stu_class = st.number_input("Class / Grade *", min_value=1, max_value=12, step=1)
                section = st.text_input("Section *", max_chars=5).upper()
            
            submitted = st.form_submit_button("Register Student", type="primary")
            if submitted:
                if name and email and section:
                    success, msg = stu_mgr.register(name, stu_class, section, roll_no, email)
                    if success:
                        st.success(msg)
                        st.session_state.db = load_data()  # Refresh state
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill out all required fields.")

    # TAB 2: View Details
    with tab2:
        st.subheader("Search Student Record")
        search_roll = st.number_input("Enter Student Roll Number:", min_value=1, step=1)
        if st.button("Search Student", type="primary"):
            student = stu_mgr.get_details(search_roll)
            if student:
                st.success(f"Record found for: **{student['name']}**")
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Roll Number:** {student['roll_no']}")
                    st.write(f"**Class:** {student['Class']} - {student['section']}")
                    st.write(f"**Email:** {student['email']}")
                with c2:
                    st.write("**Grades:**")
                    st.json(student.get("grades", {}))
                    st.write("**Attendance:**")
                    st.json(student.get("attendance", {}))
            else:
                st.error("No student found with that Roll Number.")

    # TAB 3: Add Grades
    with tab3:
        st.subheader("Add Subject Grades")
        if not db["students"]:
            st.warning("Please register a student first.")
        else:
            student_options = {f"{s['name']} (Roll: {s['roll_no']})": s["roll_no"] for s in db["students"]}
            selected_student_label = st.selectbox("Select Student:", list(student_options.keys()))
            selected_roll = student_options[selected_student_label]
            
            with st.form("grade_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    subject = st.text_input("Subject Name (e.g., Mathematics)")
                with col2:
                    marks = st.number_input("Marks Obtained", min_value=0, max_value=100, step=1)
                
                if st.form_submit_button("Save Grade", type="primary"):
                    if subject:
                        success, msg = stu_mgr.add_grade(selected_roll, subject, marks)
                        if success:
                            st.success(msg)
                            st.session_state.db = load_data()
                        else:
                            st.error(msg)
                    else:
                        st.warning("Please enter a subject name.")

    # TAB 4: Attendance
    with tab4:
        st.subheader("Log Student Attendance")
        if not db["students"]:
            st.warning("Please register a student first.")
        else:
            student_options = {f"{s['name']} (Roll: {s['roll_no']})": s["roll_no"] for s in db["students"]}
            selected_student_label = st.selectbox("Select Student for Attendance:", list(student_options.keys()))
            selected_roll = student_options[selected_student_label]
            
            with st.form("stu_att_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    month = st.selectbox("Month:", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
                with col2:
                    att_days = st.number_input("Days Present:", min_value=0, max_value=31, step=1)
                
                if st.form_submit_button("Save Attendance", type="primary"):
                    success, msg = stu_mgr.add_attendance(selected_roll, month, att_days)
                    if success:
                        st.success(msg)
                        st.session_state.db = load_data()
                    else:
                        st.error(msg)

# --- VIEW 3: TEACHER PORTAL ---
elif menu == "👨‍🏫 Teacher Portal":
    st.markdown('<div class="main-header">👨‍🏫 Teacher Management Portal</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["➕ Register Teacher", "🔍 View Details & Attendance", "📅 Log Attendance"])
    
    # TAB 1: Register
    with tab1:
        st.subheader("Register a New Teacher")
        with st.form("teacher_reg_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *")
                emp_id = st.number_input("Employee ID *", min_value=1, step=1)
            with col2:
                subject = st.text_input("Subject Taught *")
                email = st.text_input("Email Address *")
            
            submitted = st.form_submit_button("Register Teacher", type="primary")
            if submitted:
                if name and subject and email:
                    success, msg = teach_mgr.register(name, subject, emp_id, email)
                    if success:
                        st.success(msg)
                        st.session_state.db = load_data()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill out all required fields.")

    # TAB 2: View Details
    with tab2:
        st.subheader("Search Teacher Record")
        search_id = st.number_input("Enter Employee ID:", min_value=1, step=1)
        if st.button("Search Teacher", type="primary"):
            teacher = teach_mgr.get_details(search_id)
            if teacher:
                st.success(f"Record found for: **{teacher['name']}**")
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Employee ID:** {teacher['employee_id']}")
                    st.write(f"**Subject:** {teacher['subject']}")
                    st.write(f"**Email:** {teacher['email']}")
                with c2:
                    st.write("**Attendance Record:**")
                    st.json(teacher.get("attendance", {}))
            else:
                st.error("No teacher found with that Employee ID.")

    # TAB 3: Attendance
    with tab3:
        st.subheader("Log Teacher Attendance")
        if not db["teachers"]:
            st.warning("Please register a teacher first.")
        else:
            teacher_options = {f"{t['name']} (ID: {t['employee_id']})": t["employee_id"] for t in db["teachers"]}
            selected_teacher_label = st.selectbox("Select Teacher:", list(teacher_options.keys()))
            selected_id = teacher_options[selected_teacher_label]
            
            with st.form("teach_att_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    month = st.selectbox("Month:", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
                with col2:
                    att_days = st.number_input("Days Present:", min_value=0, max_value=31, step=1)
                
                if st.form_submit_button("Save Attendance", type="primary"):
                    success, msg = teach_mgr.add_attendance(selected_id, month, att_days)
                    if success:
                        st.success(msg)
                        st.session_state.db = load_data()
                    else:
                        st.error(msg)