import streamlit as st
from src.database.db import create_subject

@st.dialog("Create a New Subject")
def create_subject_dialogue(teacher_id):
    st.write("Enter the details of new subject")
    sub_id=st.text_input("Subject Code",placeholder="C501")
    sub_name=st.text_input("Subject Name",placeholder="Python")
    sub_section=st.text_input("Section",placeholder="A")

    if st.button("Create Subject Now",type='primary',width='stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id=teacher_id)
                st.toast("Subject Created Succesfully")
            except Exception as e:
                st.error("Error",e)
        else:
            st.warning("Please fill out all the fields")


    