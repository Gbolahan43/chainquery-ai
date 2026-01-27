import axios from 'axios';

// Create an Axios instance pointing to the FastAPI backend
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor: Automatically add Token if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export { api };

// Authentication API
export const authApi = {
  signup: async (email: string, password: string, fullName?: string) => {
    const res = await api.post('/auth/signup', {
      email,
      password,
      full_name: fullName
    });
    // Save Token
    localStorage.setItem('auth_token', res.data.access_token);
    return res.data;
  },

  login: async (email: string, password: string) => {
    // OAuth2 expects application/x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append('username', email); // Backend expects 'username'
    params.append('password', password);

    const res = await api.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    localStorage.setItem('auth_token', res.data.access_token);
    return res.data;
  },

  logout: () => {
    localStorage.removeItem('auth_token');
    window.location.href = '/login';
  }
};

// Query API for ChainQuery
export const chainQueryApi = {
  generate: async (input: string, chain: string, sessionId: string) => {
    // The interceptor automatically adds the token if user is logged in
    const res = await api.post('/generate', {
      user_input: input,
      chain,
      session_id: sessionId
    });
    return res.data;
  },

  getHistory: async (sessionId: string, limit: number = 10) => {
    const res = await api.get('/history', {
      params: { session_id: sessionId, limit }
    });
    return res.data;
  }
};



