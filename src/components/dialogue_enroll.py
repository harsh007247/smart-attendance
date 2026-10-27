import streamlit as st
import time
from src.database.config import supabase
from src.database.db import enroll_students_to_subject

@st.dialog("Enroll In Subject")
def enroll_dialogue():
    st.write("Enter The Subject Code provided By Your Teacher To Enroll")
    join_code= st.text_input("Subject Code",placeholder="IT101")
    if st.button("Enroll Now",type="primary",width='stretch'):

        if join_code:
            res= supabase.table('subjects').select('subject_id , name, subject_code').eq('subject_code',join_code).execute()
            if res:
                subject=res.data[0]
                student_id=st.session_state.student_data["student_id"]
            check= supabase.table('subject_students').select('*').eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
            if check.data:
                st.warning("You Are Already Enrolled In This Program")
            else:
                enroll_students_to_subject(student_id,subject['subject_id'])
                st.success("Succesfully Enrolled")
                time.sleep(1)
                st.rerun()
        else:
            st.warning("Please Enter a Subject Code")





    