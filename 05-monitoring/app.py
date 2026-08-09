import streamlit as st
from assistant import create_assistant

# 1. Configure page settings and tab appearance
st.set_page_config(page_title="Course Assistant", page_icon="📚", layout="centered")

# 2. Cache the assistant resource
# This prevents the assistant model from reloading on every interaction, significantly improving speed.
@st.cache_resource
def get_assistant():
    return create_assistant()

assistant = get_assistant()

# 3. Modern header design
st.title("📚 RAG Course Assistant")
st.markdown("Ask me anything you want to know about the course!")
st.divider()

# 4. Use session_state to maintain chat history
# Streamlit reruns the script on every interaction, so we store the history here to prevent it from being erased.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages on the screen (with User and Assistant avatars)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Modern Chat Input (A sleek combination of text box and button)
if prompt := st.chat_input("Type your question here..."):
    
    # Display the user's question and save it to history
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get the assistant's answer with a loading animation
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = assistant.rag(prompt)
            st.markdown(answer)
    
    # Save the assistant's answer to history as well
    st.session_state.messages.append({"role": "assistant", "content": answer})