import os
import sys
import streamlit as st

# Try to get API key from Streamlit Cloud secrets
try:
    PPLX_API_KEY = st.secrets["PPLX_API_KEY"]
except Exception:
    # Fallback to local .env for development
    from dotenv import load_dotenv
    load_dotenv()
    PPLX_API_KEY = os.getenv('PPLX_API_KEY', '')

# Set up paths for imports based on project structure
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'models')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))

from models.llm import get_llm_model
from utils.rag import (
    load_documents,
    chunk_data,
    create_vector_store,
    create_conversation_chain,
    calculate_perplexity,
)
from utils.websearch import web_search  # live web search fallback

def instructions_page():
    st.title("The Chatbot Blueprint")
    st.markdown("""
    ## Setup & Usage

    1. Put your API key in the `.env` file as `PPLX_API_KEY`.
    2. Upload any car manual document directly.
    3. Switch between Concise/Detailed replies in the sidebar.
    4. The bot will use uploaded docs or live web search as fallback.

    ---  
    """)

def chat_page():
    st.title("🤖 Intelligent RAG Car Manual ChatBot")
    mode = st.sidebar.radio("Response Mode:", ("Concise", "Detailed"), 1)
    uploaded_file = st.sidebar.file_uploader("Upload a file (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chain" not in st.session_state:
        st.session_state.chain = None
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    # Process uploaded document
    if uploaded_file:
        file_path = f"./uploaded_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        try:
            docs = load_documents(file_path)
            chunks = chunk_data(docs)
            st.session_state.vector_store = create_vector_store(chunks)
            st.session_state.chain = create_conversation_chain(st.session_state.vector_store, PPLX_API_KEY)
            st.success("File indexed for retrieval.")
        except Exception as e:
            st.error(f"Error processing document: {e}")

    llm_model = get_llm_model(PPLX_API_KEY)

    # Display existing chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask me anything about your docs, or just chat...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                response = ""
                source = ""
                try:
                    if st.session_state.chain:
                        history_pairs = [(m["content"], "") for m in st.session_state.messages if m["role"] == "user"]
                        out = st.session_state.chain({"question": prompt, "chat_history": history_pairs})
                        response = out.get("answer", "")
                        source = "Document"
                    else:
                        response = web_search(prompt)
                        source = "Web Search"
                    ppl = calculate_perplexity(response)
                except Exception as e:
                    response = f"Error generating response: {e}"
                    ppl = -1

                if mode == "Concise" and len(response) > 250:
                    response = response[:250] + "..."

                display_response = (
                    f"{response}\n\n_Source: {source}_\n🔢 *Perplexity:* {ppl:.2f}" if ppl >= 0 else f"{response}\n\n_Source: {source}_"
                )
                st.markdown(display_response)

                st.session_state.messages.append({"role": "assistant", "content": display_response})

def main():
    st.set_page_config(page_title="Intelligent RAG Car Manual ChatBot", page_icon="🤖", layout="wide")
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to:", ["Chat", "Instructions"], 0)
        st.divider()
        if page == "Chat":
            if st.button("🗑️ Clear Chat History"):
                st.session_state.messages = []
                st.experimental_rerun()

    if page == "Instructions":
        instructions_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()
