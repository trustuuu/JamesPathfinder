import streamlit as st
import time

st.set_page_config(
    page_title="Document GPT",
    page_icon="😍"
)
st.title("DocumentGPT")
if "messages" not in st.session_state:
    st.session_state["messages"] = []


def send_message(message, role, save=True):
    with st.chat_message(role):
        st.write(message)
    if save:
        st.session_state["messages"].append({"message": message, "role": role})

for message in st.session_state["messages"]:
    send_message(message["message"], message["role"], save=False)

message = st.chat_input("Send message to the AI")
if message:
    send_message(message, "human")
    time.sleep(2)
    send_message(f"You said: {message}", "ai")

    with st.sidebar:
        st.write(st.session_state)

        
# with st.chat_message("human"):
#     st.write("Hello")

# with st.chat_message("ai"):
#     st.write("How are you?")

# with st.status("Embedding file...", expanded=True) as status:
#     time.sleep(3)
#     st.write("Getting the file")
#     time.sleep(3)
#     st.write("Embedding th e file")
#     time.sleep(3)
#     st.write("Caching the file")
#     status.update(label="Error", state="error")

# st.chat_input("Send message to the AI")