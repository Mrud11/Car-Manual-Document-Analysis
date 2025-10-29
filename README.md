# Intelligent RAG ChatBot for Car Manual Documents

A Streamlit-powered AI chatbot that performs Retrieval Augmented Generation (RAG) over uploaded Car Manual documents and uses live web search fallback (DuckDuckGo) for out-of-document queries. It integrates Perplexity LLM for confident answering, supports concise/detailed response modes, and is designed for easy extension.

---

## Features

- **Streamlit Web UI:** Simple, modern interface for chat and interaction.
- **Document-based QA:** Upload PDF, DOCX, or TXT and ask questions about their content.
- **RAG pipeline:** Uses fast embeddings and FAISS for retrieval.
- **Web Search Fallback:** Integrates DuckDuckGo via LangChain for real-time web answers.
- **Flexible LLM Support:** Built-in Perplexity integration, easy to extend with other LLMs.
- **Response Modes:** Switch between Concise or Detailed answers.
- **Perplexity Score:** Shows confidence of generated answers.

---

## Project Structure

project/
├── app.py
├── .env
├── requirements.txt
├── models/
│ ├── init.py
│ ├── embeddings.py
│ └── llm.py
├── utils/
│ ├── init.py
│ ├── rag.py
│ └── websearch.py

---

## Setup & Installation

1. **Clone this repository**
git clone <your-repo-url>
cd <your-project-folder>


2. **Create `.env` in the project root:**
PPLX_API_KEY=your_perplexity_api_key_here


3. **Install dependencies**
pip install -r requirements.txt


4. **(Optional) Place your documents in the folder or upload via UI**

---

## Usage

streamlit run app.py

- Use the sidebar to navigate and configure response mode.
- Upload your document (PDF, DOCX, TXT).
- Chat about your document or ask anything; the bot falls back to web search if needed.
- See the response along with the source (Document/Web Search) and Perplexity score.

---

## Requirements

See `requirements.txt` for dependencies. Key packages:
- streamlit
- python-dotenv
- langchain
- transformers
- torch
- faiss-cpu
- sentence-transformers
- duckduckgo-search
- ddgs
- langchain-perplexity

---

## Technologies Used

- [LangChain](https://python.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Perplexity LLM](https://www.perplexity.ai/)
- [DuckDuckGo Search](https://duckduckgo.com/)
- FAISS, HuggingFace Embeddings, PyPDFLoader, Docx2txt

---

## Contributing

Pull requests welcome! For major changes, please open an issue first.

---

## License

Specify your license here, e.g. MIT.

---

## Author

If any doubts or questions please contact me at email: [r.mrudula27@gmail.com](mailto:r.mrudula27@gmail.com)

