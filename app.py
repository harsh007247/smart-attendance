import streamlit as st
from src.screens.home_Screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.ui.base_layout import style_background_dashboard,style_base_layout,style_background_home

def main():
    style_background_dashboard()
    style_background_home()
    style_base_layout()
    # st.header("this is header")
    # col1,col2=st.columns(2,gap='small')
    # with col1:
    #     name=st.text_input("enter your name")
    #     if st.button("click here" ,type='primary',key='btn1'):
    #         print("hi",name)
    # # st.button("click here" ,type='secondary') by default
    # with col2:
    #     st.button("click here" ,type='tertiary',key='btn2')# key for non-confilct of same type of button

    if 'login_type' not in st.session_state:
        st.session_state['login_type']=None
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()

main()


#     st.markdown("""
#         # Markdown syntax guide

# ## Headers

# # This is a Heading h1
# ## This is a Heading h2
# ###### This is a Heading h6

# ## Emphasis

# *This text will be italic*  
# _This will also be italic_

# **This text will be bold**  
# __This will also be bold__

# _You **can** combine them_

# ## Lists

# ### Unordered

# * Item 1
# * Item 2
# * Item 2a
# * Item 2b
#     * Item 3a
#     * Item 3b

# ### Ordered

# 1. Item 1
# 2. Item 2
# 3. Item 3
#     1. Item 3a
#     2. Item 3b

# ## Images

# ![This is an alt text.](/image/Markdown-mark.svg "This is a sample image.")

# ## Links

# You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

# ## Blockquotes

# > Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
# >
# >> Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

# ## Tables

# | Left columns  | Right columns |
# | ------------- |:-------------:|
# | left foo      | right foo     |
# | left bar      | right bar     |
# | left baz      | right baz     |

# ## Blocks of code

# ```
# let message = 'Hello world';
# alert(message);
# ```

# ## Mermaid diagrams
# ```mermaid
# graph TD
#   A[Start] --> B{Decision}
#   B -->|Yes| C[Finish]
#   B -->|No| D[Alternate]
# ```

# ## Inline code

# This web site is using `markedjs/marked`.

#     """)