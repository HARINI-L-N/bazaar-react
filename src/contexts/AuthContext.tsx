import React, { createContext, useContext, useState, useEffect } from 'react';
import { endpoints } from '@/lib/api';

interface User {
  id: string;
  email: string;
  name: string;
  token?: string; // JWT access token provided by backend
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, name?: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored user session
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const parsed = JSON.parse(storedUser);
        // Keep backward compatibility if older mock user without token is present
        setUser(parsed);
      } catch (e) {
        setUser(null);
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (username: string, password: string) => {
    // Call backend login endpoint to obtain JWT
    const res = await endpoints.login({ username, password });
    const payload = res.data && res.data.data ? res.data.data : res.data;
    const userData = payload?.user;
    const token = payload?.access_token || payload?.token;

    if (!userData) throw new Error('Login failed: no user returned');

    const stored = { id: userData.id || userData._id || String(userData.id), email: userData.email, name: userData.username || userData.first_name || userData.name || '', token };
    localStorage.setItem('user', JSON.stringify(stored));
    setUser(stored);
  };

  const register = async (username: string, password: string, name?: string) => {
    // Call backend register endpoint
    const res = await endpoints.register({ username, email: username, password, first_name: name });
    const payload = res.data && res.data.data ? res.data.data : res.data;
    const userData = payload?.user;
    const token = payload?.access_token || payload?.token;

    if (!userData) throw new Error('Registration failed: no user returned');

    const stored = { id: userData.id || userData._id || String(userData.id), email: userData.email, name: userData.username || userData.first_name || userData.name || '', token };
    localStorage.setItem('user', JSON.stringify(stored));
    setUser(stored);
  };

  const logout = () => {
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
