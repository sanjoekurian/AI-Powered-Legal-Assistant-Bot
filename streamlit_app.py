import streamlit as st
import requests
from typing import Dict

# Configure the page
st.set_page_config(
    page_title="Legal Assistant Bot",
    page_icon="⚖️",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        font-size: 18px;
    }
    .stButton>button {
        width: 100%;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("⚖️ Legal Assistant Bot")
st.markdown("""
    Ask questions about Indian legal procedures and get simplified, easy-to-understand answers.
    The bot can help with both litigation and corporate law matters.
""")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input area
query = st.text_input(
    "Enter your legal question:",
    placeholder="e.g., What are the steps involved in filing a lawsuit in India?"
)

# Process question when button is clicked
if st.button("Ask"):
    if query:
        with st.spinner("Processing your question..."):
            try:
                # Make API request
                response = requests.post(
                    "http://localhost:8000/ask",
                    json={"question": query}
                )
                
                if response.status_code == 200:
                    answer = response.json()["response"]
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": query,
                        "answer": answer
                    })
                else:
                    st.error("Sorry, there was an error processing your question.")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the API server. Please make sure it's running.")
    else:
        st.warning("Please enter a question.")

# Display chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("Previous Questions")
    
    for item in reversed(st.session_state.chat_history):
        with st.expander(f"Q: {item['question']}"):
            st.markdown(f"**A:** {item['answer']}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Powered by Groq's LLaMA3-70B and LangChain</p>
    </div>
""", unsafe_allow_html=True) 