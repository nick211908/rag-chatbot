import json
import os
from typing import Optional

class SessionManager:
    def __init__(self, storage_file: str = "sessions.json"):
        self.storage_file = storage_file
        self._load_sessions()
    
    def _load_sessions(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                self.sessions = json.load(f)
        else:
            self.sessions = {}
    
    def _save_sessions(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.sessions, f)
    
    def create_session(self, session_id: str, user_id: str, filename: str):
        self.sessions[session_id] = {
            "user_id": user_id,
            "filename": filename
        }
        self._save_sessions()
    
    def get_session(self, session_id: str) -> Optional[dict]:
        return self.sessions.get(session_id)
    
    def verify_ownership(self, session_id: str, user_id: str) -> bool:
        session = self.get_session(session_id)
        if not session:
            return False
        return session["user_id"] == user_id
    
    def get_user_sessions(self, user_id: str) -> list:
        return [
            {"session_id": sid, **sdata}
            for sid, sdata in self.sessions.items()
            if sdata["user_id"] == user_id
        ]

session_manager = SessionManager()
