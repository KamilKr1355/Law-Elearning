
import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from './UI';
import { isUserAdmin } from '../utils/auth';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <span className="text-2xl font-bold text-indigo-600 tracking-tighter">Law<span className="text-gray-900">Edu</span></span>
            </Link>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              <Link to="/kursy" className="text-gray-900 hover:text-indigo-600 px-3 py-2 text-sm font-medium transition-colors">Kursy</Link>
              {user && <Link to="/quiz" className="text-gray-900 hover:text-indigo-600 px-3 py-2 text-sm font-medium transition-colors">Quizy</Link>}
              {user && <Link to="/wyniki" className="text-gray-900 hover:text-indigo-600 px-3 py-2 text-sm font-medium transition-colors">Wyniki</Link>}
              {/* Robust admin check */}
              {user && isUserAdmin(user) && <Link to="/admin" className="text-indigo-600 px-3 py-2 text-sm font-medium">Panel Admina</Link>}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <Link to="/zapisane" className="text-gray-500 hover:text-yellow-500 transition mr-2" title="Zapisane artykuły">
                   ★
                </Link>
                <Link to="/profile" className="flex flex-col text-right mr-2 cursor-pointer hover:opacity-80 transition">
                  <span className="text-sm font-semibold text-gray-900">{user.username}</span>
                  <span className="text-xs text-gray-500">{isUserAdmin(user) ? 'Administrator' : 'Student'}</span>
                </Link>
                <Button variant="secondary" onClick={handleLogout} className="text-sm">Wyloguj</Button>
              </>
            ) : (
              <>
                <Link to="/login"><Button variant="ghost">Logowanie</Button></Link>
                <Link to="/register"><Button variant="primary">Rejestracja</Button></Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      <footer className="bg-white border-t border-gray-200 py-8">
        <div className="container mx-auto text-center text-gray-500 text-sm">
          <p className="mb-2">&copy; {new Date().getFullYear()} Law E-Learning Platform. Wszelkie prawa zastrzeżone.</p>
          <div className="space-x-4">
             <Link to="/kursy" className="hover:text-indigo-600">Kursy</Link>
             <Link to="/login" className="hover:text-indigo-600">Logowanie</Link>
             <Link to="/register" className="hover:text-indigo-600">Rejestracja</Link>
          </div>
        </div>
      </footer>
    </div>
  );
};
