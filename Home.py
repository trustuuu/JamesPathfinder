import streamlit as st

st.set_page_config(
    page_title="",
    page_icon="😍"
)
st.title("Home AI with langchain")
st.subheader("""
            #Hello!
             Welcome James' FullStack GPT Portfolio!

             Here are the apps I made:
            
            - [ ] [DocumentGPT](/DocumentGPT)
            - [ ] [PrivateGPT](/PrivateGPT)
            - [ ] [QuizGPT](/QuizGPT)
            - [ ] [SiteGPT](/SiteGPT)
            - [ ] [MeetingGPT](/MeetingGPT)
            - [ ] [InvestorGPT](/InvestorGPT)
                        
             """)


# with st.sidebar:
#     st.selectbox("Choose Dic", ("Eng", "Jan"))
#     tab_one, tab_two, tab_three = st.tabs(["Crawing", "Chatbot", "Quiz"])

#     with tab_one:
#         st.write("this is A tab")

#     with tab_two:
#         st.write("this is B tab")

#     with tab_three:
#         st.write("this is C tab")