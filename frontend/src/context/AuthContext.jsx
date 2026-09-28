import React, { createContext, useContext, useState, useEffect } from 'react';
import { loginUser as apiLogin, registerUser as apiRegister } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('tech_stack_token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('tech_stack_username');
    if (token && savedUser) {
      setUser({ username: savedUser });
    }
    setLoading(false);
  }, [token]);

  const login = async (username_or_email, password) => {
    const data = await apiLogin({ username_or_email, password });
    localStorage.setItem('tech_stack_token', data.access_token);
    localStorage.setItem('tech_stack_username', data.username);
    setToken(data.access_token);
    setUser({ username: data.username });
    return data;
  };

  const register = async (username, email, password) => {
    const data = await apiRegister({ username, email, password });
    localStorage.setItem('tech_stack_token', data.access_token);
    localStorage.setItem('tech_stack_username', data.username);
    setToken(data.access_token);
    setUser({ username: data.username });
    return data;
  };

  const logout = () => {
    localStorage.removeItem('tech_stack_token');
    localStorage.removeItem('tech_stack_username');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
