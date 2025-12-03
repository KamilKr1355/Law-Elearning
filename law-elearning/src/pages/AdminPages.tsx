
import React, { useEffect, useState } from 'react';
import { Card, Button, Input, Spinner, Badge } from '../components/UI';
import { kursService, authService, contentAdminService, wynikiService } from '../services/api';
import { Link, useParams } from 'react-router-dom';
import type { Kurs, Rozdzial, Artykul, Pytanie, Odpowiedz, WynikEgzaminu, StatystykiPytania } from '../types';
import { isUserAdmin } from '../utils/auth';

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
  // Real stats based on 'WynikiEgzaminu' (ALL USERS)
  const [stats, setStats] = useState<{label: string, value: number}[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Używamy getAllAdmin, żeby wykres pokazywał ruch wszystkich, a nie tylko Twój
    wynikiService.getAllAdmin().then(data => {
        // Safe array
        const results = Array.isArray(data) ? data : [];
        
        // Generate last 7 days labels
        const last7Days = [...Array(7)].map((_, i) => {
            const d = new Date();
            d.setDate(d.getDate() - (6 - i));
            return d.toISOString().split('T')[0]; // YYYY-MM-DD
        });

        const chartData = last7Days.map(dateStr => {
            // Count results that start with this date string
            const count = results.filter(w => w.data_zapisu && w.data_zapisu.startsWith(dateStr)).length;
            const labelDate = new Date(dateStr);
            // Format label as "DD.MM" (e.g., 02.12)
            const label = `${String(labelDate.getDate()).padStart(2, '0')}.${String(labelDate.getMonth() + 1).padStart(2, '0')}`;
            return { label, value: count };
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
                    <span>Weryfikuj nowych użytkowników</span>
                    <span className="text-indigo-600 font-bold">&rarr;</span>
                </Link>
                <div className="p-4 bg-yellow-50 rounded text-sm text-yellow-800">
                    💡 Pamiętaj, aby regularnie sprawdzać komentarze pod artykułami.
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
  
  useEffect(() => {
    authService.getUsers().then(data => {
        // Safe check
        setUsers(Array.isArray(data) ? data : []);
    }).catch(err => {
        console.error(err);
        setUsers([]);
    });
  }, []);

  const filteredUsers = users.filter(u => 
    u.username.toLowerCase().includes(searchTerm.toLowerCase()) || 
    (u.email && u.email.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <AdminLayout title="Użytkownicy" backLink="/admin">
      <div className="mb-4 max-w-md">
        <Input 
          placeholder="Szukaj użytkownika po nazwie lub email..." 
          value={searchTerm}
          onChange={(e: any) => setSearchTerm(e.target.value)}
        />
      </div>

      <Card className="overflow-hidden p-0">
        <table className="w-full text-left border-collapse">
          <thead className="bg-gray-50 text-xs uppercase text-gray-500 font-semibold">
            <tr>
              <th className="p-4">ID</th>
              <th className="p-4">Nazwa</th>
              <th className="p-4">Email</th>
              <th className="p-4">Rola</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 text-sm">
            {filteredUsers.map(u => (
              <tr key={u.id} className="hover:bg-gray-50">
                <td className="p-4">{u.id}</td>
                <td className="p-4 font-medium">{u.username}</td>
                <td className="p-4">{u.email}</td>
                <td className="p-4">
                  <Badge color={isUserAdmin(u) ? 'red' : 'green'}>
                    {isUserAdmin(u) ? 'Admin' : 'Student'}
                  </Badge>
                </td>
              </tr>
            ))}
            {filteredUsers.length === 0 && (
                <tr>
                    <td colSpan={4} className="p-4 text-center text-gray-500">Brak wyników wyszukiwania.</td>
                </tr>
            )}
          </tbody>
        </table>
      </Card>
    </AdminLayout>
  );
};

// ------------------- COURSES CRUD -------------------
export const AdminKursy = () => {
  const [kursy, setKursy] = useState<Kurs[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentKurs, setCurrentKurs] = useState<Partial<Kurs>>({ nazwa_kursu: '' });
  const [searchTerm, setSearchTerm] = useState('');

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

  const handleDelete = async (id: number) => {
    if (window.confirm('Czy na pewno usunąć ten kurs?')) {
      await kursService.delete(id);
      fetchKursy();
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
              <Button variant="danger" onClick={() => handleDelete(k.id)}>Usuń</Button>
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

  const handleDelete = async (id: number) => {
    if (confirm('Usunąć rozdział?')) {
      await kursService.deleteRozdzial(id);
      fetchData();
    }
  };

  return (
    <AdminLayout 
      title={`Rozdziały: ${kurs?.nazwa_kursu || '...'}`} 
      backLink="/admin/kursy"
      actions={<Button onClick={() => setIsEditing(true)}>+ Dodaj Rozdział</Button>}
    >
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
                <Button variant="danger" onClick={() => handleDelete(r.id)}>Usuń</Button>
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

  const fetchData = async () => {
    if (!kursId) return;

    // Load chapters independently
    try {
        const rozds = await kursService.getRozdzialy(kursId);
        setRozdzialy(Array.isArray(rozds) ? rozds : []);
    } catch (e) {
        setRozdzialy([]);
    }

    // Load articles and deduplicate based on artykul_id if available
    try {
        const arts = await kursService.getArtykuly(kursId);
        if (Array.isArray(arts)) {
            // Deduplication logic: use Map with artykul_id (if available) or id as key
            // This fixes the issue where backend returns identical 'id': 1 for all items
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

    // Use proper ID for update (prefer id from edit state)
    if (currentArt.id) {
      await kursService.updateArtykul(currentArt.id, payload);
    } else {
      await kursService.createArtykul(parseInt(kursId), payload);
    }
    setIsEditing(false);
    setCurrentArt({ tytul: '', tresc: '', nr_artykulu: '', rozdzial_id: 0 });
    fetchData();
  };

  const handleDelete = async (id: number) => {
    if (confirm('Usunąć artykuł?')) {
      await kursService.deleteArtykul(id);
      fetchData();
    }
  };

  const handleEdit = async (art: any) => {
    // Determine the ID to use for fetching details and updating
    // If we have artykul_id, that's likely the real PK
    const realId = art.artykul_id || art.id;
    
    try {
        const detail = await kursService.getArtykulDetail(realId.toString());
        setCurrentArt({
          id: detail.id,
          tytul: detail.tytul,
          tresc: detail.tresc,
          // @ts-ignore
          nr_artykulu: detail.nr_artykulu || '1', 
          // @ts-ignore
          rozdzial_id: detail.rozdzial_id || (rozdzialy.length > 0 ? rozdzialy[0].id : 0)
        });
        setIsEditing(true);
    } catch (e) {
        // Fallback if detail fetch fails, use list data
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
                <Button type="button" variant="ghost" onClick={() => setIsEditing(false)}>Anuluj</Button>
              </div>
           </form>
        </Card>
      )}

      <div className="space-y-3">
        {artykuly.map(a => {
            // Determine display ID and key
            const displayId = a.artykul_id || a.id;
            return (
              <Card key={displayId} className="flex justify-between items-center py-3">
                 <div>
                   <span className="text-xs text-gray-500 block">ID: {displayId}</span>
                   {/* Ensures title is displayed if available */}
                   <span className="font-medium">{a.tytul || `Artykuł ${displayId}`}</span>
                 </div>
                 <div className="space-x-2">
                    <Link to={`/admin/artykuly/${displayId}/pytania`}>
                      <Button variant="secondary" className="text-xs">Pytania</Button>
                    </Link>
                    <Button variant="ghost" onClick={() => handleEdit(a)}>Edytuj</Button>
                    <Button variant="danger" onClick={() => handleDelete(displayId)}>Usuń</Button>
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

  const handleDelete = async (id: number) => {
    if (confirm('Usunąć pytanie?')) {
      await contentAdminService.deletePytanie(id);
      fetchData();
    }
  };

  return (
    <AdminLayout 
      title={`Pytania do art. ID: ${artykulId}`} 
      backLink="/admin/kursy"
      actions={<Button onClick={() => setIsEditing(true)}>+ Dodaj Pytanie</Button>}
    >
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
               <Button variant="danger" onClick={() => handleDelete(p.id)}>Usuń</Button>
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

  const fetchData = async () => {
    if (!pytanieId) return;
    try {
      // Fetch answers
      const data = await contentAdminService.getOdpowiedzi(parseInt(pytanieId));
      setOdpowiedzi(Array.isArray(data) ? data : []);
      
      // Fetch parent question to know where to go back
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

  const handleDelete = async (id: number) => {
    if (confirm('Usunąć odpowiedź?')) {
      await contentAdminService.deleteOdpowiedz(id);
      fetchData();
    }
  };

  return (
    <AdminLayout 
      title={`Odpowiedzi do pytania ID: ${pytanieId}`} 
      backLink={parentPytanie ? `/admin/artykuly/${parentPytanie.artykul_id}/pytania` : '/admin/kursy'}
      actions={<Button onClick={() => setIsEditing(true)}>+ Dodaj Odpowiedź</Button>}
    >
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
               <Button variant="danger" onClick={() => handleDelete(o.id)}>Usuń</Button>
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
  
  // Sorting state for questions
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
                        ? kWyniki.reduce((acc, curr) => acc + curr.wynik, 0) / kWyniki.length
                        : 0;
                    return {
                        id: k.id,
                        name: k.nazwa_kursu,
                        count: kWyniki.length,
                        avg: avg.toFixed(1)
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
                
                // Initial sort
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

    setQuestionStats(prev => {
        const sorted = [...prev].sort((a, b) => {
            if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
            if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
            return 0;
        });
        return sorted;
    });
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
                            <Badge color={r.wynik >= 50 ? 'green' : 'red'}>{r.wynik.toFixed(0)}%</Badge>
                        </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
                {results.length === 0 && <div className="p-8 text-center text-gray-500">Brak danych lub błąd połączenia z API.</div>}
             </div>
           )}

           {activeTab === 'kursy_stats' && (
             <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead className="bg-gray-50 text-xs uppercase text-gray-500 font-semibold">
                    <tr>
                        <th className="p-4">Nazwa Kursu</th>
                        <th className="p-4 text-center">Liczba podejść (Wszyscy)</th>
                        <th className="p-4 text-center">Średnia Ocena</th>
                    </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 text-sm">
                    {courseStats.map(c => (
                        <tr key={c.id} className="hover:bg-gray-50">
                        <td className="p-4 font-medium">{c.name}</td>
                        <td className="p-4 text-center">{c.count}</td>
                        <td className="p-4 text-center">
                            <span className={`font-bold ${parseFloat(c.avg) >= 50 ? 'text-green-600' : 'text-gray-600'}`}>
                                {c.avg}%
                            </span>
                        </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
                {courseStats.length === 0 && <div className="p-8 text-center text-gray-500">Brak danych.</div>}
             </div>
           )}

           {activeTab === 'trudnosc' && (
             <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead className="bg-gray-50 text-xs uppercase text-gray-500 font-semibold select-none">
                    <tr>
                        <th className="p-4 cursor-pointer hover:bg-gray-100" onClick={() => handleSort('id')}>
                            ID {renderSortArrow('id')}
                        </th>
                        <th className="p-4 cursor-pointer hover:bg-gray-100" onClick={() => handleSort('artykul_id')}>
                            Art. ID {renderSortArrow('artykul_id')}
                        </th>
                        <th className="p-4 cursor-pointer hover:bg-gray-100" onClick={() => handleSort('tresc')}>
                            Treść Pytania {renderSortArrow('tresc')}
                        </th>
                        <th className="p-4 text-center cursor-pointer hover:bg-gray-100" onClick={() => handleSort('ilosc')}>
                            Próby {renderSortArrow('ilosc')}
                        </th>
                        <th className="p-4 text-center cursor-pointer hover:bg-gray-100" onClick={() => handleSort('poprawne')}>
                            Poprawne {renderSortArrow('poprawne')}
                        </th>
                        <th className="p-4 text-center cursor-pointer hover:bg-gray-100" onClick={() => handleSort('procent')}>
                            Skuteczność {renderSortArrow('procent')}
                        </th>
                    </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 text-sm">
                    {questionStats.map(d => (
                        <tr key={d.id} className="hover:bg-gray-50">
                        <td className="p-4">{d.id}</td>
                        <td className="p-4">{d.artykul_id}</td>
                        <td className="p-4 truncate max-w-md font-medium" title={d.tresc}>{d.tresc}</td>
                        <td className="p-4 text-center">{d.ilosc}</td>
                        <td className="p-4 text-center">{d.poprawne}</td>
                        <td className="p-4 text-center">
                            <div className="flex items-center justify-center space-x-2">
                                <div className="w-24 bg-gray-200 rounded-full h-2">
                                    <div 
                                        className={`h-2 rounded-full ${d.procent > 70 ? 'bg-green-500' : d.procent > 40 ? 'bg-yellow-500' : 'bg-red-500'}`} 
                                        style={{ width: `${d.procent}%` }}
                                    ></div>
                                </div>
                                <span className="text-xs font-bold">{d.procent.toFixed(0)}%</span>
                            </div>
                        </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
                {questionStats.length === 0 && <div className="p-8 text-center text-gray-500">Brak danych statystycznych.</div>}
             </div>
           )}
        </Card>
      )}
    </AdminLayout>
  );
};
