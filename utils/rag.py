import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from models.embeddings import get_embedder
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import torch

def load_documents(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext == ".pdf":
        from langchain.document_loaders import PyPDFLoader
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        from langchain.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(file_path)
    elif ext == ".txt":
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file format")
    return loader.load()

def chunk_data(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return text_splitter.split_documents(documents)

def create_vector_store(chunks):
    embedder = get_embedder()
    return FAISS.from_documents(chunks, embedder)

def create_conversation_chain(vector_store, api_key):
    from langchain_perplexity import ChatPerplexity
    llm = ChatPerplexity(pplx_api_key=api_key, model="sonar")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)

def calculate_perplexity(text):
    model_id = "distilgpt2"
    model = GPT2LMHeadModel.from_pretrained(model_id)
    tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
    encodings = tokenizer(text, return_tensors="pt")
    max_len = model.config.n_positions
    stride = 512
    lls = []
    for i in range(0, encodings.input_ids.size(1), stride):
        begin_loc = max(i + stride - max_len, 0)
        end_loc = i + stride
        trg_len = end_loc - i
        input_ids = encodings.input_ids[:, begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100
        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            log_likelihood = outputs.loss * trg_len
        lls.append(log_likelihood)
    ppl = torch.exp(torch.stack(lls).sum() / end_loc)
    return ppl.item()
