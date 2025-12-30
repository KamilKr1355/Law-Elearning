
import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { aktywnoscService, kursService } from '../services/api';
import type { Notatka, ZapisArtykulu, ArtykulView } from '../types';
import { Card, Button, Spinner, ConfirmationModal, Badge } from '../components/UI';

export const MojeNotatki = () => {
  const [notatki, setNotatki] = useState<Notatka[]>([]);
  const [articlesMap, setArticlesMap] = useState<{[key: number]: {tytul: string, nr: string}}>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [noteToDelete, setNoteToDelete] = useState<number | null>(null);

  // Stan edycji
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingText, setEditingText] = useState('');

  const fetchNotatki = async () => {
    setLoading(true);
    try {
        const notesData = await aktywnoscService.getNotatki();
        const safeNotes = Array.isArray(notesData) ? notesData : [];
        setNotatki(safeNotes);

        const uniqueIds = Array.from(new Set(safeNotes.map(n => n.artykul_id)));
        const map: {[key: number]: {tytul: string, nr: string}} = {};
        
        await Promise.all(uniqueIds.map(async (id) => {
            try {
                const artDetail = await kursService.getArtykulDetail(id.toString());
                map[id] = { 
                    tytul: artDetail.tytul || 'Artykuł bez tytułu',
                    nr: artDetail.nr_artykulu || ''
                };
            } catch (e) {
                map[id] = { tytul: `Artykuł #${id}`, nr: '' };
            }
        }));
        
        setArticlesMap(map);
    } catch (err) {
        console.error(err);
        setError('Nie udało się pobrać notatek.');
    } finally {
        setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotatki();
  }, []);

  const handleEditStart = (note: Notatka) => {
    setEditingId(note.id);
    setEditingText(note.tresc);
  };

  const handleEditCancel = () => {
    setEditingId(null);
    setEditingText('');
  };

  const handleEditSave = async (id: number) => {
    if (!editingText.trim()) return;
    try {
        await aktywnoscService.updateNotatka(id, editingText);
        setNotatki(prev => prev.map(n => n.id === id ? { ...n, tresc: editingText } : n));
        setEditingId(null);
    } catch (e) {
        alert('Błąd podczas zapisywania notatki.');
    }
  };

  const handleDeleteClick = (id: number) => {
      setNoteToDelete(id);
      setDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
      if (!noteToDelete) return;
      try {
          await aktywnoscService.deleteNotatka(noteToDelete);
          setNotatki(prev => prev.filter(n => n.id !== noteToDelete));
      } catch (e) {
          console.error(e);
          fetchNotatki();
      } finally {
          setDeleteModalOpen(false);
          setNoteToDelete(null);
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
    <>
      <ConfirmationModal 
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDelete}
        title="Usuwanie notatki"
        message="Czy na pewno chcesz usunąć tę notatkę? Tej operacji nie można cofnąć."
      />

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Moje Notatki</h1>
        
        {notatki.length === 0 ? (
          <Card className="text-center py-10">
            <p className="text-gray-500 mb-4">Nie masz jeszcze żadnych notatek.</p>
            <Link to="/kursy"><Button>Przejdź do nauki</Button></Link>
          </Card>
        ) : (
          <div className="grid gap-6">
            {notatki.map((note) => {
              const artData = articlesMap[note.artykul_id];
              const isEditing = editingId === note.id;

              return (
                <Card key={note.id} className="relative group border-l-4 border-l-yellow-400">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex flex-col">
                        <Link to={`/artykul/${note.artykul_id}`} className="flex items-center space-x-2 group/link">
                          {artData?.nr && <Badge color="blue">Art. {artData.nr}</Badge>}
                          <span className="text-sm font-bold text-indigo-600 group-hover/link:underline">
                            {artData?.tytul || `Artykuł #${note.artykul_id}`}
                          </span>
                        </Link>
                    </div>
                    <span className="text-xs text-gray-400">
                        {note.data_zapisu ? new Date(note.data_zapisu).toLocaleDateString() : ''}
                    </span>
                  </div>
                  
                  {isEditing ? (
                    <div className="mt-2 space-y-2">
                      <textarea 
                        className="w-full p-3 border-2 border-yellow-200 rounded-lg focus:ring-2 focus:ring-yellow-500 outline-none bg-yellow-50/50"
                        value={editingText}
                        rows={4}
                        onChange={(e) => setEditingText(e.target.value)}
                      />
                      <div className="flex justify-end space-x-2">
                        <Button variant="ghost" onClick={handleEditCancel} className="text-xs">Anuluj</Button>
                        <Button onClick={() => handleEditSave(note.id)} className="text-xs">Zapisz</Button>
                      </div>
                    </div>
                  ) : (
                    <>
                      <p className="text-gray-800 whitespace-pre-wrap bg-yellow-50/50 p-3 rounded border border-yellow-100 italic">{note.tresc}</p>
                      <div className="mt-4 flex justify-end space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onClick={() => handleEditStart(note)} className="text-xs text-gray-500 hover:text-indigo-600 transition">Edytuj</button>
                        <button onClick={() => handleDeleteClick(note.id)} className="text-xs text-red-400 hover:text-red-600 transition">Usuń</button>
                      </div>
                    </>
                  )}
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </>
  );
};

export const KursNotatki = () => {
    const { kursId } = useParams<{ kursId: string }>();
    const [notatki, setNotatki] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [noteToDelete, setNoteToDelete] = useState<number | null>(null);

    const [editingId, setEditingId] = useState<number | null>(null);
    const [editingText, setEditingText] = useState('');

    const fetchNotatki = async () => {
        if (!kursId) return;
        setLoading(true);
        try {
            const data = await aktywnoscService.getNotatkiKursu(kursId);
            setNotatki(Array.isArray(data) ? data : []);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchNotatki(); }, [kursId]);

    const handleEditStart = (note: any) => {
        setEditingId(note.id);
        setEditingText(note.tresc);
    };

    const handleEditCancel = () => {
        setEditingId(null);
        setEditingText('');
    };

    const handleEditSave = async (id: number) => {
        if (!editingText.trim()) return;
        try {
            await aktywnoscService.updateNotatka(id, editingText);
            setNotatki(prev => prev.map(n => n.id === id ? { ...n, tresc: editingText } : n));
            setEditingId(null);
        } catch (e) {
            alert('Błąd podczas zapisu.');
        }
    };

    const handleDeleteClick = (id: number) => {
        setNoteToDelete(id);
        setDeleteModalOpen(true);
    };

    const confirmDelete = async () => {
        if (!noteToDelete) return;
        try {
            await aktywnoscService.deleteNotatka(noteToDelete);
            setNotatki(prev => prev.filter(n => n.id !== noteToDelete));
        } catch (e) {
            console.error(e);
        } finally {
            setDeleteModalOpen(false);
            setNoteToDelete(null);
        }
    };

    if (loading) return <Spinner />;

    return (
        <>
            <ConfirmationModal 
                isOpen={deleteModalOpen}
                onClose={() => setDeleteModalOpen(false)}
                onConfirm={confirmDelete}
                title="Usuwanie notatki"
                message="Czy na pewno chcesz usunąć tę notatkę?"
            />

            <div className="max-w-4xl mx-auto">
                <div className="flex items-center space-x-4 mb-6">
                    <Link to={kursId ? `/kursy/${kursId}` : "/kursy"} className="text-gray-400 hover:text-gray-600">&larr; Wróć</Link>
                    <h1 className="text-3xl font-bold text-gray-900">Notatki: {notatki[0]?.nazwa_kursu || 'Twój Kurs'}</h1>
                </div>

                {notatki.length === 0 ? (
                    <Card className="text-center py-10">
                        <p className="text-gray-500">Brak notatek dla tego kursu.</p>
                    </Card>
                ) : (
                    <div className="grid gap-6">
                        {notatki.map((note) => {
                            const isEditing = editingId === note.id;
                            return (
                                <Card key={note.id} className="relative group border-l-4 border-l-yellow-400">
                                    <div className="flex justify-between items-start mb-2">
                                        <Link to={`/artykul/${note.artykul_id}`} className="flex items-center space-x-2 group/link">
                                            <Badge color="blue">Art. {note.nr_artykulu || note.artykul_id}</Badge>
                                            <span className="text-sm font-bold text-indigo-600 group-hover/link:underline">Otwórz źródło</span>
                                        </Link>
                                        <span className="text-xs text-gray-400">
                                            {note.data_zapisu ? new Date(note.data_zapisu).toLocaleDateString() : ''}
                                        </span>
                                    </div>
                                    
                                    {isEditing ? (
                                        <div className="mt-2 space-y-2">
                                          <textarea 
                                            className="w-full p-3 border-2 border-yellow-200 rounded-lg focus:ring-2 focus:ring-yellow-500 outline-none bg-yellow-50/50"
                                            value={editingText}
                                            rows={4}
                                            onChange={(e) => setEditingText(e.target.value)}
                                          />
                                          <div className="flex justify-end space-x-2">
                                            <Button variant="ghost" onClick={handleEditCancel} className="text-xs">Anuluj</Button>
                                            <Button onClick={() => handleEditSave(note.id)} className="text-xs">Zapisz</Button>
                                          </div>
                                        </div>
                                    ) : (
                                        <>
                                          <p className="text-gray-800 whitespace-pre-wrap bg-yellow-50/50 p-3 rounded border border-yellow-100 italic">{note.tresc}</p>
                                          <div className="mt-4 flex justify-end space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                              <button onClick={() => handleEditStart(note)} className="text-xs text-gray-500 hover:text-indigo-600 transition">Edytuj</button>
                                              <Button variant="danger" className="text-xs py-1 px-3" onClick={() => handleDeleteClick(note.id)}>Usuń</Button>
                                          </div>
                                        </>
                                    )}
                                </Card>
                            );
                        })}
                    </div>
                )}
            </div>
        </>
    );
};

export const ZapisaneArtykuly = () => {
  const [zapisane, setZapisane] = useState<ZapisArtykulu[]>([]);
  const [loading, setLoading] = useState(true);

  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [bookmarkToDelete, setBookmarkToDelete] = useState<number | null>(null);

  const fetchZapisane = () => {
    aktywnoscService.getZapisane()
      .then(data => {
          setZapisane(Array.isArray(data) ? data : []);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchZapisane(); }, []);

  const handleRemoveClick = (artykulId: number) => {
      setBookmarkToDelete(artykulId);
      setDeleteModalOpen(true);
  };

  const confirmRemove = async () => {
      if (!bookmarkToDelete) return;
      try {
          await aktywnoscService.deleteZapis(bookmarkToDelete);
          setZapisane(prev => prev.filter(item => item.artykul_id !== bookmarkToDelete));
      } catch (e) {
          console.error(e);
          fetchZapisane();
      } finally {
          setDeleteModalOpen(false);
          setBookmarkToDelete(null);
      }
  };

  if (loading) return <Spinner />;

  return (
    <>
      <ConfirmationModal 
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmRemove}
        title="Usuwanie zakładki"
        message="Czy na pewno chcesz usunąć ten artykuł z zapisanych?"
        confirmLabel="Usuń"
      />

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
                  <Link to={`/artykul/${item.artykul_id || '#'}`}><Button variant="secondary">Czytaj</Button></Link>
                  <button onClick={() => handleRemoveClick(item.artykul_id)} className="text-gray-400 hover:text-red-500 transition" title="Usuń z zapisanych">✕</button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </>
  );
};
