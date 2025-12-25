
import React, { useEffect, useState } from 'react';
import { Card, Button, Input, Spinner, Badge, ConfirmationModal } from '../components/UI';
import { kursService, authService, contentAdminService, wynikiService } from '../services/api';
import { Link, useParams } from 'react-router-dom';
import type { Kurs, Rozdzial, Artykul, Pytanie, Odpowiedz, WynikEgzaminu, StatystykiPytania, KursDni } from '../types';
import { isUserAdmin } from '../utils/auth';
import { useAuth } from '../context/AuthContext';

const AdminLayout = ({ title, children, actions, backLink }: any) => (
  <div className="space-y-6">
    <div className="flex justify-between items-center border-b pb-4">
      <div className="flex items-center space-x-4">
        {backLink && <Link to={backLink} className="text-gray-400 hover:text-gray-600 text-sm">&larr; Wróć</Link>}
        <h1 className="text-2xl font-bold text-gray-800">{title}</h1>
      </div>
      <div className="flex space-x-2">{actions}</div>
    </div>
    {children}
  </div>
);

// ------------------- DASHBOARD -------------------
export const AdminDashboard = () => {
  const [stats, setStats] = useState<{label: string, value: number}[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    wynikiService.getStatsLast7Days().then(data => {
        const rawData = Array.isArray(data) ? data : [];
        const chartData = rawData.map((item: any) => {
            const dateObj = new Date(item.dzien);
            const label = `${String(dateObj.getDate()).padStart(2, '0')}.${String(dateObj.getMonth() + 1).padStart(2, '0')}`;
            return {
                label: label,
                value: item.liczba_kursow
            };
        });

        setStats(chartData);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  const maxVal = stats.length > 0 ? Math.max(...stats.map(s => s.value), 1) : 10;

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-extrabold text-indigo-900 tracking-tight">PANEL GŁÓWNY (ADMIN)</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/admin/kursy">
          <Card hover className="bg-gradient-to-br from-indigo-500 to-purple-600 text-white border-none h-full flex flex-col justify-center items-center text-center p-8">
            <div className="text-5xl mb-4">📚</div>
            <h3 className="text-2xl font-bold">Kursy</h3>
            <p className="opacity-80 mt-2">Zarządzaj treścią edukacyjną</p>
          </Card>
        </Link>
        <Link to="/admin/users">
          <Card hover className="bg-white h-full flex flex-col justify-center items-center text-center p-8">
            <div className="text-5xl mb-4">👥</div>
            <h3 className="text-2xl font-bold text-gray-800">Użytkownicy</h3>
            <p className="text-gray-500 mt-2">Przeglądaj bazę studentów</p>
          </Card>
        </Link>
        <Link to="/admin/raporty">
          <Card hover className="bg-white h-full flex flex-col justify-center items-center text-center p-8">
            <div className="text-5xl mb-4">📊</div>
            <h3 className="text-2xl font-bold text-gray-800">Raporty</h3>
            <p className="text-gray-500 mt-2">Analiza wyników i statystyki</p>
          </Card>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
           <h3 className="font-bold text-lg mb-6">Aktywność Użytkowników (Rozwiązane Egzaminy)</h3>
           {loading ? <Spinner /> : (
               <div className="flex items-end justify-between h-40 space-x-2">
                 {stats.map((s, i) => (
                    <div key={i} className="flex flex-col items-center w-full group">
                       <div className="w-full relative flex items-end justify-center">
                          <div 
                            className="w-full bg-indigo-100 rounded-t-md hover:bg-indigo-300 transition-all relative group-hover:shadow-md"
                            style={{ height: `${(s.value / maxVal) * 120}px`, minHeight: s.value > 0 ? '4px' : '0' }}
                          >
                             <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition">
                                {s.value}
                             </div>
                          </div>
                       </div>
                       <span className="text-xs text-gray-500 mt-2">{s.label}</span>
                    </div>
                 ))}
                 {stats.length === 0 && <p className="w-full text-center text-gray-400 text-sm">Brak danych z ostatniego tygodnia.</p>}
               </div>
           )}
        </Card>
        
        <Card>
            <h3 className="font-bold text-lg mb-4">Szybkie Akcje</h3>
            <div className="space-y-3">
                <Link to="/admin/kursy" className="block p-3 bg-gray-50 rounded hover:bg-indigo-50 flex justify-between items-center transition">
                    <span>Dodaj nowy materiał dydaktyczny</span>
                    <span className="text-indigo-600 font-bold">+</span>
                </Link>
                <Link to="/admin/users" className="block p-3 bg-gray-50 rounded hover:bg-indigo-50 flex justify-between items-center transition">
                    <span>Zarządzaj studentami</span>
                    <span className="text-indigo-600 font-bold">&rarr;</span>
                </Link>
                <div className="p-4 bg-yellow-50 rounded text-sm text-yellow-800">
                    💡 Pamiętaj, aby regularnie sprawdzać raporty trudności pytań.
                </div>
            </div>
        </Card>
      </div>
    </div>
  );
};

// ------------------- USERS -------------------
export const AdminUsers = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const { user: currentUser } = useAuth();
  
  // Modal state
  const [modal, setModal] = useState({ open: false, type: '', userId: 0, userName: '' });

  const fetchUsers = () => {
    setLoading(true);
    authService.getUsers().then(data => {
        setUsers(Array.isArray(data) ? data : []);
    }).catch(err => {
        console.error(err);
        setUsers([]);
    }).finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handlePromote = async () => {
    try {
        await authService.promoteToAdmin(modal.userId);
        fetchUsers();
    } catch (e) {
        alert('Błąd podczas awansowania użytkownika.');
    }
  };

  const handleBan = async () => {
    try {
        await authService.toggleUserBan(modal.userId);
        fetchUsers();
    } catch (e) {
        alert('Błąd podczas zmiany statusu blokady.');
    }
  };

  const handleDelete = async () => {
    try {
        await authService.deleteUser(modal.userId);
        fetchUsers();
    } catch (e) {
        alert('Błąd podczas usuwania użytkownika.');
    }
  };

  const filteredUsers = users.filter(u => 
    u.username.toLowerCase().includes(searchTerm.toLowerCase()) || 
    (u.email && u.email.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <AdminLayout title="Zarządzanie Użytkownikami" backLink="/admin">
      <ConfirmationModal 
        isOpen={modal.open}
        onClose={() => setModal({...modal, open: false})}
        onConfirm={modal.type === 'promote' ? handlePromote : modal.type === 'ban' ? handleBan : handleDelete}
        title={modal.type === 'promote' ? 'Awansuj na Admina' : modal.type === 'ban' ? 'Zmień status blokady' : 'Usuń użytkownika'}
        message={`Czy na pewno chcesz wykonać tę akcję na użytkowniku ${modal.userName}?`}
        confirmLabel={modal.type === 'delete' ? 'Usuń trwale' : 'Wykonaj'}
      />

      <div className="mb-4 max-w-md">
        <Input 
          placeholder="Szukaj użytkownika..." 
          value={searchTerm}
          onChange={(e: any) => setSearchTerm(e.target.value)}
        />
      </div>

      {loading ? <Spinner /> : (
        <Card className="overflow-hidden p-0">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-50 text-xs uppercase text-gray-500 font-semibold">
              <tr>
                <th className="p-4">ID</th>
                <th className="p-4">Nazwa</th>
                <th className="p-4">Rola / Status</th>
                <th className="p-4 text-right">Akcje</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 text-sm">
              {filteredUsers.map(u => (
                <tr key={u.id} className="hover:bg-gray-50">
                  <td className="p-4">{u.id}</td>
                  <td className="p-4">
                      <div className="font-medium text-gray-900">{u.username}</div>
                      <div className="text-xs text-gray-400">{u.email}</div>
                  </td>
                  <td className="p-4">
                    <div className="flex flex-col space-y-1">
                      <Badge color={isUserAdmin(u) ? 'red' : 'green'}>
                        {isUserAdmin(u) ? 'Admin' : 'Student'}
                      </Badge>
                      {u.is_active === false && <Badge color="red">Zablokowany</Badge>}
                    </div>
                  </td>
                  <td className="p-4 text-right space-x-1">
                    {!isUserAdmin(u) && (
                      <button 
                        onClick={() => setModal({ open: true, type: 'promote', userId: u.id, userName: u.username })}
                        className="text-xs bg-indigo-50 text-indigo-600 px-2 py-1 rounded hover:bg-indigo-100 transition"
                        title="Awansuj"
                      >
                        ↑ Admin
                      </button>
                    )}
                    {currentUser?.id !== u.id && (
                      <>
                        <button 
                          onClick={() => setModal({ open: true, type: 'ban', userId: u.id, userName: u.username })}
                          className={`text-xs px-2 py-1 rounded transition ${u.is_active === false ? 'bg-green-50 text-green-600 hover:bg-green-100' : 'bg-orange-50 text-orange-600 hover:bg-orange-100'}`}
                        >
                          {u.is_active === false ? 'Odblokuj' : 'Ban'}
                        </button>
                        <button 
                          onClick={() => setModal({ open: true, type: 'delete', userId: u.id, userName: u.username })}
                          className="text-xs bg-red-50 text-red-600 px-2 py-1 rounded hover:bg-red-100 transition"
                        >
                          🗑
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}
    </AdminLayout>
  );
};

// ------------------- COURSES CRUD -------------------
export const AdminKursy = () => {
  const [kursy, setKursy] = useState<Kurs[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentKurs, setCurrentKurs] = useState<Partial<Kurs>>({ nazwa_kursu: '' });
  const [searchTerm, setSearchTerm] = useState('');
  
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [kursToDelete, setKursToDelete] = useState<number | null>(null);

  const fetchKursy = () => kursService.getAll().then(data => setKursy(Array.isArray(data) ? data : []));
  
  useEffect(() => { fetchKursy(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (currentKurs.id) {
      await kursService.update(currentKurs.id, currentKurs);
    } else {
      await kursService.create(currentKurs);
    }
    setIsEditing(false);
    setCurrentKurs({ nazwa_kursu: '' });
    fetchKursy();
  };

  const handleDeleteClick = (id: number) => {
      setKursToDelete(id);
      setDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    if (kursToDelete) {
      await kursService.delete(kursToDelete);
      fetchKursy();
      setKursToDelete(null);
    }
  };

  const filteredKursy = kursy.filter(k => 
    k.nazwa_kursu.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <AdminLayout 
      title="Zarządzanie Kursami" 
      backLink="/admin"
      actions={<Button onClick={() => setIsEditing(true)}>+ Dodaj Kurs</Button>}
    >
      <ConfirmationModal 
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDelete}
        title="Usuwanie Kursu"
        message="Czy na pewno chcesz usunąć ten kurs?"
      />

      {isEditing && (
        <Card className="mb-6 bg-gray-50 border-indigo-200">
          <h3 className="font-bold mb-4">{currentKurs.id ? 'Edytuj Kurs' : 'Nowy Kurs'}</h3>
          <form onSubmit={handleSubmit} className="flex gap-4 items-end">
            <div className="flex-grow">
              <Input 
                label="Nazwa Kursu" 
                value={currentKurs.nazwa_kursu} 
                onChange={(e: any) => setCurrentKurs({...currentKurs, nazwa_kursu: e.target.value})} 
                required 
              />
            </div>
            <div className="mb-4 space-x-2">
              <Button type="submit">Zapisz</Button>
              <Button type="button" variant="ghost" onClick={() => { setIsEditing(false); setCurrentKurs({nazwa_kursu:''}); }}>Anuluj</Button>
            </div>
          </form>
        </Card>
      )}

      <div className="mb-4 max-w-md">
        <Input 
            placeholder="Szukaj kursu..." 
            value={searchTerm}
            onChange={(e: any) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="grid gap-4">
        {filteredKursy.map(k => (
          <Card key={k.id} className="flex justify-between items-center py-4">
            <span className="font-semibold text-lg">{k.nazwa_kursu}</span>
            <div className="space-x-2 flex items-center">
              <Link to={`/admin/kursy/${k.id}/rozdzialy`}>
                <Button variant="secondary" className="text-sm">Rozdziały</Button>
              </Link>
              <Link to={`/admin/kursy/${k.id}/artykuly`}>
                <Button variant="secondary" className="text-sm">Artykuły</Button>
              </Link>
              <Button variant="ghost" onClick={() => { setCurrentKurs(k); setIsEditing(true); }}>Edytuj</Button>
              <Button variant="danger" onClick={() => handleDeleteClick(k.id)}>Usuń</Button>
            </div>
          </Card>
        ))}
      </div>
    </AdminLayout>
  );
};

// ------------------- CHAPTERS CRUD -------------------
export const AdminRozdzialy = () => {
  const { kursId } = useParams<{ kursId: string }>();
  const [rozdzialy, setRozdzialy] = useState<Rozdzial[]>([]);
  const [kurs, setKurs] = useState<Kurs | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [currentRozdzial, setCurrentRozdzial] = useState<Partial<Rozdzial>>({ nazwa_rozdzialu: '' });
  
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<number | null>(null);

  const fetchData = async () => {
    if (!kursId) return;
    const k = await kursService.getOne(kursId); 
    setKurs(Array.isArray(k) ? k[0] : k); 
    const r = await kursService.getRozdzialy(kursId);
    setRozdzialy(Array.isArray(r) ? r : []);
  };

  useEffect(() => { fetchData(); }, [kursId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!kursId) return;
    const payload = { ...currentRozdzial, kurs_id: parseInt(kursId) };
    
    if (currentRozdzial.id) {
      await kursService.updateRozdzial(currentRozdzial.id, payload);
    } else {
      await kursService.createRozdzial(parseInt(kursId), payload);
    }
    setIsEditing(false);
    setCurrentRozdzial({ nazwa_rozdzialu: '' });
    fetchData();
  };

  const handleDeleteClick = (id: number) => {
      setItemToDelete(id);
      setDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    if (itemToDelete) {
      await kursService.deleteRozdzial(itemToDelete);
      fetchData();
      setItemToDelete(null);
    }
  };

  return (
    <AdminLayout 
      title={`Rozdziały: ${kurs?.nazwa_kursu || '...'}`} 
      backLink="/admin/kursy"
      actions={<Button onClick={() => setIsEditing(true)}>+ Dodaj Rozdział</Button>}
    >
       <ConfirmationModal 
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDelete}
        title="Usuwanie Rozdziału"
        message="Czy na pewno chcesz usunąć ten rozdział?"
      />

       {isEditing && (
        <Card className="mb-6 bg-gray-50 border-indigo-200">
          <h3 className="font-bold mb-4">{currentRozdzial.id ? 'Edytuj Rozdział' : 'Nowy Rozdział'}</h3>
          <form onSubmit={handleSubmit} className="flex gap-4 items-end">
            <div className="flex-grow">
              <Input 
                label="Nazwa Rozdziału" 
                value={currentRozdzial.nazwa_rozdzialu} 
                onChange={(e: any) => setCurrentRozdzial({...currentRozdzial, nazwa_rozdzialu: e.target.value})} 
                required 
              />
            </div>
            <div className="mb-4 space-x-2">
              <Button type="submit">Zapisz</Button>
              <Button type="button" variant="ghost" onClick={() => { setIsEditing(false); setCurrentRozdzial({nazwa_rozdzialu:''}); }}>Anuluj</Button>
            </div>
          </form>
        </Card>
      )}

      <div className="space-y-4">
        {rozdzialy.length === 0 && <p className="text-gray-500">Brak rozdziałów.</p>}
        {rozdzialy.map(r => (
           <Card key={r.id} className="flex justify-between items-center py-3">
             <span className="font-medium">{r.nazwa_rozdzialu}</span>
             <div className="space-x-2">
                <Button variant="ghost" onClick={() => { setCurrentRozdzial(r); setIsEditing(true); }}>Edytuj</Button>
                <Button variant="danger" onClick={() => handleDeleteClick(r.id)}>Usuń</Button>
             </div>
           </Card>
        ))}
      </div>
    </AdminLayout>
  );
};

// ------------------- ARTICLES CRUD -------------------
export const AdminArtykuly = () => {
  const { kursId } = useParams<{ kursId: string }>();
  const [artykuly, setArtykuly] = useState<any[]>([]);
  const [rozdzialy, setRozdzialy] = useState<Rozdzial[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentArt, setCurrentArt] = useState<Partial<Artykul>>({ tytul: '', tresc: '', nr_artykulu: '', rozdzial_id: 0 });
  
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<number | null>(null);

  const fetchData = async () => {
    if (!kursId) return;

    try {
        const rozds = await kursService.getRozdzialy(kursId);
        setRozdzialy(Array.isArray(rozds) ? rozds : []);
    } catch (e) {
        setRozdzialy([]);
    }

    try {
        const arts = await kursService.getArtykuly(kursId);
        if (Array.isArray(arts)) {
            const uniqueArts = Array.from(new Map(arts.map(item => [item.artykul_id || item.id, item])).values());
            setArtykuly(uniqueArts);
        } else {
            setArtykuly([]);
        }
    } catch (e) {
        setArtykuly([]);
    }
  };

  useEffect(() => { fetchData(); }, [kursId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!kursId) return;
    
    const payload = {
      tytul: currentArt.tytul,
      tresc: currentArt.tresc,
      nr_artykulu: currentArt.nr_artykulu,
      rozdzial_id: currentArt.rozdzial_id || (rozdzialy.length > 0 ? rozdzialy[0].id : 0)
    };

    if (currentArt.id) {
      await kursService.updateArtykul(currentArt.id, payload);
    } else {
      await kursService.createArtykul(parseInt(kursId), payload);
    }
    setIsEditing(false);
    setCurrentArt({ tytul: '', tresc: '', nr_artykulu: '', rozdzial_id: 0 });
    fetchData();
  };

  const handleDeleteClick = (id: number) => {
      setItemToDelete(id);
      setDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    if (itemToDelete) {
      await kursService.deleteArtykul(itemToDelete);
      fetchData();
      setItemToDelete(null);
    }
  };

  const handleEdit = async (art: any) => {
    const realId = art.artykul_id || art.id;
    try {
        const detail = await kursService.getArtykulDetail(realId.toString());
        setCurrentArt({
          id: detail.id,
          tytul: detail.tytul,
          tresc: detail.tresc,
          nr_artykulu: detail.nr_artykulu || '1', 
          rozdzial_id: detail.rozdzial_id || (rozdzialy.length > 0 ? rozdzialy[0].id : 0)
        });
        setIsEditing(true);
    } catch (e) {
        setCurrentArt({
          id: realId,
          tytul: art.tytul,
          tresc: art.tresc,
          nr_artykulu: art.nr_artykulu || '1', 
          rozdzial_id: art.rozdzial_id || (rozdzialy.length > 0 ? rozdzialy[0].id : 0)
        });
        setIsEditing(true);
    }
  };

  return (
    <AdminLayout 
      title="Zarządzanie Artykułami" 
      backLink="/admin/kursy"
      actions={<Button onClick={() => setIsEditing(true)}>+ Dodaj Artykuł</Button>}
    >
      <ConfirmationModal 
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDelete}
        title="Usuwanie Artykułu"
        message="Czy na pewno chcesz usunąć ten artykuł?"
      />

      {isEditing && (
        <Card className="mb-6 bg-gray-50 border-indigo-200">
           <h3 className="font-bold mb-4">{currentArt.id ? 'Edytuj' : 'Nowy'} Artykuł</h3>
           <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <Input label="Tytuł" value={currentArt.tytul} onChange={(e:any) => setCurrentArt({...currentArt, tytul: e.target.value})} required />
                <Input label="Nr Artykułu" value={currentArt.nr_artykulu} onChange={(e:any) => setCurrentArt({...currentArt, nr_artykulu: e.target.value})} required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Rozdział</label>
                <select 
                  className="w-full p-2 border rounded"
                  value={currentArt.rozdzial_id}
                  onChange={(e) => setCurrentArt({...currentArt, rozdzial_id: parseInt(e.target.value)})}
                >
                  <option value={0}>Wybierz rozdział...</option>
                  {rozdzialy.map(r => <option key={r.id} value={r.id}>{r.nazwa_rozdzialu}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Treść (HTML)</label>
                <textarea 
                  className="w-full p-2 border rounded h-32 font-mono text-sm" 
                  value={currentArt.tresc}
                  onChange={(e) => setCurrentArt({...currentArt, tresc: e.target.value})}
                  required
                />
              </div>
              <div className="flex space-x-2">
                <Button type="submit">Zapisz</Button>
                <Button type="button" variant="ghost" onClick={() => { setIsEditing(false); setCurrentArt({tytul: '', tresc: '', nr_artykulu: '', rozdzial_id: 0}); }}>Anuluj</Button>
              </div>
           </form>
        </Card>
      )}

      <div className="space-y-3">
        {artykuly.map(a => {
            const displayId = a.artykul_id || a.id;
            return (
              <Card key={displayId} className="flex justify-between items-center py-3">
                 <div>
                   <span className="text-xs text-gray-500 block">ID: {displayId}</span>
                   <span className="font-medium">Art. {a.nr_artykulu || '?'} - {a.tytul || `Artykuł ${displayId}`}</span>
                 </div>
                 <div className="space-x-2">
                    <Link to={`/admin/artykuly/${displayId}/pytania`}>
                      <Button variant="secondary" className="text-xs">Pytania</Button>
                    </Link>
                    <Button variant="ghost" onClick={() => handleEdit(a)}>Edytuj</Button>
                    <Button variant="danger" onClick={() => handleDeleteClick(displayId)}>Usuń</Button>
                 </div>
              </Card>
            );
        })}
      </div>
    </AdminLayout>
  );
};

// ------------------- QUESTIONS (PYTANIA) CRUD -------------------
export const AdminPytania = () => {
  const { artykulId } = useParams<{ artykulId: string }>();
  const [pytania, setPytania] = useState<Pytanie[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentPytanie, setCurrentPytanie] = useState<Partial<Pytanie>>({ tresc: '' });
  
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<number | null>(null);

  const fetchData = async () => {
    if (!artykulId) return;
    try {
      const data = await contentAdminService.getPytaniaByArtykul(parseInt(artykulId));
      setPytania(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error(e);
      setPytania([]);
    }
  };

  useEffect(() => { fetchData(); }, [artykulId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!artykulId) return;
    const payload = { ...currentPytanie, artykul_id: parseInt(artykulId) };

    if (currentPytanie.id) {
      await contentAdminService.updatePytanie(currentPytanie.id, payload);
    } else {
      await contentAdminService.createPytanie(payload);
    }
    setIsEditing(false);
    setCurrentPytanie({ tresc: '' });
    fetchData();
  };

  const handleDeleteClick = (id: number) => {
      setItemToDelete(id);
      setDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    if (itemToDelete) {
      await contentAdminService.deletePytanie(itemToDelete);
      fetchData();
      setItemToDelete(null);
    }
  };

  return (
    <AdminLayout 
      title={`Pytania do art. ID: ${artykulId}`} 
      backLink="/admin/kursy"
      actions={<Button onClick={() => setIsEditing(true)}>+ Dodaj Pytanie</Button>}
    >
      <ConfirmationModal 
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDelete}
        title="Usuwanie Pytania"
        message="Czy na pewno chcesz usunąć to pytanie?"
      />

      {isEditing && (
        <Card className="mb-6 bg-gray-50 border-indigo-200">
          <h3 className="font-bold mb-4">{currentPytanie.id ? 'Edytuj' : 'Nowe'} Pytanie</h3>
          <form onSubmit={handleSubmit} className="flex gap-4 items-end">
            <div className="flex-grow">
              <Input 
                label="Treść Pytania" 
                value={currentPytanie.tresc} 
                onChange={(e: any) => setCurrentPytanie({...currentPytanie, tresc: e.target.value})} 
                required 
              />
            </div>
            <div className="mb-4 space-x-2">
              <Button type="submit">Zapisz</Button>
              <Button type="button" variant="ghost" onClick={() => { setIsEditing(false); setCurrentPytanie({tresc:''}); }}>Anuluj</Button>
            </div>
          </form>
        </Card>
      )}

      <div className="space-y-3">
        {pytania.length === 0 && <p className="text-gray-500">Brak pytań.</p>}
        {pytania.map(p => (
          <Card key={p.id} className="flex justify-between items-center py-3">
            <span className="font-medium">{p.tresc}</span>
            <div className="space-x-2">
               <Link to={`/admin/pytania/${p.id}/odpowiedzi`}>
                 <Button variant="secondary" className="text-xs">Odpowiedzi</Button>
               </Link>
               <Button variant="ghost" onClick={() => { setCurrentPytanie(p); setIsEditing(true); }}>Edytuj</Button>
               <Button variant="danger" onClick={() => handleDeleteClick(p.id)}>Usuń</Button>
            </div>
          </Card>
        ))}
      </div>
    </AdminLayout>
  );
};

// ------------------- ANSWERS (ODPOWIEDZI) CRUD -------------------
export const AdminOdpowiedzi = () => {
  const { pytanieId } = useParams<{ pytanieId: string }>();
  const [odpowiedzi, setOdpowiedzi] = useState<Odpowiedz[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentOdp, setCurrentOdp] = useState<Partial<Odpowiedz>>({ tresc: '', poprawna: false });
  const [parentPytanie, setParentPytanie] = useState<Pytanie | null>(null);
  
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<number | null>(null);

  const fetchData = async () => {
    if (!pytanieId) return;
    try {
      const data = await contentAdminService.getOdpowiedzi(parseInt(pytanieId));
      setOdpowiedzi(Array.isArray(data) ? data : []);
      
      const pytData = await contentAdminService.getPytanie(parseInt(pytanieId));
      setParentPytanie(pytData);
    } catch (e) {
      console.error(e);
      setOdpowiedzi([]);
    }
  };

  useEffect(() => { fetchData(); }, [pytanieId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pytanieId) return;
    const payload = { ...currentOdp, pytanie_id: parseInt(pytanieId) };

    if (currentOdp.id) {
      await contentAdminService.updateOdpowiedz(currentOdp.id, payload);
    } else {
      await contentAdminService.createOdpowiedz(payload);
    }
    setIsEditing(false);
    setCurrentOdp({ tresc: '', poprawna: false });
    fetchData();
  };

  const handleDeleteClick = (id: number) => {
      setItemToDelete(id);
      setDeleteModalOpen(true);
  };

  const confirmDelete = async () => {
    if (itemToDelete) {
      await contentAdminService.deleteOdpowiedz(itemToDelete);
      fetchData();
      setItemToDelete(null);
    }
  };

  return (
    <AdminLayout 
      title={`Odpowiedzi do pytania ID: ${pytanieId}`} 
      backLink={parentPytanie ? `/admin/artykuly/${parentPytanie.artykul_id}/pytania` : '/admin/kursy'}
      actions={<Button onClick={() => setIsEditing(true)}>+ Dodaj Odpowiedź</Button>}
    >
      <ConfirmationModal 
        isOpen={deleteModalOpen}
        onClose={() => setDeleteModalOpen(false)}
        onConfirm={confirmDelete}
        title="Usuwanie Odpowiedzi"
        message="Czy na pewno chcesz usunąć tę odpowiedź?"
      />

      {isEditing && (
        <Card className="mb-6 bg-gray-50 border-indigo-200">
          <h3 className="font-bold mb-4">{currentOdp.id ? 'Edytuj' : 'Nowa'} Odpowiedź</h3>
          <form onSubmit={handleSubmit} className="flex gap-4 items-end">
            <div className="flex-grow">
              <Input 
                label="Treść Odpowiedzi" 
                value={currentOdp.tresc} 
                onChange={(e: any) => setCurrentOdp({...currentOdp, tresc: e.target.value})} 
                required 
              />
            </div>
            <div className="mb-4">
              <label className="flex items-center space-x-2">
                <input 
                  type="checkbox" 
                  checked={currentOdp.poprawna}
                  onChange={(e) => setCurrentOdp({...currentOdp, poprawna: e.target.checked})}
                  className="w-5 h-5 text-indigo-600 rounded"
                />
                <span className="text-sm font-bold text-gray-700">Poprawna</span>
              </label>
            </div>
            <div className="mb-4 space-x-2">
              <Button type="submit">Zapisz</Button>
              <Button type="button" variant="ghost" onClick={() => { setIsEditing(false); setCurrentOdp({tresc: '', poprawna: false}); }}>Anuluj</Button>
            </div>
          </form>
        </Card>
      )}

      <div className="space-y-3">
        {odpowiedzi.length === 0 && <p className="text-gray-500">Brak odpowiedzi.</p>}
        {odpowiedzi.map(o => (
          <Card key={o.id} className="flex justify-between items-center py-3">
            <div className="flex items-center space-x-3">
              <span className={`w-3 h-3 rounded-full ${o.poprawna ? 'bg-green-500' : 'bg-red-300'}`}></span>
              <span className="font-medium">{o.tresc}</span>
              {o.poprawna && <Badge color="green">Poprawna</Badge>}
            </div>
            <div className="space-x-2">
               <Button variant="ghost" onClick={() => { setCurrentOdp(o); setIsEditing(true); }}>Edytuj</Button>
               <Button variant="danger" onClick={() => handleDeleteClick(o.id)}>Usuń</Button>
            </div>
          </Card>
        ))}
      </div>
    </AdminLayout>
  );
};

// ------------------- REPORTS -------------------
export const AdminReports = () => {
  const [activeTab, setActiveTab] = useState('wyniki');
  const [results, setResults] = useState<WynikEgzaminu[]>([]);
  const [courseStats, setCourseStats] = useState<any[]>([]);
  const [questionStats, setQuestionStats] = useState<any[]>([]);
  const [userMap, setUserMap] = useState<{[key:number]: string}>({});
  const [loading, setLoading] = useState(false);
  const [sortConfig, setSortConfig] = useState<{ key: string, direction: 'asc' | 'desc' } | null>(null);

  useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
        try {
            if (activeTab === 'wyniki') {
                const [allResults, allUsers] = await Promise.all([
                    wynikiService.getAllAdmin(),
                    authService.getUsers()
                ]);
                
                const uMap: {[key:number]: string} = {};
                if (Array.isArray(allUsers)) {
                    allUsers.forEach((u: any) => uMap[u.id] = u.username);
                }
                setUserMap(uMap);
                setResults(Array.isArray(allResults) ? allResults : []);
            } else if (activeTab === 'kursy_stats') {
                const [kursy, wyniki] = await Promise.all([
                    kursService.getAll(),
                    wynikiService.getAllAdmin()
                ]);
                
                const safeKursy = Array.isArray(kursy) ? kursy : [];
                const safeWyniki = Array.isArray(wyniki) ? wyniki : [];

                const stats = safeKursy.map(k => {
                    const kWyniki = safeWyniki.filter(w => w.kurs_id === k.id);
                    const avg = kWyniki.length > 0 
                        ? kWyniki.reduce((acc, curr) => acc + Number(curr.wynik || 0), 0) / kWyniki.length
                        : 0;
                    return {
                        id: k.id,
                        name: k.nazwa_kursu,
                        count: kWyniki.length,
                        avg: Number(avg).toFixed(1)
                    };
                });
                setCourseStats(stats);
            } else if (activeTab === 'trudnosc') {
                const [pytania, allStats] = await Promise.all([
                    kursService.getAllPytania(),
                    wynikiService.getAllStats()
                ]);
                
                const safePytania = Array.isArray(pytania) ? pytania : [];
                const safeStats = Array.isArray(allStats) ? allStats : [];

                const statsMap: {[key: number]: StatystykiPytania} = {};
                safeStats.forEach((s: StatystykiPytania) => {
                    statsMap[s.pytanie_id] = s;
                });

                const stats = safePytania.map((p: Pytanie) => {
                    const s = statsMap[p.id];
                    return {
                        id: p.id,
                        artykul_id: p.artykul_id,
                        tresc: p.tresc,
                        ilosc: s ? s.ilosc_odpowiedzi : 0,
                        poprawne: s ? s.poprawne_odpowiedzi : 0,
                        procent: s ? parseFloat(s.procent_poprawnych || '0') : 0
                    };
                });
                
                stats.sort((a, b) => a.procent - b.procent);
                setQuestionStats(stats);
            }
        } catch (e) {
            console.error(e);
            setResults([]);
            setCourseStats([]);
            setQuestionStats([]);
        } finally {
            setLoading(false);
        }
    };
    fetchData();
  }, [activeTab]);

  const handleSort = (key: string) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });

    if (activeTab === 'trudnosc') {
        setQuestionStats(prev => {
            const sorted = [...prev].sort((a, b) => {
                if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
                if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
                return 0;
            });
            return sorted;
        });
    }
  };

  const renderSortArrow = (key: string) => {
      if (!sortConfig || sortConfig.key !== key) return <span className="text-gray-300">↕</span>;
      return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  return (
    <AdminLayout title="Raporty i Analizy" backLink="/admin">
      <div className="flex space-x-4 border-b mb-6 overflow-x-auto">
        <button 
            className={`pb-2 px-4 font-medium transition-colors whitespace-nowrap ${activeTab === 'wyniki' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('wyniki')}
        >
            Wyniki Egzaminów
        </button>
        <button 
            className={`pb-2 px-4 font-medium transition-colors whitespace-nowrap ${activeTab === 'kursy_stats' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('kursy_stats')}
        >
            Statystyki Kursów
        </button>
        <button 
            className={`pb-2 px-4 font-medium transition-colors whitespace-nowrap ${activeTab === 'trudnosc' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setActiveTab('trudnosc')}
        >
            Trudność Pytań
        </button>
      </div>

      {loading ? <Spinner /> : (
        <Card className="overflow-hidden p-0">
           {activeTab === 'wyniki' && (
             <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead className="bg-gray-50 text-xs uppercase text-gray-500 font-semibold">
                    <tr>
                        <th className="p-4">Data</th>
                        <th className="p-4">Kurs ID</th>
                        <th className="p-4">Student</th>
                        <th className="p-4">Wynik</th>
                    </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 text-sm">
                    {results.map(r => (
                        <tr key={r.id} className="hover:bg-gray-50">
                        <td className="p-4">{r.data_zapisu ? new Date(r.data_zapisu).toLocaleDateString() : '-'}</td>
                        <td className="p-4">#{r.kurs_id}</td>
                        <td className="p-4 font-medium text-gray-800">
                             {userMap[r.uzytkownik_id] || `ID: ${r.uzytkownik_id}`}
                        </td>
                        <td className="p-4">
                            <Badge color={Number(r.wynik || 0) >= 50 ? 'green' : 'red'}>{Math.round(Number(r.wynik || 0))}%</Badge>
                        </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
             </div>
           )}

           {activeTab === 'kursy_stats' && (
              <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead className="bg-gray-50 text-xs uppercase text-gray-500 font-semibold">
                        <tr>
                            <th className="p-4">Nazwa Kursu</th>
                            <th className="p-4">Rozwiązanych egzaminów</th>
                            <th className="p-4">Średni wynik</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 text-sm">
                        {courseStats.map(s => (
                            <tr key={s.id} className="hover:bg-gray-50">
                                <td className="p-4 font-medium">{s.name}</td>
                                <td className="p-4">{s.count}</td>
                                <td className="p-4 font-bold text-indigo-600">{s.avg}%</td>
                            </tr>
                        ))}
                    </tbody>
                  </table>
              </div>
           )}

           {activeTab === 'trudnosc' && (
             <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead className="bg-gray-50 text-xs uppercase text-gray-500 font-semibold">
                    <tr>
                        <th className="p-4">Pytanie</th>
                        <th className="p-4 cursor-pointer hover:text-indigo-600" onClick={() => handleSort('ilosc')}>Próby {renderSortArrow('ilosc')}</th>
                        <th className="p-4 cursor-pointer hover:text-indigo-600" onClick={() => handleSort('procent')}>Skuteczność {renderSortArrow('procent')}</th>
                    </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 text-sm">
                    {questionStats.map(s => (
                        <tr key={s.id} className="hover:bg-gray-50">
                            <td className="p-4 max-w-xs truncate" title={s.tresc}>{s.tresc}</td>
                            <td className="p-4">{s.ilosc}</td>
                            <td className="p-4">
                                <div className="flex items-center space-x-2">
                                    <div className="w-24 bg-gray-200 rounded-full h-1.5 overflow-hidden">
                                        <div 
                                            className={`h-full ${s.procent > 70 ? 'bg-green-500' : s.procent > 40 ? 'bg-yellow-500' : 'bg-red-500'}`} 
                                            style={{ width: `${s.procent}%` }}
                                        ></div>
                                    </div>
                                    <span className="font-bold">{s.procent}%</span>
                                </div>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
             </div>
           )}
        </Card>
      )}
    </AdminLayout>
  );
};
