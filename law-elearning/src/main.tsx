
import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Layout } from './components/Layout';
import { Login, Register } from './pages/AuthPages';
import { KursyList, KursDetail, ArtykulReader } from './pages/CoursePages';
import { AdminDashboard, AdminUsers, AdminKursy, AdminReports, AdminRozdzialy, AdminArtykuly, AdminPytania, AdminOdpowiedzi } from './pages/AdminPages';
import { QuizStart, QuizActive, QuizSummary } from './pages/QuizPages';
import { MojeNotatki, ZapisaneArtykuly, KursNotatki } from './pages/ActivityPages';
import { StudyMode } from './pages/StudyPages';
import { ResultsHistory } from './pages/ResultsPages';
import { ProfilePage } from './pages/ProfilePage';
import { isUserAdmin } from './utils/auth';

const ProtectedRoute = ({ children, adminOnly = false }: { children?: React.ReactNode, adminOnly?: boolean }) => {
  const { user, isLoading, logout } = useAuth();
  
  if (isLoading) return <div className="p-10 text-center flex justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div></div>;
  if (!user) return <Navigate to="/login" replace />;
  
  if (adminOnly && !isUserAdmin(user)) {
      console.warn("Access Denied: User is not recognized as Admin", user);
      
      return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center p-4">
            <div className="bg-white p-8 rounded-xl shadow-lg max-w-md w-full text-center border-t-4 border-red-500">
                <div className="text-5xl mb-4">🚫</div>
                <h1 className="text-2xl font-bold text-gray-900 mb-2">Odmowa Dostępu</h1>
                <p className="text-gray-600 mb-6">Ta sekcja jest dostępna tylko dla administratorów.</p>
                
                <div className="bg-gray-100 p-4 rounded text-left text-xs font-mono mb-6 overflow-x-auto">
                    <p className="font-bold text-gray-500 mb-1">DIAGNOSTYKA:</p>
                    <p>User: <span className="text-blue-600">{user.username}</span></p>
                    <p>Raw isAdmin: <span className="text-red-600">{JSON.stringify(user.isAdmin)}</span> ({typeof user.isAdmin})</p>
                    <p>Detected Role: <span className="font-bold">{isUserAdmin(user) ? 'ADMIN' : 'STUDENT'}</span></p>
                </div>

                <div className="space-y-3">
                    <button 
                        onClick={() => { logout(); window.location.href = '/login'; }}
                        className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded font-medium transition"
                    >
                        Wyloguj i zaloguj ponownie
                    </button>
                    <button 
                        onClick={() => window.location.href = '/'} 
                        className="w-full py-2 px-4 text-gray-500 hover:text-gray-700 text-sm"
                    >
                        Wróć na stronę główną
                    </button>
                </div>
            </div>
        </div>
      );
  }

  return <>{children}</>;
};

const App = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/" element={<Navigate to="/kursy" />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            <Route path="/kursy" element={<ProtectedRoute><KursyList /></ProtectedRoute>} />
            <Route path="/kursy/:id" element={<ProtectedRoute><KursDetail /></ProtectedRoute>} />
            <Route path="/artykul/:id" element={<ProtectedRoute><ArtykulReader /></ProtectedRoute>} />
            <Route path="/nauka/:kursId" element={<ProtectedRoute><StudyMode /></ProtectedRoute>} />
            <Route path="/wyniki" element={<ProtectedRoute><ResultsHistory /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
            <Route path="/kursy/:kursId/notatki" element={<ProtectedRoute><KursNotatki /></ProtectedRoute>} />
            
            <Route path="/quiz" element={<ProtectedRoute><QuizStart /></ProtectedRoute>} />
            <Route path="/quiz/play" element={<ProtectedRoute><QuizActive /></ProtectedRoute>} />
            <Route path="/quiz/wynik" element={<ProtectedRoute><QuizSummary /></ProtectedRoute>} />

            <Route path="/moje-notatki" element={<ProtectedRoute><MojeNotatki /></ProtectedRoute>} />
            <Route path="/zapisane" element={<ProtectedRoute><ZapisaneArtykuly /></ProtectedRoute>} />
            
            <Route path="/admin" element={<ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>} />
            <Route path="/admin/users" element={<ProtectedRoute adminOnly><AdminUsers /></ProtectedRoute>} />
            <Route path="/admin/raporty" element={<ProtectedRoute adminOnly><AdminReports /></ProtectedRoute>} />
            <Route path="/admin/kursy" element={<ProtectedRoute adminOnly><AdminKursy /></ProtectedRoute>} />
            <Route path="/admin/kursy/:kursId/rozdzialy" element={<ProtectedRoute adminOnly><AdminRozdzialy /></ProtectedRoute>} />
            <Route path="/admin/kursy/:kursId/artykuly" element={<ProtectedRoute adminOnly><AdminArtykuly /></ProtectedRoute>} />
            <Route path="/admin/artykuly/:artykulId/pytania" element={<ProtectedRoute adminOnly><AdminPytania /></ProtectedRoute>} />
            <Route path="/admin/pytania/:pytanieId/odpowiedzi" element={<ProtectedRoute adminOnly><AdminOdpowiedzi /></ProtectedRoute>} />
            
            <Route path="*" element={<div className="text-center mt-20 text-xl text-gray-400">404 - Strona nie istnieje</div>} />
          </Routes>
        </Layout>
      </AuthProvider>
    </BrowserRouter>
  );
};

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<App />);
}
