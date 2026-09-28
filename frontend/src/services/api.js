import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Interceptor to inject JWT Auth token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('tech_stack_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

export const fetchHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export const fetchRoles = async () => {
  const response = await api.get('/api/roles');
  return response.data;
};

export const fetchSkills = async () => {
  const response = await api.get('/api/skills');
  return response.data;
};

export const fetchGithubProfile = async (username) => {
  const response = await api.get(`/api/github/${encodeURIComponent(username)}`);
  return response.data;
};

export const runPortfolioAnalysis = async (payload) => {
  const response = await api.post('/api/analysis', payload);
  return response.data;
};

export const fetchAnalysisById = async (id) => {
  const response = await api.get(`/api/analysis/${id}`);
  return response.data;
};

export const loginUser = async (credentials) => {
  const response = await api.post('/api/auth/login', credentials);
  return response.data;
};

export const registerUser = async (userData) => {
  const response = await api.post('/api/auth/register', userData);
  return response.data;
};

export default api;
