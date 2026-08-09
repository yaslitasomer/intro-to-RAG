import streamlit as st
from assistant import create_assistant
from db_save import save_conversation
from db_feedback import save_feedback
from judge import evaluate_relevance
# 1. Configure page settings and tab appearance
st.set_page_config(page_title="Course Assistant", page_icon="📚", layout="centered")

# 2. Cache the assistant resource
@st.cache_resource
def get_assistant():
    return create_assistant()

assistant = get_assistant()

# 3. Modern header design
st.title("📚 RAG Course Assistant")
st.markdown("Ask me anything you want to know about the course!")
st.divider()

# 4. Use session_state to maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display metrics if available
        if "metrics" in message:
            record = message["metrics"]
            st.caption(f"⏱️ **Time:** {record.response_time:.2f}s | 🪙 **Tokens:** {record.prompt_tokens} (P) + {record.completion_tokens} (C) | 💰 **Cost:** ${record.cost:.4f}")
            
        # Display AI Judge evaluation if available
        if "relevance" in message:
            with st.expander("🤖 AI Judge Evaluation"):
                st.write(f"**Relevance:** {message['relevance']}")
                st.write(f"**Explanation:** {message['explanation']}")

# 5. Modern Chat Input
if prompt := st.chat_input("Type your question here..."):
    
    # Display the user's question and save it to history
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get the assistant's answer and metrics
    with st.chat_message("assistant"):
        with st.spinner("Thinking and evaluating..."):
            answer = assistant.rag(prompt)
            st.markdown(answer)
            
            # Retrieve the last call data generated in the background
            record = assistant.last_call
            
            # Save conversation to database
            conversation_id = save_conversation(record, prompt, "llm-zoomcamp")
            st.session_state.conversation_id = conversation_id
            
            # --- AI Judge Evaluation ---
            relevance, explanation = evaluate_relevance(prompt, answer)
            save_feedback(conversation_id, "judge", relevance=relevance, explanation=explanation)
            
            # Display a sleek, single-line metrics bar
            st.caption(f"⏱️ **Time:** {record.response_time:.2f}s | 🪙 **Tokens:** {record.prompt_tokens} (P) + {record.completion_tokens} (C) | 💰 **Cost:** ${record.cost:.4f} | 💾 **Saved ID:** {conversation_id}")
            
            # Display Judge Evaluation in a collapsible box
            with st.expander("🤖 AI Judge Evaluation"):
                st.write(f"**Relevance:** {relevance}")
                st.write(f"**Explanation:** {explanation}")
    
    # Save the assistant's answer, metrics, and judge data to history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": answer,
        "metrics": record,
        "relevance": relevance,
        "explanation": explanation
    })

# 6. User Feedback Mechanism
conversation_id = st.session_state.get("conversation_id")

if conversation_id is not None:
    st.write("---")
    st.markdown("**How was this response?**")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Good (+1)", key=f"feedback_up_{conversation_id}", use_container_width=True):
            save_feedback(conversation_id, "user", score=1)
            st.success("Thanks for your positive feedback!")

    with col2:
        if st.button("👎 Bad (-1)", key=f"feedback_down_{conversation_id}", use_container_width=True):
            save_feedback(conversation_id, "user", score=-1)
            st.warning("Thanks for letting us know, we will improve!")