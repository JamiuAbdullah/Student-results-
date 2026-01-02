import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="School Result Portal",
    page_icon="🎓",
    layout="centered"
)

FILE_PATH = "School_Result_Portal_1000plus.xlsx"

# -------------------------
# Load and Save Functions
# -------------------------
def load_data():
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_excel(FILE_PATH)
        except ImportError:
            st.error("❌ Missing library `openpyxl`. Add it to requirements.txt and redeploy.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error loading Excel file: {e}")
            st.stop()
    else:
        columns = [
            "student id", "full_name", "class", "arm", "gender", "date_of_birth",
            "maths", "english", "physics", "chemistry", "biology",
            "total", "average", "grade"
        ]
        df = pd.DataFrame(columns=columns)

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\u00A0", "")
        .str.lower()
    )

    # Normalize student_id → student id
    if "student_id" in df.columns:
        df.rename(columns={"student_id": "student id"}, inplace=True)

    return df

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

# -------------------------
# Load Data
# -------------------------
df = load_data()

# -------------------------
# UI
# -------------------------
st.title("🎓 School Result Portal")
st.write("Check and manage students' academic results")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Check Result", "Add Result", "Update Result", "Delete Result", "View All Results"]
)

# -------------------------
# CHECK RESULT
# -------------------------
if menu == "Check Result":
    st.subheader("🔍 Check Student Result")

    student_id_input = st.text_input("Enter Student ID").strip().lower()

    if st.button("Check Result"):
        student_ids = df["student id"].astype(str).str.strip().str.lower()
        result = df[student_ids == student_id_input]

        if result.empty:
            st.error("❌ Result not found")
        else:
            st.success("✅ Result found")

            # -------- STUDENT PROFILE --------
            profile_fields = [
                "student id", "full_name", "class",
                "arm", "gender", "date_of_birth"
            ]
            profile_fields = [f for f in profile_fields if f in result.columns]

            profile = result[profile_fields].iloc[0].to_frame()
            profile.columns = ["Value"]
            profile.index = profile.index.str.replace("_", " ").str.title()

            st.subheader("👤 Student Profile")
            st.table(profile)

            # -------- ACADEMIC PERFORMANCE (SAFE FIX) --------
            all_possible_scores = [
                "maths", "english", "physics",
                "chemistry", "biology",
                "total", "average", "grade"
            ]

            score_fields = [c for c in all_possible_scores if c in result.columns]

            if score_fields:
                result[score_fields] = result[score_fields].fillna(0)

                scores = result[score_fields].iloc[0].to_frame()
                scores.columns = ["Score"]
                scores.index = scores.index.str.replace("_", " ").str.title()

                st.subheader("📊 Academic Performance")
                st.table(scores)
            else:
                st.warning("⚠ No academic performance recorded for this student yet.")

# -------------------------
# ADD RESULT
# -------------------------
elif menu == "Add Result":
    st.subheader("➕ Add New Student Result")

    with st.form("add_result_form"):
        student_id = st.text_input("Student ID")
        full_name = st.text_input("Full Name")
        student_class = st.text_input("Class")
        arm = st.text_input("Arm")
        gender = st.selectbox("Gender", ["Male", "Female"])
        date_of_birth = st.date_input("Date of Birth")

        maths = st.number_input("Maths", 0, 100)
        english = st.number_input("English", 0, 100)
        physics = st.number_input("Physics", 0, 100)
        chemistry = st.number_input("Chemistry", 0, 100)
        biology = st.number_input("Biology", 0, 100)

        submit = st.form_submit_button("Save Result")

    if submit:
        total = maths + english + physics + chemistry + biology
        average = round(total / 5, 2)
        grade = calculate_grade(average)

        new_data = {
            "student id": student_id,
            "full_name": full_name,
            "class": student_class,
            "arm": arm,
            "gender": gender,
            "date_of_birth": date_of_birth,
            "maths": maths,
            "english": english,
            "physics": physics,
            "chemistry": chemistry,
            "biology": biology,
            "total": total,
            "average": average,
            "grade": grade
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        save_data(df)
        st.success("✅ Result added successfully")

# -------------------------
# UPDATE RESULT
# -------------------------
elif menu == "Update Result":
    st.subheader("✏️ Update Student Result")

    student_id_input = st.text_input("Enter Student ID").strip().lower()
    student_ids = df["student id"].astype(str).str.strip().str.lower()
    result = df[student_ids == student_id_input]

    if not result.empty:
        student = result.iloc[0]

        maths = st.number_input("Maths", 0, 100, int(student.get("maths", 0)))
        english = st.number_input("English", 0, 100, int(student.get("english", 0)))
        physics = st.number_input("Physics", 0, 100, int(student.get("physics", 0)))
        chemistry = st.number_input("Chemistry", 0, 100, int(student.get("chemistry", 0)))
        biology = st.number_input("Biology", 0, 100, int(student.get("biology", 0)))

        if st.button("Update Result"):
            total = maths + english + physics + chemistry + biology
            average = round(total / 5, 2)
            grade = calculate_grade(average)

            df.loc[result.index, [
                "maths", "english", "physics",
                "chemistry", "biology",
                "total", "average", "grade"
            ]] = [
                maths, english, physics,
                chemistry, biology,
                total, average, grade
            ]

            save_data(df)
            st.success("✅ Result updated successfully")
    else:
        st.info("Enter a valid Student ID to update")

# -------------------------
# DELETE RESULT
# -------------------------
elif menu == "Delete Result":
    st.subheader("🗑 Delete Student Result")

    student_id_input = st.text_input("Enter Student ID to delete").strip().lower()

    if st.button("Delete"):
        student_ids = df["student id"].astype(str).str.strip().str.lower()

        if student_id_input in student_ids.values:
            df = df[student_ids != student_id_input]
            save_data(df)
            st.success("✅ Student result deleted successfully")
        else:
            st.error("❌ Student ID not found")

# -------------------------
# VIEW ALL RESULTS
# -------------------------
elif menu == "View All Results":
    st.subheader("📊 All Students Results")

    if df.empty:
        st.info("No results available yet")
    else:
        st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("© 2026 School Result Portal | Built with Streamlit")    # Normalize student_id → student id
    




