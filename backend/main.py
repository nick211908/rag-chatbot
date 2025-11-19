from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
from backend.models import UserSignup, UserLogin, ChatRequest, ChatResponse
from backend.auth import signup_user, login_user, verify_token
from backend.pdf_handler import PDFProcessor
from backend.chat import ChatWithPDF
from backend.session_manager import session_manager

app = FastAPI(title="PDF Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "PDF Chat API is running"}

@app.post("/api/auth/signup")
async def signup(user: UserSignup):
    result = await signup_user(user.email, user.password)
    return {
        "message": "User created successfully",
        "user": result["user"],
        "session": result["session"]
    }

@app.post("/api/auth/login")
async def login(user: UserLogin):
    result = await login_user(user.email, user.password)
    return {
        "message": "Login successful",
        "access_token": result["access_token"],
        "user": result["user"],
        "user_id": result["user_id"]
    }

@app.post("/api/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user = Depends(verify_token)
):
    if not file.filename or not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    session_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{session_id}.pdf")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    processor = PDFProcessor(session_id)
    result = processor.process_pdf(file_path)
    
    session_manager.create_session(session_id, user["id"], file.filename)
    
    return {
        "session_id": session_id,
        "filename": file.filename,
        **result
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    user = Depends(verify_token)
):
    if not session_manager.verify_ownership(chat_request.session_id, user["id"]):
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this session"
        )
    
    chat_handler = ChatWithPDF(chat_request.session_id)
    result = chat_handler.get_answer(chat_request.question)
    
    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"]
    )

@app.get("/api/sessions")
async def get_user_sessions(user = Depends(verify_token)):
    sessions = session_manager.get_user_sessions(user["id"])
    return {"sessions": sessions}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
