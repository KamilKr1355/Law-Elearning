
import React, { useEffect, useState } from 'react';
import { wynikiService, kursService } from '../services/api';
import type { WynikEgzaminu, Kurs, LeaderboardEntry } from '../types';
import { Card, Spinner, Badge } from '../components/UI';
import { useAuth } from '../context/AuthContext';

export const ResultsHistory = () => {
  const [wyniki, setWyniki] = useState<WynikEgzaminu[]>([]);
  const [kursy, setKursy] = useState<Kurs[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    // Wrap fetches in Promise.all to load in parallel, but handle errors individually
    // so one failure doesn't break the whole page (e.g. leaderboard).
    Promise.all([
      wynikiService.getAll().catch(() => []), // Safe fetch: return empty array on error
      kursService.getAll().catch(() => []),   // Safe fetch
      wynikiService.getLeaderboard().catch(() => []) // Safe fetch
    ]).then(([wData, kData, lData]) => {
      // Filter results for current user
      // Safe check if wData is array
      const safeWData = Array.isArray(wData) ? wData : [];
      const myResults = user ? safeWData.filter(w => w.uzytkownik_id === user.id) : safeWData;
      
      myResults.sort((a, b) => new Date(b.data_zapisu).getTime() - new Date(a.data_zapisu).getTime());
      
      setWyniki(myResults);
      setKursy(Array.isArray(kData) ? kData : []);
      if (Array.isArray(lData)) {
          setLeaderboard(lData);
      }
    }).finally(() => setLoading(false));
  }, [user]);

  const getKursName = (id: number) => {
    return kursy.find(k => k.id === id)?.nazwa_kursu || `Kurs ID: ${id}`;
  };

  if (loading) return <Spinner />;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      
      {/* Top Section: Header & Leaderboard */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-4">
              <h1 className="text-3xl font-bold text-gray-900">Twoje Wyniki</h1>
              <div className="flex space-x-4">
                <Card className="px-4 py-2 flex flex-col items-center">
                    <span className="text-xs text-gray-500 uppercase">Egzaminy</span>
                    <span className="font-bold text-xl">{wyniki.length}</span>
                </Card>
                <Card className="px-4 py-2 flex flex-col items-center">
                    <span className="text-xs text-gray-500 uppercase">Twoja Średnia</span>
                    <span className="font-bold text-xl text-indigo-600">
                        {wyniki.length > 0 
                            ? (wyniki.reduce((acc, curr) => acc + Number(curr.wynik || 0), 0) / wyniki.length).toFixed(0) 
                            : 0}%
                    </span>
                </Card>
            </div>
          </div>

          {/* Leaderboard Card */}
          <div className="relative">
              <Card className="bg-gradient-to-br from-indigo-900 to-indigo-700 text-white h-full border-none">
                  <h3 className="font-bold text-lg mb-4 flex items-center">
                      <span className="text-2xl mr-2">🏆</span> Top 3 Studentów
                  </h3>
                  <div className="space-y-3">
                      {leaderboard.length === 0 ? (
                          <p className="text-indigo-200 text-sm">Brak wystarczającej liczby wyników do rankingu.</p>
                      ) : (
                          leaderboard.map((entry, idx) => {
                              let medal = '';
                              let bgClass = '';
                              if (idx === 0) { medal = '🥇'; bgClass = 'bg-yellow-500/20'; }
                              else if (idx === 1) { medal = '🥈'; bgClass = 'bg-gray-400/20'; }
                              else if (idx === 2) { medal = '🥉'; bgClass = 'bg-orange-600/20'; }

                              return (
                                  <div key={idx} className={`flex justify-between items-center p-2 rounded ${bgClass}`}>
                                      <div className="flex items-center space-x-2">
                                          <span>{medal}</span>
                                          <span className="font-medium text-sm truncate max-w-[120px]">{entry.username}</span>
                                      </div>
                                      {/* FIX: Ensure srednia is treated as a number */}
                                      <span className="font-bold text-sm">{Number(entry.srednia).toFixed(1)}%</span>
                                  </div>
                              );
                          })
                      )}
                  </div>
              </Card>
          </div>
      </div>

      <div className="border-t pt-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Historia Egzaminów</h2>
        {wyniki.length === 0 ? (
            <Card className="text-center py-10">
            <p className="text-gray-500">Brak historii egzaminów.</p>
            </Card>
        ) : (
            <div className="grid gap-4">
            {wyniki.map((wynik) => (
                <Card key={wynik.id} className="flex flex-col md:flex-row justify-between items-center transition hover:shadow-md">
                <div className="flex flex-col mb-4 md:mb-0">
                    <span className="font-bold text-lg text-gray-800">{getKursName(wynik.kurs_id)}</span>
                    <span className="text-sm text-gray-500">{new Date(wynik.data_zapisu).toLocaleString()}</span>
                </div>
                
                <div className="flex items-center space-x-6">
                    <div className="text-right">
                        <span className="block text-xs text-gray-400 uppercase">Wynik</span>
                        <span className={`text-2xl font-bold ${Number(wynik.wynik) >= 50 ? 'text-green-600' : 'text-red-500'}`}>
                            {Math.round(Number(wynik.wynik))}%
                        </span>
                    </div>
                    <div className="w-16 h-16 relative flex items-center justify-center">
                        <svg className="w-full h-full transform -rotate-90">
                            <circle cx="32" cy="32" r="28" stroke="#e5e7eb" strokeWidth="6" fill="transparent" />
                            <circle cx="32" cy="32" r="28" stroke={Number(wynik.wynik) >= 50 ? '#10b981' : '#ef4444'} strokeWidth="6" fill="transparent" 
                                    strokeDasharray={175.9} 
                                    strokeDashoffset={175.9 - (175.9 * Number(wynik.wynik)) / 100} />
                        </svg>
                    </div>
                </div>
                </Card>
            ))}
            </div>
        )}
      </div>
    </div>
  );
};
