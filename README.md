# RAG ChatBot with PDF Processing

A full-stack AI-powered chatbot that allows users to upload PDF documents and ask questions about their content using Retrieval-Augmented Generation (RAG).

## Features

- User authentication (signup/login)
- PDF upload and processing
- AI-powered chat with PDF content
- Vector database storage for efficient retrieval
- Real-time chat interface
- Session management

## Tech Stack

### Backend
- Python 3.11
- FastAPI (web framework)
- LangChain (LLM integration)
- Google Generative AI (embedding model)
- ChromaDB (vector database)
- Supabase (user authentication)
- PyPDF2 (PDF processing)

### Frontend
- React 18
- Vite (build tool)
- Axios (HTTP client)
- React Router v7

## Prerequisites

- Docker and Docker Compose
- Google AI Studio API Key
- Supabase account and project

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-chatBot
   ```

2. Create a `.env` file in the root directory with your configuration:
   ```env
   GOOGLE_API_KEY=your_google_ai_studio_api_key
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   SUPABASE_JWT_SECRET=your_supabase_jwt_secret
   CHROMA_DB_PATH=./chroma_db
   ```

3. Deploy the application:
   ```bash
   # On Linux/Mac
   ./deploy.sh
   
   # On Windows
   deploy.bat
   ```

## Manual Deployment

### Backend
```bash
# Install dependencies
pip install -e .

# Run the server
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Or build and serve for production
npm run build
npm run preview
```

## API Endpoints

- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/upload` - Upload and process PDF
- `POST /api/chat` - Chat with PDF content
- `GET /api/sessions` - Get user sessions
- `GET /api/health` - Health check

## Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── auth.py          # Authentication logic
│   ├── chat.py          # Chat functionality
│   ├── config.py        # Configuration management
│   ├── main.py          # Main FastAPI app
│   ├── models.py        # Data models
│   ├── pdf_handler.py   # PDF processing
│   └── session_manager.py # Session management
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── api.js       # API client
│   │   └── config.js    # Frontend configuration
│   └── ...              
├── uploads/             # Uploaded PDF files
├── chroma_db/           # Vector database storage
├── Dockerfile           # Backend Docker configuration
├── docker-compose.yml   # Multi-container deployment
├── deploy.sh            # Deployment script (Linux/Mac)
├── deploy.bat           # Deployment script (Windows)
└── .env                 # Environment variables
```

## License

MIT