import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import json
import base64
import streamlit as st

CHAT_HISTORY_FILE = "chat_history.json"
os.environ["GOOGLE_API_KEY"] = "AIzaSyBk3TaNDDFBN52nOj3Q01JNRWC8tm0KEFU"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Clear chat history at the start of each session
def clear_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)

# Initialize session state for chat
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            data = json.load(file)
            return data.get('chat_history', [])
    return []

def save_chat_history(chat_history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump({"chat_history": chat_history}, file)

# Extract text from a PDF
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        text_pages = []
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            text_pages.append((os.path.basename(file_path), page_num + 1, text))
    return text_pages

# Split text into chunks
def get_text_chunks_and_metadata(text_pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks_metadata = []
    for file_name, page_num, text in text_pages:
        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            chunks_metadata.append({"text": chunk, "metadata": {"title": file_name, "page_number": page_num}})
    return chunks_metadata

# Generate a vector store from the chunks
def get_vector_store(chunks_metadata):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    texts = [chunk["text"] for chunk in chunks_metadata]
    metadatas = [chunk["metadata"] for chunk in chunks_metadata]
    vector_store = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)
    vector_store.save_local("faiss_index")

# Generate conversational chain for question answering
def get_conversational_chain():
    prompt_template = """
        You are an intelligent assistant with access to a detailed context. Your task is to answer the user's question strictly based on the provided context.
        If the context does not contain relevant information to answer the question, respond with:
        "Sorry, I don't have the information you're looking for. Please contact our team for further assistance via phone at +91 9263283565 or email at Genillect@gmail.com."
        If user greet you with hi or hello,respond with:
        "Hello sir welcome to Genillect, how can I help you"

        Use the history to maintain context in your responses
        
        If user greet you with thanks for help,thanks,thank you,It was helpfull,so repond with:
        You're welcome, Sir! I'm glad I could help. If you need further assistance, feel free to reach out.😊

        When answering questions about processes or procedures, provide detailed steps based solely on the context.

        Context:\n{context}\n
        Question:\n{question}\n 
        Generate a response based solely on the context above. Do not generate any response that is not grounded in the context.
    """.strip()

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Get answer to the user's question using the chatbot logic
def get_answer(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question, k=15)

    chain = get_conversational_chain()
    
    context = ""
    input_documents = []
    for doc in docs:
        context += doc.page_content + "\n"
        input_documents.append(doc)

    response = chain({"input_documents": input_documents, "context": context, "question": user_question})
    answer_text = response.get('output_text', "The answer is not available in the context").strip()

    return answer_text


 

