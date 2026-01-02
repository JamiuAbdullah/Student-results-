import pandas as pd
import streamlit as st

FILE_PATH = "School_Result_Portal_1000plus.xlsx"  

def load_data():
    try:
        return pd.read_excel(FILE_PATH)
    except ImportError as e:
        st.error("Error: Missing required library `openpyxl` to read Excel files.\n"
                 "Please install it by adding `openpyxl` to your requirements.txt.")
        st.stop()  
    except FileNotFoundError:
        st.error(f"Error: Excel file not found at path: {FILE_PATH}")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.stop()

df = load_data()

st.write("Data loaded successfully!")
st.dataframe(df)
