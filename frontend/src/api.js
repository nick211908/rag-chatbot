import axios from 'axios';
import { API_URL } from './config';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const signup = (email, password) => 
  api.post('/api/auth/signup', { email, password });

export const login = (email, password) => 
  api.post('/api/auth/login', { email, password });

export const uploadPDF = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/upload', formData);
};

export const sendMessage = (question, sessionId) => 
  api.post('/api/chat', { question, session_id: sessionId });

export default api;
