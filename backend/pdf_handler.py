import os
from typing import List
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from backend.config import settings

class PDFProcessor:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._embeddings = None
        self.persist_directory = f"{settings.CHROMA_DB_PATH}/{session_id}"
    
    @property
    def embeddings(self):
        if self._embeddings is None:
            if not settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not configured in environment")
            self._embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                api_key=settings.GOOGLE_API_KEY
            )
        return self._embeddings
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        pdf_reader = PdfReader(pdf_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    def split_text(self, text: str) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]
        return documents
    
    def create_vector_store(self, documents: List[Document]):
        if not documents:
            raise ValueError("No documents to process")
        os.makedirs(self.persist_directory, exist_ok=True)
        try:
            vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            return vectorstore
        except Exception as e:
            print(f"Error creating vector store: {str(e)}")
            raise
    
    def get_vector_store(self):
        if not os.path.exists(self.persist_directory):
            return None
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
    
    def process_pdf(self, pdf_path: str):
        text = self.extract_text_from_pdf(pdf_path)
        if not text or len(text.strip()) == 0:
            raise ValueError("PDF appears to be empty or unable to extract text")
        
        documents = self.split_text(text)
        if not documents:
            raise ValueError("No text chunks created from PDF")
        
        print(f"Processing PDF with {len(documents)} chunks")
        vectorstore = self.create_vector_store(documents)
        return {
            "status": "success",
            "chunks": len(documents),
            "message": "PDF processed successfully"
        }
