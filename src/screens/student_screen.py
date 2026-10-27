import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipeline.face_pipeline import predict_attendance,get_all_students,getface_embeddings,train_classifier
from src.pipeline.voice_pipeline import get_voice_embedding
from src.database.db import create_student,get_student_attendance,get_students_subjects,unenroll_students_to_subject
from src.components.dialogue_enroll import enroll_dialogue
from src.components.subject_card import subject_card

import numpy as np
from PIL import Image
import time



def student_dashboard():
    student_data=st.session_state.student_data
    student_id=student_data['student_id']
    c1,c2= st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"welcome Back {student_data['name']}")
        if st.button('Logout',type='secondary',key='loginbackbin',shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1,c2=st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll In subject",type='primary',width='stretch'):
            enroll_dialogue()
    st.divider()

    with st.spinner("Loading Your enrolled subjects"):
        subjects=get_students_subjects(student_id)
        logs=get_student_attendance(student_id)
    stats_map={}
    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']


        stats = stats_map.get(sid,{"total":0, "attended": 0} )
        def unenroll_button():
                if st.button("Unenroll from tihs course", type='tertiary', width='stretch', icon=':material/delete_forever:'):
                    unenroll_students_to_subject(student_id, sid)
                    st.toast(f'Unenrolled from {sub['name']} successfully!')
                    st.rerun()

        with cols[i % 2]:

            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()
def student_screen():
    show_registration=False
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    c1,c2= st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',type='secondary',key='loginbackbin',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()

    st.space()
    st.space()
    st.header("Login Using Face ID",text_alignment='center')
    photo_source=st.camera_input("POSITION YOUR FACE IN THE CENTER")
    if photo_source:
        img= np.array(Image.open(photo_source))
        with st.spinner("AI is Scanning"):
            detected,all_ids,num_faces=predict_attendance(img)
            if num_faces==0:
                st.warning("face not Found")
            elif num_faces>1:
                st.warning("Multiple faces found")
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()
                    student= next((s for s in all_students if s['student_id']==student_id),None)

                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role='student'
                        st.session_state.student_data=student
                        st.toast(f"Welcome Back {student['name'] }👏")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.info("face nnot recognizerd! may be you are new")
                    show_registration=True
    if show_registration:
        with st.container(border=True):
            st.header("REGISTER NEW PROFILE") 
            new_name=st.text_input("enter your name")
            st.subheader("optional: Voice enrollment")
            st.info("enroll your voice for attendance")
            audio_data=None

            try:
                audio_data=st.audio_input("record a short phrase like I am a Present, My name is Harsh")
            except Exception:
                st.error("audio recording failed")

            if st.button("create Account",type='primary'):
                if new_name:
                    with st.spinner("creating profile.."):
                        img=np.array(Image.open(photo_source))
                        encodings=getface_embeddings(img)
                        if encodings:
                            face_emd=encodings[0].tolist()

                            voice_emb=None
                            if audio_data:
                                voice_emd=get_voice_embedding(audio_data.read())
                            response_data= create_student(new_name,face_embedding=face_emd,voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role='student'
                                st.session_state.student_data=response_data[0]
                                st.toast(f"profile Created ,HI {new_name}")
                                time.sleep(2)
                                st.rerun()
                        else:
                            st.error("Couldn't Capture Your Facial Recognition ")


                else:
                    st.warning("please enter your name")


    footer_dashboard()

    
