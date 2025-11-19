from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from backend.pdf_handler import PDFProcessor
from backend.config import settings

class ChatWithPDF:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.pdf_processor = PDFProcessor(session_id)
        self._llm = None
    
    @property
    def llm(self):
        if self._llm is None:
            # Lazy initialization to avoid loading issues at startup
            self._llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                api_key=settings.GOOGLE_API_KEY,
                temperature=0.7
            )
        return self._llm
        
    def get_answer(self, question: str):
        vectorstore = self.pdf_processor.get_vector_store()
        
        if not vectorstore:
            return {
                "answer": "Please upload a PDF first before asking questions.",
                "sources": []
            }
        
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        result = qa_chain.invoke({"query": question})
        
        sources = [doc.page_content[:200] + "..." for doc in result["source_documents"]]
        
        return {
            "answer": result["result"],
            "sources": sources
        }
