import streamlit as st


def footer_home():
    logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-_7UypXkU0xPhXrjlDHA21iXMH5NVrvB2H--oquNGqA&s"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:white;"> Created with ❤️ by </p>  
        <img src='{logo_url}' style='max-height:25px' />
        </div>
                
                """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-_7UypXkU0xPhXrjlDHA21iXMH5NVrvB2H--oquNGqA&s"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
        <p style="font-weight:bold; color:black;"> Created with ❤️ by </p>  
        <img src='{logo_url}' style='max-height:25px' />
        </div>
                
                """, unsafe_allow_html=True)