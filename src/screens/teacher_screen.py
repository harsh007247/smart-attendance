import streamlit as st
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import teacher_check_exist,create_teacher,teacher_login

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
    st.header("welcome Back!")

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
                st.erorr("Invalid Username")


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


