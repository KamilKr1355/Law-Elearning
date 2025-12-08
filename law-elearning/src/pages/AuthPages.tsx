
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authService, setAuthToken } from '../services/api';
import { Card, Input, Button } from '../components/UI';

export const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // 1. Get Token
      const tokenRes = await authService.login({ username, password });
      
      // 2. Set token in API headers manually to ensure getProfile works immediately
      setAuthToken(tokenRes.access);
      
      // 3. Fetch full profile (which contains isAdmin flag)
      const profile = await authService.getProfile();
      
      // 4. Update context and storage
      login(tokenRes.access, profile);
      
      navigate('/kursy');
    } catch (err) {
      console.error(err);
      setError('Błędne dane logowania');
    }
  };

  return (
    <div className="flex justify-center items-center h-[80vh]">
      <Card className="w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Witaj ponownie</h2>
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>}
        <form onSubmit={handleSubmit}>
          <Input label="Nazwa użytkownika" value={username} onChange={(e: any) => setUsername(e.target.value)} required />
          <Input label="Hasło" type="password" value={password} onChange={(e: any) => setPassword(e.target.value)} required />
          <Button type="submit" className="w-full mt-4">Zaloguj się</Button>
        </form>
      </Card>
    </div>
  );
};

export const Register = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authService.register(formData);
      navigate('/login');
    } catch (err) {
      setError('Rejestracja nie powiodła się. Sprawdź dane.');
    }
  };

  return (
    <div className="flex justify-center items-center h-[80vh]">
      <Card className="w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Utwórz konto</h2>
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>}
        <form onSubmit={handleSubmit}>
          <Input label="Nazwa użytkownika" value={formData.username} onChange={(e: any) => setFormData({...formData, username: e.target.value})} required />
          <Input label="Email" type="email" value={formData.email} onChange={(e: any) => setFormData({...formData, email: e.target.value})} required />
          <Input label="Hasło" type="password" value={formData.password} onChange={(e: any) => setFormData({...formData, password: e.target.value})} required />
          <Button type="submit" className="w-full mt-4">Zarejestruj się</Button>
        </form>
      </Card>
    </div>
  );
};
