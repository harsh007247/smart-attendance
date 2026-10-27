import streamlit as st
import time
from src.database.config import supabase
from src.database.db import create_subject

@st.dialog("Create a New Subject")
def create_subject_dialogue(teacher_id):
    st.write("Enter the details of new subject")
    sub_id=st.text_input("Subject Code",placeholder="C501")
    sub_name=st.text_input("Subject Name",placeholder="Python")
    sub_section=st.text_input("Section",placeholder="A")

    if st.button("Create Subject Now",type='primary',width='stretch'):
        if sub_id and sub_name and sub_section:
            clean_code = sub_id.strip()
            existing = supabase.table('subjects').select('subject_id').eq('subject_code', clean_code).execute()
            if existing.data:
                st.error(f"Subject Code '{clean_code}' already exists! Please use a unique code.")
            else:
                try:
                    create_subject(clean_code,sub_name.strip(),sub_section.strip(),teacher_id=teacher_id)
                    st.toast("Subject Created Succesfully")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please fill out all the fields")


    