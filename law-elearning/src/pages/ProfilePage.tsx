
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { authService } from '../services/api';
import { Card, Button, Input, Spinner } from '../components/UI';
import { isUserAdmin } from '../utils/auth';

export const ProfilePage = () => {
  const { user, login } = useAuth();
  const [formData, setFormData] = useState({ name: '', email: '', password: '', newPassword: '' });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    if (user) {
      setFormData(prev => ({ 
        ...prev, 
        name: user.name || '', 
        email: user.email || '' 
      }));
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      // Mock update
      const updatedUser = await authService.updateProfile({
        ...user,
        name: formData.name,
        email: formData.email
      });
      
      // Update context
      if (user && user.token) {
        login(user.token, updatedUser);
      }
      
      setMessage({ type: 'success', text: 'Profil został zaktualizowany!' });
    } catch (err) {
      setMessage({ type: 'error', text: 'Wystąpił błąd podczas aktualizacji.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-10">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Ustawienia Profilu</h1>
      
      <div className="grid gap-6">
        <Card>
          <div className="flex items-center space-x-4 mb-6">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center text-2xl font-bold text-indigo-600">
              {user?.username.charAt(0).toUpperCase()}
            </div>
            <div>
              <h2 className="text-xl font-bold">{user?.username}</h2>
              <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                {isUserAdmin(user) ? 'Administrator' : 'Student'}
              </span>
            </div>
          </div>

          {message.text && (
            <div className={`p-4 rounded mb-4 ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {message.text}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input 
              label="Imię i Nazwisko" 
              value={formData.name} 
              onChange={(e: any) => setFormData({...formData, name: e.target.value})} 
            />
            <Input 
              label="Adres Email" 
              type="email"
              value={formData.email} 
              onChange={(e: any) => setFormData({...formData, email: e.target.value})} 
            />
            
            <div className="border-t pt-4 mt-4">
              <h3 className="font-semibold mb-4 text-gray-700">Zmiana hasła (opcjonalne)</h3>
              <Input 
                label="Nowe hasło" 
                type="password"
                placeholder="Pozostaw puste, aby nie zmieniać"
                value={formData.newPassword} 
                onChange={(e: any) => setFormData({...formData, newPassword: e.target.value})} 
              />
            </div>

            <div className="flex justify-end pt-4">
              <Button type="submit" disabled={loading}>
                {loading ? 'Zapisywanie...' : 'Zapisz zmiany'}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};
