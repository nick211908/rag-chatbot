# PDF Chat Web Application

## Overview
A full-stack web application that allows users to upload PDF documents and chat with them using AI. Built with FastAPI (Python) backend, React frontend, LangChain for PDF processing, ChromaDB for vector embeddings, and Supabase for authentication.

## Recent Changes
- **November 18, 2025**: Initial project setup and security improvements
  - Created FastAPI backend with authentication endpoints using Supabase
  - Implemented PDF upload and processing with ChromaDB vector storage
  - Built chat endpoint using LangChain and OpenAI GPT-5 for RAG (Retrieval Augmented Generation)
  - Created React frontend with Vite
  - Implemented authentication UI (Login and Signup)
  - Built PDF upload and chat interface
  - Configured workflows for both backend and frontend servers
  - **Security improvements**:
    - Fixed async/await for Supabase calls using asyncio.to_thread()
    - Implemented secure JWT token verification with signature validation
    - Added user ownership tracking for PDF sessions
    - Added session persistence in frontend using localStorage

## Project Architecture

### Backend (FastAPI)
- **Location**: `/backend` directory
- **Main Components**:
  - `main.py`: FastAPI application with API endpoints
  - `auth.py`: Supabase authentication (signup, login, token verification with JWT)
  - `session_manager.py`: User session ownership tracking and validation
  - `pdf_handler.py`: PDF processing and ChromaDB vector storage
  - `chat.py`: LangChain-based chat with RAG using OpenAI GPT-5
  - `models.py`: Pydantic models for request/response validation
  - `config.py`: Configuration management
- **Port**: 8000
- **Key Dependencies**: FastAPI, Uvicorn, ChromaDB, PyPDF2, Supabase, LangChain, OpenAI, PyJWT

### Frontend (React + Vite)
- **Location**: `/frontend` directory
- **Main Components**:
  - `src/App.jsx`: Main app with routing
  - `src/components/Login.jsx`: Login page
  - `src/components/Signup.jsx`: Signup page
  - `src/components/Chat.jsx`: PDF upload and chat interface
  - `src/api.js`: API client with Axios
  - `src/config.js`: Frontend configuration
- **Port**: 5000
- **Key Dependencies**: React, React Router DOM, Axios, Vite

### Authentication
- **Provider**: Supabase
- **Features**: User signup, login, JWT token-based authentication
- **Protected Routes**: PDF upload and chat require authentication

### Vector Storage
- **Database**: ChromaDB
- **Purpose**: Store PDF embeddings for semantic search
- **Embeddings**: OpenAI embeddings
- **Location**: `./chroma_db` directory (one folder per session)

### AI Model
- **Provider**: OpenAI
- **Model**: GPT-5 (released August 7, 2025)
- **Use Cases**: 
  - Generate embeddings from PDF chunks
  - Answer questions about PDF content using RAG

## Setup Instructions

### Required Environment Variables
Create a `.env` file in the root directory with:
```
GOOGLE_API_KEY=your_google_ai_studio_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
```

**Finding your Supabase credentials:**
1. Go to your Supabase project dashboard
2. Navigate to Settings > API
3. Copy the Project URL for `SUPABASE_URL`
4. Copy the anon/public key for `SUPABASE_KEY`
5. Copy the JWT Secret for `SUPABASE_JWT_SECRET`

**Note:** The JWT secret is required for secure token verification. If not provided, the app will fall back to using Supabase's get_user API method.

### Running the Application
The application uses two workflows:
1. **Frontend**: Runs Vite dev server on port 5000
2. **Backend**: Runs Uvicorn server on port 8000

Both workflows are configured to start automatically.

## How to Use

1. **Sign Up**: Create an account on the signup page
2. **Login**: Sign in with your credentials
3. **Upload PDF**: Select and upload a PDF file
4. **Chat**: Ask questions about the PDF content
5. **AI Responses**: Get answers based on the PDF content with source citations

## User Preferences
- Uses TypeScript/JavaScript for frontend
- Uses Python for backend
- Prefers modern, clean UI design
- Needs real-time chat functionality with AI

## Technical Notes
- Frontend uses Vite with `allowedHosts: true` for Replit compatibility
- Backend configured to bind to `0.0.0.0` for proper network access
- PDFs are processed into chunks for better context retrieval
- Each upload session gets a unique ID for isolated vector storage
- Session ownership is tracked per user to prevent unauthorized access
- JWT tokens are verified with signature validation for security
- Frontend persists session ID and chat history in localStorage
- Supabase calls use asyncio.to_thread() for proper async handling

## Security Features
- Secure JWT token verification with signature validation
- User ownership tracking for PDF sessions
- Protected API endpoints requiring authentication
- Session validation to prevent unauthorized access to other users' PDFs
- Automatic token expiry checking
