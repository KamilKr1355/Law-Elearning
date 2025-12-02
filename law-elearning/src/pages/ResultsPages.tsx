import React, { useEffect, useState } from 'react';
import { wynikiService, kursService } from '../services/api';
import type { WynikEgzaminu, Kurs } from '../types';
import { Card, Spinner, Badge } from '../components/UI';
import { useAuth } from '../context/AuthContext';

export const ResultsHistory = () => {
  const [wyniki, setWyniki] = useState<WynikEgzaminu[]>([]);
  const [kursy, setKursy] = useState<Kurs[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    Promise.all([
      wynikiService.getAll(),
      kursService.getAll()
    ]).then(([wData, kData]) => {
      // Filter results for current user just in case API returns all (though standard user API usually filters)
      // Assuming API returns mixed if not careful, but let's trust the backend or filter if needed.
      // Based on swagger, /aktywnosc/wyniki-egzaminu/ returns list.
      // If user.id is available, we can filter.
      const myResults = user ? wData.filter((w: { uzytkownik_id: number; }) => w.uzytkownik_id === user.id) : wData;
      
      // Sort by date desc
      myResults.sort((a: { data_zapisu: string | number | Date; }, b: { data_zapisu: string | number | Date; }) => new Date(b.data_zapisu).getTime() - new Date(a.data_zapisu).getTime());
      
      setWyniki(myResults);
      setKursy(kData);
    }).finally(() => setLoading(false));
  }, [user]);

  const getKursName = (id: number) => {
    return kursy.find(k => k.id === id)?.nazwa_kursu || `Kurs ID: ${id}`;
  };

  if (loading) return <Spinner />;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold text-gray-900">Twoje Wyniki</h1>
        
        {/* Simple Stats Summary */}
        <div className="flex space-x-4">
            <Card className="px-4 py-2 flex flex-col items-center">
                <span className="text-xs text-gray-500 uppercase">Egzaminy</span>
                <span className="font-bold text-xl">{wyniki.length}</span>
            </Card>
            <Card className="px-4 py-2 flex flex-col items-center">
                <span className="text-xs text-gray-500 uppercase">Średnia</span>
                <span className="font-bold text-xl text-indigo-600">
                    {wyniki.length > 0 
                        ? (wyniki.reduce((acc, curr) => acc + curr.wynik, 0) / wyniki.length).toFixed(0) 
                        : 0}%
                </span>
            </Card>
        </div>
      </div>

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
                    <span className={`text-2xl font-bold ${wynik.wynik >= 50 ? 'text-green-600' : 'text-red-500'}`}>
                        {Math.round(wynik.wynik)}%
                    </span>
                 </div>
                 <div className="w-16 h-16 relative flex items-center justify-center">
                    <svg className="w-full h-full transform -rotate-90">
                        <circle cx="32" cy="32" r="28" stroke="#e5e7eb" strokeWidth="6" fill="transparent" />
                        <circle cx="32" cy="32" r="28" stroke={wynik.wynik >= 50 ? '#10b981' : '#ef4444'} strokeWidth="6" fill="transparent" 
                                strokeDasharray={175.9} 
                                strokeDashoffset={175.9 - (175.9 * wynik.wynik) / 100} />
                    </svg>
                 </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};