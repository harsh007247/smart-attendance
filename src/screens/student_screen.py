import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

def student_screen():
    style_background_dashboard()
    style_base_layout()
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
    st.camera_input("POSITION YOUR FACE IN THE CENTER")
    footer_dashboard()

    
