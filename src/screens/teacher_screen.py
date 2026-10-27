import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import teacher_check_exist,create_teacher,teacher_login,get_teacher_subjects
from src.components.dialogue_create_subject import create_subject_dialogue
from src.components.dialogue_share_subject import share_subject_dialogue
from src.components.subject_card import subject_card
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=='Login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_Register()

def teacher_dashboard():
    """
        # FLOW BETWEEN teacher_screen() AND teacher_dashboard()
        #
        # 1. After successful teacher login, teacher's data is stored in:
        #    st.session_state["teacher_data"] = teacher_data
        #
        # 2. In teacher_screen(), this condition checks whether the
        #    "teacher_data" key exists in session_state:
        #    if "teacher_data" in st.session_state:
        #
        # 3. If the key exists, teacher_dashboard() is called.
        #
        # 4. Inside teacher_dashboard(), we retrieve the stored data:
        #    teacher_data = st.session_state.teacher_data
        #
        # 5. Now we can use teacher_data to access teacher details,
        #    such as name, email, or ID, and display the dashboard.
        #
        # IMPORTANT:
        # - teacher_screen() decides WHICH screen to display.
        # - teacher_dashboard() displays the teacher's dashboard.
        # - Both functions are connected through st.session_state.
        # - The key must be created during login before accessing its value.
    """
    teacher_data=st.session_state.teacher_data
    teacher_name=st.session_state.teacher_data["username"]
    c1,c2= st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"welcome Back {teacher_name}")
        if st.button('Logout',type='secondary',key='loginbackbin',shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()
    st.space()        
    st.space() 

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab="take_attendance"

    tab1, tab2, tab3= st.columns(3)
    with tab1:
        type1="primary" if st.session_state.current_teacher_tab=="take_attendance" else "tertiary"
        if st.button("Take Attendance",type=type1,width='stretch',icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab="take_attendance"
            st.rerun()
    with tab2:
        type2="primary" if st.session_state.current_teacher_tab=="manage_subjects" else "tertiary"
        if st.button("Manage Subjects",type=type2,width='stretch',icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab="manage_subjects"
            st.rerun()
    with tab3:
        type3="primary" if st.session_state.current_teacher_tab=="attendance_records" else "tertiary"
        if st.button("Attendance Records",type=type3,width='stretch',icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab="attendance_records"
            st.rerun()
    st.divider()

    if st.session_state.current_teacher_tab=="take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab=="manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab=="attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()

def teacher_tab_take_attendance():
    st.header("Take AI attendance")
def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    c1,c2=st.columns(2)
    with c1:
        st.header("manage subjects")
    with c2:
        if st.button("Create New Subject",width='stretch'):
            create_subject_dialogue(teacher_id)

    #list all subjects

    subjects=get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats=[
                ("👥","STUDENTS",sub["total_students"]),
                ("🎒","CLASSES",sub["total_classes"])
            ]
        def share_btn():
            if st.button(f"Share Code {sub["name"]}",key=f"share__{sub["subject_code"]}",icon=":material/share:"):
                share_subject_dialogue(sub["name"],sub["subject_code"])
            st.space()

        subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")

def teacher_tab_attendance_records():
    st.header("attendane records")

def login_teacher(username,password):
    if not username or not password:
        return False

    teacher=teacher_login(username,password)
    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.islogged_in=True
        return True
    return False





def teacher_screen_login():
    c1,c2= st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',type='secondary',key='loginbackbin',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()


    st.header("Login Using Password",text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Enter Username",placeholder='harsh001')
    teacher_password=st.text_input("Enter Password",type='password',placeholder="Enter Password")
    st.divider()

    btcn1,btcn2=st.columns(2)
    with btcn1:
        if st.button('Login',icon=":material/passkey:", shortcut="control+enter",width='stretch'):
            if login_teacher(teacher_username,teacher_password):
                st.toast(f"Welcome Back! {teacher_username}",icon="👏")
                import time
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid Username")


    with btcn2:
        if st.button('Register Instead',type="primary",icon=":material/passkey:",width='stretch'):
            st.session_state.teacher_login_type='register'



    footer_dashboard()
def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "ALL FIELDS ARE REQUIRED"
    if teacher_check_exist(teacher_username):
        return False,'Username already taken'
    if teacher_pass!=teacher_pass_confirm:
        return False ,"Password don't match"
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,'succesfully Created ! Login Now'
    except Exception as e:
        return False,"unexpected error occur"

    
    
     
    
def teacher_screen_Register():
    c1,c2= st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button('Go back to Home',type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()

    st.header("Register Your Profile",text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Enter Username",placeholder='harsh001')
    teacher_name=st.text_input("Enter Your name",placeholder='harsh')
    teacher_password=st.text_input("Enter Password",type='password',placeholder="Enter Password")
    teacher_password_confirm=st.text_input("Confirm Password",type='password',placeholder="Confirm Your Password")
    st.divider()

    btcn1,btcn2=st.columns(2)
    with btcn1:
        if st.button('Register',icon=":material/passkey:", shortcut="control+enter",width='stretch'):
            success,message=register_teacher(teacher_username,teacher_name,teacher_password,teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type='Login'
                st.rerun()
            else:
                st.error(message)
    with btcn2:
        if st.button('Login Instead',type="primary",icon=":material/passkey:",width='stretch'):
            st.session_state.teacher_login_type='Login'
            st.rerun()



    footer_dashboard()


