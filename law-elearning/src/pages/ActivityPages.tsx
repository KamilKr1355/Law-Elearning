
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { aktywnoscService } from '../services/api';
import type { Notatka, ZapisArtykulu } from '../types';
import { Card, Button, Spinner } from '../components/UI';

export const MojeNotatki = () => {
  const [notatki, setNotatki] = useState<Notatka[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchNotatki = () => {
    setLoading(true);
    aktywnoscService.getNotatki()
      .then((data) => {
        // Zabezpieczenie na wypadek, gdyby API zwróciło null lub coś innego niż tablicę
        if (Array.isArray(data)) {
            setNotatki(data);
        } else {
            setNotatki([]);
        }
      })
      .catch((err) => {
        console.error(err);
        setError('Nie udało się pobrać notatek.');
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchNotatki();
  }, []);

  const handleDelete = async (id: number) => {
    if (confirm('Czy na pewno usunąć tę notatkę?')) {
      await aktywnoscService.deleteNotatka(id);
      fetchNotatki();
    }
  };

  if (loading) return <Spinner />;

  if (error) {
      return (
        <Card className="text-center py-10 border-red-200 bg-red-50">
           <p className="text-red-600 mb-4">{error}</p>
           <Button variant="secondary" onClick={fetchNotatki}>Spróbuj ponownie</Button>
        </Card>
      );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Moje Notatki</h1>
      
      {notatki.length === 0 ? (
        <Card className="text-center py-10">
          <p className="text-gray-500 mb-4">Nie masz jeszcze żadnych notatek.</p>
          <Link to="/kursy"><Button>Przejdź do nauki</Button></Link>
        </Card>
      ) : (
        <div className="grid gap-6">
          {notatki.map((note) => (
            <Card key={note.id} className="relative group">
              <div className="flex justify-between items-start mb-2">
                <Link to={`/artykul/${note.artykul_id}`} className="text-sm font-semibold text-indigo-600 hover:underline">
                  Do artykułu #{note.artykul_id}
                </Link>
                <span className="text-xs text-gray-400">
                    {note.data_zapisu ? new Date(note.data_zapisu).toLocaleDateString() : ''}
                </span>
              </div>
              <p className="text-gray-800 whitespace-pre-wrap">{note.tresc}</p>
              
              <div className="mt-4 flex justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                <Button variant="danger" className="text-xs py-1 px-3" onClick={() => handleDelete(note.id)}>Usuń</Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export const ZapisaneArtykuly = () => {
  const [zapisane, setZapisane] = useState<ZapisArtykulu[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchZapisane = () => {
    aktywnoscService.getZapisane()
      .then(data => {
          setZapisane(Array.isArray(data) ? data : []);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchZapisane(); }, []);

  const handleRemove = async (artykulId: number) => {
    // API delete uses artykul_id as param
    await aktywnoscService.deleteZapis(artykulId);
    fetchZapisane();
  };

  if (loading) return <Spinner />;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Zapisane do przeczytania</h1>
      
      {zapisane.length === 0 ? (
        <Card className="text-center py-10">
          <p className="text-gray-500 mb-4">Brak zapisanych artykułów.</p>
          <Link to="/kursy"><Button>Przeglądaj Kursy</Button></Link>
        </Card>
      ) : (
        <div className="grid gap-4">
          {zapisane.map((item) => (
            <Card key={item.id} className="flex justify-between items-center hover:shadow-md transition">
              <div className="flex items-center space-x-4">
                <div className="text-2xl text-yellow-400">★</div>
                <div>
                  <h3 className="font-bold text-lg text-gray-800">{item.tytul}</h3>
                  <span className="text-xs text-gray-500">Zapisano: {item.data_zapisu ? new Date(item.data_zapisu).toLocaleDateString() : ''}</span>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                {/* Używamy artykul_id do linku, a nie ID zakładki */}
                <Link to={`/artykul/${item.artykul_id || '#'}`}><Button variant="secondary">Czytaj</Button></Link>
                {/* Używamy artykul_id do usunięcia */}
                <button onClick={() => handleRemove(item.artykul_id)} className="text-gray-400 hover:text-red-500 transition" title="Usuń z zapisanych">✕</button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
