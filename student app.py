import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="School Result Portal",
    page_icon="🎓",
    layout="centered"
)

FILE_PATH = "School_Result_Portal_1000plus.xlsx"


def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    else:
        columns = [
            "Student ID", "Student Name", "Class",
            "Maths", "English", "Physics", "Chemistry", "Biology",
            "Total", "Average", "Grade"
        ]
        return pd.DataFrame(columns=columns)

def save_data(df):
    df.to_excel(FILE_PATH, index=False)

def calculate_grade(avg):
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 45:
        return "D"
    else:
        return "F"


df = load_data()


st.title("🎓 School Result Portal")
st.write("Check and manage students' academic results")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Check Result", "Add Result", "View All Results"]
)


if menu == "Check Result":
    st.subheader("🔍 Check Student Result")

    student_id = st.text_input("Enter Student ID")

    if st.button("Check Result"):
        if student_id.strip() == "":
            st.warning("Please enter a Student ID")
        else:
            result = df[df["Student ID"].astype(str) == student_id]

            if result.empty:
                st.error("❌ Result not found")
            else:
                st.success("✅ Result found")
                st.table(result)


elif menu == "Add Result":
    st.subheader("➕ Add New Student Result")

    with st.form("add_result_form"):
        student_id = st.text_input("Student ID")
        student_name = st.text_input("Student Name")
        student_class = st.text_input("Class")

        col1, col2 = st.columns(2)

        with col1:
            maths = st.number_input("Maths", 0, 100)
            english = st.number_input("English", 0, 100)
            physics = st.number_input("Physics", 0, 100)

        with col2:
            chemistry = st.number_input("Chemistry", 0, 100)
            biology = st.number_input("Biology", 0, 100)

        submit = st.form_submit_button("Save Result")

    if submit:
        if student_id == "" or student_name == "" or student_class == "":
            st.error("❌ Please fill all fields")
        else:
            total = maths + english + physics + chemistry + biology
            average = round(total / 5, 2)
            grade = calculate_grade(average)

            new_data = {
                "Student ID": student_id,
                "Student Name": student_name,
                "Class": student_class,
                "Maths": maths,
                "English": english,
                "Physics": physics,
                "Chemistry": chemistry,
                "Biology": biology,
                "Total": total,
                "Average": average,
                "Grade": grade
            }

            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df)

            st.success("✅ Result added successfully")


elif menu == "View All Results":
    st.subheader("📊 All Students Results")

    if df.empty:
        st.info("No results available yet")
    else:
        st.dataframe(df, use_container_width=True)


st.markdown("---")
st.caption("© 2026 School Result Portal | Built with Streamlit")
