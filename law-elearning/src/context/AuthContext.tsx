
import React, { createContext, useContext, useState, useEffect } from 'react';
import type { User } from '../types';
import { authService, setAuthToken } from '../services/api';

interface AuthContextType {
  user: User | null;
  login: (token: string, userData: User) => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType>(null!);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Funkcja czyszcząca sesję
  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    setAuthToken(''); // Czyści nagłówki axios
  };

  const login = (token: string, userData: User) => {
    const userWithToken = { ...userData, token };
    setUser(userWithToken);
    localStorage.setItem('user', JSON.stringify(userWithToken));
    setAuthToken(token); // Ustawia nagłówki axios natychmiast
  };

  useEffect(() => {
    const initAuth = async () => {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const parsedUser = JSON.parse(storedUser);
          
          if (parsedUser.token) {
            // Ustaw token, żeby zapytanie o profil przeszło
            setAuthToken(parsedUser.token);
            
            try {
              // Pobierz świeże dane z serwera (w tym isAdmin)
              const freshProfile = await authService.getProfile();
              
              // Zaktualizuj stan najnowszymi danymi
              const updatedUser = { ...freshProfile, token: parsedUser.token };
              setUser(updatedUser);
              localStorage.setItem('user', JSON.stringify(updatedUser));
            } catch (err) {
              console.warn("Error fetching profile, keeping local data for debug purposes", err);
              // ZMIANA: Nie wylogowujemy agresywnie, pozwalamy UI obsłużyć stan
              // Jeśli token wygasł, kolejne zapytania API i tak zwrócą 401
              if (!user) {
                  setUser(parsedUser);
              }
            }
          } else {
             logout();
          }
        } catch (e) {
          logout();
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
