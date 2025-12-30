
import React, { useEffect, useState } from 'react';
import { Card, Button, Input, Spinner, Badge, ConfirmationModal } from '../components/UI';
import { kursService, authService, contentAdminService, wynikiService } from '../services/api';
import { Link, useParams, useNavigate } from 'react-router-dom';
import type { Kurs, Rozdzial, Artykul, Pytanie, Odpowiedz, WynikEgzaminu, StatystykiPytania } from '../types';
import { isUserAdmin } from '../utils/auth';
import { useAuth } from '../context/AuthContext';

const AdminLayout = ({ title, children, actions, backLink }: any) => (
  <div className="space-y-6 animate-fadeIn">
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b pb-6 gap-4">
      <div className="flex items-center space-x-4">
        {backLink && <Link to={backLink} className="bg-white border shadow-sm px-4 py-2 rounded-xl text-gray-500 hover:text-indigo-600 font-bold text-xs transition-all uppercase tracking-widest">&larr; Powrót</Link>}
        <h1 className="text-3xl font-black text-gray-900 uppercase tracking-tighter">{title}</h1>
      </div>
      <div className="flex space-x-2 w-full md:w-auto">{actions}</div>
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
            return { label, value: item.liczba_kursow };
        });
        setStats(chartData);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  const maxVal = stats.length > 0 ? Math.max(...stats.map(s => s.value), 1) : 10;

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-black text-indigo-950 tracking-tighter uppercase">Panel Administratora</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/admin/kursy">
          <Card hover className="bg-gradient-to-br from-indigo-600 to-indigo-900 text-white border-none h-full flex flex-col justify-center items-center text-center p-10 relative overflow-hidden group">
            <div className="text-6xl mb-4 drop-shadow-lg transition-transform group-hover:scale-110 duration-500">📚</div>
            <h3 className="text-2xl font-black uppercase tracking-tighter">Edukacja</h3>
            <p className="opacity-70 mt-2 text-sm font-bold">Kursy i Artykuły</p>
          </Card>
        </Link>
        <Link to="/admin/users">
          <Card hover className="bg-white h-full flex flex-col justify-center items-center text-center p-10 border-2 border-gray-100 relative group">
            <div className="text-6xl mb-4 grayscale group-hover:grayscale-0 transition-all duration-500">👥</div>
            <h3 className="text-2xl font-black text-gray-800 uppercase tracking-tighter">Użytkownicy</h3>
            <p className="text-gray-400 mt-2 text-sm font-bold">Zarządzanie studentami</p>
          </Card>
        </Link>
        <Link to="/admin/raporty">
          <Card hover className="bg-white h-full flex flex-col justify-center items-center text-center p-10 border-2 border-gray-100 relative group">
            <div className="text-6xl mb-4 grayscale group-hover:grayscale-0 transition-all duration-500">📈</div>
            <h3 className="text-2xl font-black text-gray-800 uppercase tracking-tighter">Analityka</h3>
            <p className="text-gray-400 mt-2 text-sm font-bold">Raporty i Wyniki</p>
          </Card>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card className="border-none shadow-2xl bg-white/80">
           <h3 className="font-black text-lg mb-8 uppercase tracking-widest text-indigo-900 border-b pb-4">Aktywność studentów</h3>
           {loading ? <Spinner /> : (
               <div className="flex items-end justify-between h-48 space-x-3 px-2">
                 {stats.map((s, i) => (
                    <div key={i} className="flex flex-col items-center w-full group">
                       <div className="w-full relative flex items-end justify-center">
                          <div 
                            className="w-full bg-indigo-200 rounded-t-xl hover:bg-indigo-600 transition-all relative shadow-sm"
                            style={{ height: `${(s.value / maxVal) * 140}px`, minHeight: '4px' }}
                          >
                             <div className="absolute -top-10 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-[10px] font-black px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition shadow-xl z-20">
                                {s.value}
                             </div>
                          </div>
                       </div>
                       <span className="text-[10px] font-black text-gray-400 mt-3">{s.label}</span>
                    </div>
                 ))}
               </div>
           )}
        </Card>
        
        <Card className="border-none shadow-2xl">
            <h3 className="font-black text-lg mb-6 uppercase tracking-widest text-indigo-900 border-b pb-4">Skróty systemowe</h3>
            <div className="space-y-4">
                <Link to="/admin/kursy" className="block p-5 bg-gray-50 rounded-2xl hover:bg-indigo-600 hover:text-white flex justify-between items-center transition-all duration-300 group shadow-sm">
                    <span className="font-bold text-gray-700 group-hover:text-white">Dodaj nową wiedzę</span>
                    <span className="bg-indigo-600 group-hover:bg-white group-hover:text-indigo-600 text-white w-10 h-10 rounded-xl flex items-center justify-center font-black transition-colors">+</span>
                </Link>
                <Link to="/admin/users" className="block p-5 bg-gray-50 rounded-2xl hover:bg-indigo-600 hover:text-white flex justify-between items-center transition-all duration-300 group shadow-sm">
                    <span className="font-bold text-gray-700 group-hover:text-white">Lista użytkowników</span>
                    <span className="text-indigo-600 group-hover:text-white font-black text-2xl tracking-tighter">&rarr;</span>
                </Link>
                <div className="p-6 bg-amber-50 rounded-2xl text-xs font-bold text-amber-800 border-2 border-amber-100 leading-relaxed shadow-inner">
                    💡 Każda zmiana w kursie (ID) jest natychmiast widoczna dla wszystkich zalogowanych studentów.
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
  const [modal, setModal] = useState({ open: false, type: '', userId: 0, userName: '' });

  const fetchUsers = () => {
    setLoading(true);
    authService.getUsers().then(data => {
        const list = Array.isArray(data) ? data : [];
        setUsers(list.sort((a, b) => a.id - b.id)); // ASC sort
    }).finally(() => setLoading(false));
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleAction = async () => {
    try {
        if (modal.type === 'promote') await authService.promoteToAdmin(modal.userId);
        else if (modal.type === 'ban') await authService.toggleUserBan(modal.userId);
        else if (modal.type === 'delete') await authService.deleteUser(modal.userId);
        fetchUsers();
    } catch (e) { alert('Błąd operacji.'); }
  };

  const filteredUsers = users.filter(u => 
    u.username.toLowerCase().includes(searchTerm.toLowerCase()) || 
    (u.email && u.email.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <AdminLayout title="Użytkownicy" backLink="/admin">
      <ConfirmationModal 
        isOpen={modal.open}
        onClose={() => setModal({...modal, open: false})}
        onConfirm={handleAction}
        title={modal.type === 'delete' ? 'Usuwanie użytkownika' : 'Zmiana statusu'}
        message={`Czy na pewno chcesz wykonać tę akcję na ${modal.userName} (ID: ${modal.userId})?`}
      />
      <div className="mb-6 max-w-md"><Input placeholder="Szukaj studenta..." value={searchTerm} onChange={(e: any) => setSearchTerm(e.target.value)} /></div>
      {loading ? <Spinner /> : (
        <Card className="overflow-hidden p-0 border-none shadow-2xl">
          <table className="w-full text-left border-collapse text-sm">
            <thead className="bg-gray-50 text-[10px] uppercase text-gray-400 font-black tracking-widest border-b">
              <tr><th className="p-5">ID</th><th className="p-5">Użytkownik</th><th className="p-5">Rola</th><th className="p-5 text-right">Akcje</th></tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredUsers.map(u => (
                <tr key={u.id} className="hover:bg-indigo-50/20 transition-colors">
                  <td className="p-5 font-mono text-xs text-indigo-300 font-bold">#{u.id}</td>
                  <td className="p-5">
                      <div className="font-black text-gray-900">{u.username}</div>
                      <div className="text-[10px] text-gray-400 font-bold uppercase">{u.email}</div>
                  </td>
                  <td className="p-5">
                    <div className="flex flex-col space-y-1 items-start">
                      <Badge color={isUserAdmin(u) ? 'red' : 'green'}>{isUserAdmin(u) ? 'ADMIN' : 'STUDENT'}</Badge>
                      {u.is_active === false && <Badge color="red">BAN</Badge>}
                    </div>
                  </td>
                  <td className="p-5 text-right space-x-2">
                    {!isUserAdmin(u) && <button onClick={() => setModal({ open: true, type: 'promote', userId: u.id, userName: u.username })} className="text-[10px] font-black bg-white border shadow-sm text-indigo-600 px-4 py-2 rounded-xl hover:bg-indigo-600 hover:text-white transition-all uppercase">Awansuj</button>}
                    {currentUser?.id !== u.id && (
                      <>
                        <button onClick={() => setModal({ open: true, type: 'ban', userId: u.id, userName: u.username })} className={`text-[10px] font-black px-4 py-2 border shadow-sm rounded-xl transition-all uppercase ${u.is_active === false ? 'bg-green-500 text-white border-green-600' : 'bg-amber-50 text-amber-600 border-amber-100'}`}>{u.is_active === false ? 'Odblokuj' : 'Blokuj'}</button>
                        <button onClick={() => setModal({ open: true, type: 'delete', userId: u.id, userName: u.username })} className="text-[10px] font-black bg-red-50 text-red-600 border border-red-100 px-4 py-2 rounded-xl hover:bg-red-600 hover:text-white transition-all uppercase">Usuń</button>
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

// ------------------- COURSES -------------------
export const AdminKursy = () => {
  const [kursy, setKursy] = useState<Kurs[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentKurs, setCurrentKurs] = useState<Partial<Kurs>>({ nazwa_kursu: '' });
  const [searchTerm, setSearchTerm] = useState('');
  const [delModal, setDelModal] = useState({ open: false, id: 0, name: '' });

  const fetchKursy = () => kursService.getAll().then(data => {
      const list = Array.isArray(data) ? data : [];
      setKursy(list.sort((a, b) => a.id - b.id)); // ASC sort
  });
  
  useEffect(() => { fetchKursy(); }, []);

  const handleEdit = (k: Kurs) => {
      setCurrentKurs(k);
      setIsEditing(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (currentKurs.id) await kursService.update(currentKurs.id, currentKurs);
    else await kursService.create(currentKurs);
    setIsEditing(false);
    setCurrentKurs({ nazwa_kursu: '' });
    fetchKursy();
  };

  const confirmDelete = async () => {
      await kursService.delete(delModal.id);
      fetchKursy();
      setDelModal({ ...delModal, open: false });
  };

  const filteredKursy = kursy.filter(k => k.nazwa_kursu.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <AdminLayout title="Zarządzanie Kursami" backLink="/admin" actions={<Button onClick={() => { setIsEditing(true); setCurrentKurs({nazwa_kursu:''}); }}>+ Nowy Kurs</Button>}>
      <ConfirmationModal isOpen={delModal.open} onClose={() => setDelModal({ ...delModal, open: false })} onConfirm={confirmDelete} title="Usuwanie kursu" message={`Usunąć kurs "${delModal.name}"? Wszystkie materiały zostaną skasowane.`} />
      {isEditing && (
        <Card className="mb-8 border-4 border-indigo-100 bg-indigo-50/30 shadow-2xl rounded-3xl p-8">
          <h3 className="text-xl font-black mb-6 uppercase tracking-tighter text-indigo-950">{currentKurs.id ? `Edycja obiektu #${currentKurs.id}` : 'REJESTRACJA NOWEGO KURSU'}</h3>
          <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-6 items-end">
            <div className="flex-grow w-full">
              <Input label="Nazwa Kursu" value={currentKurs.nazwa_kursu} onChange={(e: any) => setCurrentKurs({...currentKurs, nazwa_kursu: e.target.value})} required />
            </div>
            <div className="mb-4 flex space-x-3 w-full md:w-auto">
              <Button type="submit" className="flex-1 md:px-10 font-black uppercase tracking-widest py-3">Zapisz</Button>
              <Button type="button" variant="secondary" className="flex-1 md:px-6" onClick={() => { setIsEditing(false); setCurrentKurs({nazwa_kursu:''}); }}>Anuluj</Button>
            </div>
          </form>
        </Card>
      )}
      <div className="mb-6 max-w-md"><Input placeholder="Szukaj w bazie kursów..." value={searchTerm} onChange={(e: any) => setSearchTerm(e.target.value)} /></div>
      <div className="grid gap-4">
        {filteredKursy.map(k => (
          <Card key={k.id} className="flex flex-col md:flex-row justify-between items-center py-5 px-8 border-2 border-gray-100 shadow-sm hover:border-indigo-200 transition-all rounded-2xl group">
            <div className="flex items-center space-x-6 mb-4 md:mb-0">
                <span className="font-mono text-sm text-indigo-300 font-black bg-indigo-50 w-12 h-12 flex items-center justify-center rounded-xl">#{k.id}</span>
                <span className="font-black text-xl text-gray-800 uppercase tracking-tighter group-hover:text-indigo-600 transition-colors">{k.nazwa_kursu}</span>
            </div>
            <div className="flex flex-wrap justify-center gap-2">
              <Link to={`/admin/kursy/${k.id}/rozdzialy`}><Button variant="secondary" className="text-[10px] font-black uppercase tracking-widest px-4">Rozdziały</Button></Link>
              <Link to={`/admin/kursy/${k.id}/artykuly`}><Button variant="secondary" className="text-[10px] font-black uppercase tracking-widest px-4">Artykuły</Button></Link>
              <button onClick={() => handleEdit(k)} className="text-[10px] font-black bg-indigo-50 text-indigo-600 px-5 py-3 hover:bg-indigo-600 hover:text-white rounded-xl transition-all uppercase tracking-widest">Edycja</button>
              <button onClick={() => setDelModal({ open: true, id: k.id, name: k.nazwa_kursu })} className="text-[10px] font-black bg-red-50 text-red-600 px-5 py-3 hover:bg-red-600 hover:text-white rounded-xl transition-all uppercase tracking-widest">Usuń</button>
            </div>
          </Card>
        ))}
      </div>
    </AdminLayout>
  );
};

// ------------------- CHAPTERS -------------------
export const AdminRozdzialy = () => {
  const { kursId } = useParams<{ kursId: string }>();
  const [rozdzialy, setRozdzialy] = useState<Rozdzial[]>([]);
  const [kurs, setKurs] = useState<Kurs | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [currentRozdzial, setCurrentRozdzial] = useState<Partial<Rozdzial>>({ nazwa_rozdzialu: '' });
  const [delModal, setDelModal] = useState({ open: false, id: 0, name: '' });

  const fetchData = async () => {
    if (!kursId) return;
    const [k, r] = await Promise.all([kursService.getOne(kursId), kursService.getRozdzialy(kursId)]);
    setKurs(Array.isArray(k) ? k[0] : k); 
    setRozdzialy((Array.isArray(r) ? r : []).sort((a, b) => a.id - b.id)); // ASC sort
  };

  useEffect(() => { fetchData(); }, [kursId]);

  const handleEdit = (r: Rozdzial) => {
      setCurrentRozdzial(r);
      setIsEditing(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!kursId) return;
    const payload = { ...currentRozdzial, kurs_id: parseInt(kursId) };
    if (currentRozdzial.id) await kursService.updateRozdzial(currentRozdzial.id, payload);
    else await kursService.createRozdzial(parseInt(kursId), payload);
    setIsEditing(false);
    setCurrentRozdzial({ nazwa_rozdzialu: '' });
    fetchData();
  };

  const confirmDelete = async () => {
      await kursService.deleteRozdzial(delModal.id);
      fetchData();
      setDelModal({ ...delModal, open: false });
  };

  return (
    <AdminLayout title={`Rozdziały: ${kurs?.nazwa_kursu || '...'}`} backLink="/admin/kursy" actions={<Button onClick={() => { setIsEditing(true); setCurrentRozdzial({nazwa_rozdzialu:''}); }}>+ Nowy Rozdział</Button>}>
       <ConfirmationModal isOpen={delModal.open} onClose={() => setDelModal({ ...delModal, open: false })} onConfirm={confirmDelete} title="Usuwanie rozdziału" message={`Usunąć rozdział "${delModal.name}"?`} />
       {isEditing && (
        <Card className="mb-8 border-4 border-indigo-100 bg-white shadow-2xl rounded-3xl p-8">
          <h3 className="font-black mb-6 uppercase tracking-tighter text-indigo-950">{currentRozdzial.id ? `Edycja Rozdziału #${currentRozdzial.id}` : 'Nowy Rozdział'}</h3>
          <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-6 items-end">
            <div className="flex-grow w-full"><Input label="Tytuł rozdziału" value={currentRozdzial.nazwa_rozdzialu} onChange={(e: any) => setCurrentRozdzial({...currentRozdzial, nazwa_rozdzialu: e.target.value})} required /></div>
            <div className="mb-4 flex space-x-3 w-full md:w-auto"><Button type="submit" className="flex-1 md:px-10 font-black uppercase tracking-widest py-3">Zapisz</Button><Button type="button" variant="secondary" className="flex-1" onClick={() => { setIsEditing(false); setCurrentRozdzial({nazwa_rozdzialu:''}); }}>Anuluj</Button></div>
          </form>
        </Card>
      )}
      <div className="grid gap-3">
        {rozdzialy.map(r => (
           <Card key={r.id} className="flex justify-between items-center py-4 px-6 border-2 border-gray-50 rounded-2xl hover:border-indigo-100 transition-all">
             <div className="flex items-center space-x-4">
                 <span className="font-mono text-[10px] text-indigo-300 font-black bg-indigo-50 w-10 h-10 flex items-center justify-center rounded-lg">#{r.id}</span>
                 <span className="font-bold text-gray-800 uppercase tracking-tighter">{r.nazwa_rozdzialu}</span>
             </div>
             <div className="flex space-x-2">
                <button onClick={() => handleEdit(r)} className="text-[10px] font-black text-indigo-600 bg-indigo-50 px-4 py-2 rounded-xl hover:bg-indigo-600 hover:text-white transition-all uppercase tracking-widest">Edytuj</button>
                <button onClick={() => setDelModal({ open: true, id: r.id, name: r.nazwa_rozdzialu })} className="text-[10px] font-black text-red-500 bg-red-50 px-4 py-2 rounded-xl hover:bg-red-600 hover:text-white transition-all uppercase tracking-widest">Usuń</button>
             </div>
           </Card>
        ))}
      </div>
    </AdminLayout>
  );
};

// ------------------- ARTICLES -------------------
export const AdminArtykuly = () => {
  const { kursId } = useParams<{ kursId: string }>();
  const [artykuly, setArtykuly] = useState<any[]>([]);
  const [rozdzialy, setRozdzialy] = useState<Rozdzial[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentArt, setCurrentArt] = useState<Partial<Artykul>>({ tytul: '', tresc: '', nr_artykulu: '', rozdzial_id: 0 });
  const [delModal, setDelModal] = useState({ open: false, id: 0, name: '' });

  const fetchData = async () => {
    if (!kursId) return;
    
    // FETCH CHAPTERS - Independent to avoid blocking if articles fail
    try {
        const rozds = await kursService.getRozdzialy(kursId);
        setRozdzialy((Array.isArray(rozds) ? rozds : []).sort((a, b) => a.id - b.id));
    } catch (e) {
        setRozdzialy([]);
    }

    // FETCH ARTICLES
    try {
        const arts = await kursService.getArtykuly(kursId);
        if (Array.isArray(arts)) {
            const uniqueArts = Array.from(new Map(arts.map(item => [item.artykul_id || item.id, item])).values())
                                    .sort((a: any, b: any) => (a.artykul_id || a.id) - (b.artykul_id || b.id));
            setArtykuly(uniqueArts);
        } else {
            setArtykuly([]);
        }
    } catch (e) {
        setArtykuly([]);
    }
  };

  useEffect(() => { 
    fetchData(); 
    setIsEditing(false);
    setCurrentArt({ tytul: '', tresc: '', nr_artykulu: '', rozdzial_id: 0 });
  }, [kursId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!kursId) return;
    
    const payload = {
      tytul: currentArt.tytul,
      tresc: currentArt.tresc,
      nr_artykulu: currentArt.nr_artykulu,
      rozdzial_id: currentArt.rozdzial_id || (rozdzialy.length > 0 ? rozdzialy[0].id : 0)
    };

    if (currentArt.id !== undefined && currentArt.id !== null) {
      await kursService.updateArtykul(currentArt.id, payload);
    } else {
      await kursService.createArtykul(parseInt(kursId), payload);
    }
    
    setIsEditing(false);
    setCurrentArt({ tytul: '', tresc: '', nr_artykulu: '', rozdzial_id: 0 });
    fetchData();
  };

  const handleEdit = async (art: any) => {
    const realId = art.artykul_id || art.id;
    window.scrollTo({ top: 0, behavior: 'smooth' });
    try {
        const detail = await kursService.getArtykulDetail(realId.toString());
        setCurrentArt({
          id: detail.id || realId,
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

  const confirmDelete = async () => {
      await kursService.deleteArtykul(delModal.id);
      fetchData();
      setDelModal({ ...delModal, open: false });
  };

  return (
    <AdminLayout title="Baza Artykułów" backLink="/admin/kursy" actions={<Button onClick={() => { setCurrentArt({tytul:'', tresc:'', nr_artykulu:'', rozdzial_id:0}); setIsEditing(true); }}>+ Dodaj Artykuł</Button>}>
      <ConfirmationModal isOpen={delModal.open} onClose={() => setDelModal({ ...delModal, open: false })} onConfirm={confirmDelete} title="Usuwanie lekcji" message={`Usunąć artykuł "${delModal.name}"?`} />
      {isEditing && (
        <Card className="mb-8 border-4 border-indigo-100 bg-white shadow-2xl rounded-3xl p-8 animate-fadeIn">
           <h3 className="font-black mb-6 uppercase tracking-tighter text-indigo-950">{currentArt.id ? `Edycja artykułu #${currentArt.id}` : 'REJESTRACJA NOWEJ LEKCJI'}</h3>
           <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input label="Tytuł artykułu" value={currentArt.tytul} onChange={(e:any) => setCurrentArt({...currentArt, tytul: e.target.value})} required />
                <Input label="Numer artykułu" value={currentArt.nr_artykulu} onChange={(e:any) => setCurrentArt({...currentArt, nr_artykulu: e.target.value})} required />
              </div>
              <div>
                <label className="block text-[10px] font-black text-indigo-400 uppercase tracking-widest mb-2">Przypisany Rozdział</label>
                <select className="w-full p-4 border-2 border-gray-100 rounded-2xl focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-600 outline-none bg-gray-50 font-bold transition-all" value={currentArt.rozdzial_id} onChange={(e) => setCurrentArt({...currentArt, rozdzial_id: parseInt(e.target.value)})}>
                  <option value={0}>-- Wybierz rozdział --</option>
                  {rozdzialy.map(r => <option key={r.id} value={r.id}>{r.nazwa_rozdzialu}</option>)}
                </select>
                {rozdzialy.length === 0 && <p className="text-red-500 text-[10px] mt-2 font-black uppercase tracking-widest">⚠️ Brak rozdziałów w tym kursie. Najpierw dodaj przynajmniej jeden rozdział.</p>}
              </div>
              <div>
                <label className="block text-[10px] font-black text-indigo-400 uppercase tracking-widest mb-2">Treść merytoryczna (HTML)</label>
                <textarea className="w-full p-6 border-2 border-gray-100 rounded-2xl h-64 font-mono text-sm focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all" value={currentArt.tresc} onChange={(e) => setCurrentArt({...currentArt, tresc: e.target.value})} required />
              </div>
              <div className="flex space-x-3 pt-4 border-t">
                <Button type="submit" className="px-12 font-black uppercase tracking-widest py-4">Zapisz Artykuł</Button>
                <Button type="button" variant="secondary" className="px-8" onClick={() => { setIsEditing(false); setCurrentArt({tytul: '', tresc: '', nr_artykulu: '', rozdzial_id: 0}); }}>Anuluj</Button>
              </div>
           </form>
        </Card>
      )}
      <div className="grid gap-3">
        {artykuly.map(a => {
            const displayId = a.artykul_id || a.id;
            return (
              <Card key={displayId} className="flex flex-col md:flex-row justify-between items-center py-5 px-8 border-2 border-gray-50 shadow-sm hover:border-indigo-200 transition-all rounded-2xl group">
                 <div className="flex items-center space-x-6 mb-4 md:mb-0">
                   <span className="font-mono text-sm text-indigo-300 font-black bg-indigo-50 w-12 h-12 flex items-center justify-center rounded-xl">#{displayId}</span>
                   <div className="flex flex-col">
                      <span className="font-black text-gray-900 uppercase tracking-tighter leading-tight text-lg group-hover:text-indigo-600 transition-colors">Art. {a.nr_artykulu || '?'} - {a.tytul || `Bez tytułu`}</span>
                      <span className="text-[9px] font-black text-gray-400 uppercase tracking-widest mt-1">Rozdział: {rozdzialy.find(r => r.id === a.rozdzial_id)?.nazwa_rozdzialu || `ID #${a.rozdzial_id}`}</span>
                   </div>
                 </div>
                 <div className="flex gap-2">
                    <Link to={`/admin/artykuly/${displayId}/pytania`}><Button variant="secondary" className="text-[10px] font-black uppercase tracking-widest px-4">Pytania</Button></Link>
                    <button onClick={() => handleEdit(a)} className="text-[10px] font-black bg-indigo-50 text-indigo-600 px-5 py-3 hover:bg-indigo-600 hover:text-white rounded-xl transition-all uppercase tracking-widest">Edycja</button>
                    <button onClick={() => setDelModal({ open: true, id: displayId, name: a.tytul || `Art. ${a.nr_artykulu}` })} className="text-[10px] font-black bg-red-50 text-red-600 px-5 py-3 hover:bg-red-600 hover:text-white rounded-xl transition-all uppercase tracking-widest">Usuń</button>
                 </div>
              </Card>
            );
        })}
      </div>
    </AdminLayout>
  );
};

// ------------------- QUESTIONS -------------------
export const AdminPytania = () => {
  const { artykulId } = useParams<{ artykulId: string }>();
  const [pytania, setPytania] = useState<Pytanie[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentPytanie, setCurrentPytanie] = useState<Partial<Pytanie>>({ tresc: '' });
  const [delModal, setDelModal] = useState({ open: false, id: 0 });
  const [artykul, setArtykul] = useState<any>(null);

  const fetchData = async () => {
    if (!artykulId) return;
    try {
        const [qData, aData] = await Promise.all([
          contentAdminService.getPytaniaByArtykul(parseInt(artykulId)),
          kursService.getArtykulDetail(artykulId)
        ]);
        setPytania((Array.isArray(qData) ? qData : []).sort((a, b) => a.id - b.id)); // ASC sort
        setArtykul(aData);
    } catch(e) { console.error(e); }
  };

  useEffect(() => { fetchData(); }, [artykulId]);

  const handleEdit = (p: Pytanie) => {
      setCurrentPytanie(p);
      setIsEditing(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!artykulId) return;
    const payload = { ...currentPytanie, artykul_id: parseInt(artykulId) };
    if (currentPytanie.id) await contentAdminService.updatePytanie(currentPytanie.id, payload);
    else await contentAdminService.createPytanie(payload);
    setIsEditing(false);
    setCurrentPytanie({ tresc: '' });
    fetchData();
  };

  const confirmDelete = async () => {
      await contentAdminService.deletePytanie(delModal.id);
      fetchData();
      setDelModal({ ...delModal, open: false });
  };

  return (
    <AdminLayout 
      title={`Baza pytań: Art. #${artykulId}`} 
      backLink={artykul ? `/admin/kursy/${artykul.kurs_id}/artykuly` : '/admin/kursy'} 
      actions={<Button onClick={() => { setIsEditing(true); setCurrentPytanie({tresc:''}); }}>+ Nowe Pytanie</Button>}
    >
      <ConfirmationModal isOpen={delModal.open} onClose={() => setDelModal({ ...delModal, open: false })} onConfirm={confirmDelete} title="Usuwanie pytania" message={`Usunąć to pytanie? Wszystkie przypisane odpowiedzi również zostaną skasowane.`} />
      {isEditing && (
        <Card className="mb-8 border-4 border-indigo-100 bg-indigo-50/30 rounded-3xl p-8 animate-fadeIn">
          <h3 className="font-black mb-6 uppercase tracking-tighter text-indigo-950">{currentPytanie.id ? `Edycja pytania #${currentPytanie.id}` : 'REJESTRACJA NOWEGO PYTANIA'}</h3>
          <form onSubmit={handleSubmit} className="flex flex-col gap-6">
            <Input label="Treść pytania" value={currentPytanie.tresc} onChange={(e: any) => setCurrentPytanie({...currentPytanie, tresc: e.target.value})} required />
            <div className="flex space-x-3 justify-end"><Button type="submit" className="px-12 font-black uppercase py-4">Zapisz</Button><Button type="button" variant="secondary" onClick={() => { setIsEditing(false); setCurrentPytanie({tresc:''}); }}>Anuluj</Button></div>
          </form>
        </Card>
      )}
      <div className="grid gap-3">
        {pytania.map(p => (
          <Card key={p.id} className="flex justify-between items-center py-5 px-8 border-2 border-gray-50 rounded-2xl hover:border-indigo-100 transition-all">
            <div className="flex items-center space-x-4 overflow-hidden">
                <span className="font-mono text-xs text-indigo-300 font-black bg-indigo-50 w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-lg">#{p.id}</span>
                <span className="font-bold text-gray-700 truncate">{p.tresc}</span>
            </div>
            <div className="flex space-x-2 flex-shrink-0">
               <Link to={`/admin/pytania/${p.id}/odpowiedzi`}><Button variant="secondary" className="text-[10px] font-black uppercase tracking-widest px-4">Opcje</Button></Link>
               <button onClick={() => handleEdit(p)} className="text-[10px] font-black bg-indigo-50 text-indigo-600 px-4 py-2 rounded-xl hover:bg-indigo-600 hover:text-white transition-all uppercase tracking-widest">Edytuj</button>
               <button onClick={() => setDelModal({ open: true, id: p.id })} className="text-[10px] font-black bg-red-50 text-red-600 px-4 py-2 rounded-xl hover:bg-red-600 hover:text-white transition-all uppercase tracking-widest">Usuń</button>
            </div>
          </Card>
        ))}
      </div>
    </AdminLayout>
  );
};

// ------------------- ANSWERS -------------------
export const AdminOdpowiedzi = () => {
  const { pytanieId } = useParams<{ pytanieId: string }>();
  const [odpowiedzi, setOdpowiedzi] = useState<Odpowiedz[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentOdp, setCurrentOdp] = useState<Partial<Odpowiedz>>({ tresc: '', poprawna: false });
  const [delModal, setDelModal] = useState({ open: false, id: 0 });
  const [pytanie, setPytanie] = useState<any>(null);

  const fetchData = async () => {
    if (!pytanieId) return;
    try {
        const [oData, pData] = await Promise.all([
          contentAdminService.getOdpowiedzi(parseInt(pytanieId)),
          contentAdminService.getPytanie(parseInt(pytanieId))
        ]);
        setOdpowiedzi((Array.isArray(oData) ? oData : []).sort((a, b) => a.id - b.id)); // ASC sort
        setPytanie(pData);
    } catch(e) { console.error(e); }
  };

  useEffect(() => { fetchData(); }, [pytanieId]);

  const handleEdit = (o: Odpowiedz) => {
      setCurrentOdp(o);
      setIsEditing(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pytanieId) return;
    const payload = { ...currentOdp, pytanie_id: parseInt(pytanieId) };
    if (currentOdp.id) await contentAdminService.updateOdpowiedz(currentOdp.id, payload);
    else await contentAdminService.createOdpowiedz(payload);
    setIsEditing(false);
    setCurrentOdp({ tresc: '', poprawna: false });
    fetchData();
  };

  const confirmDelete = async () => {
      await contentAdminService.deleteOdpowiedz(delModal.id);
      fetchData();
      setDelModal({ ...delModal, open: false });
  };

  return (
    <AdminLayout 
      title="Opcje odpowiedzi" 
      backLink={pytanie ? `/admin/artykuly/${pytanie.artykul_id}/pytania` : '/admin/kursy'} 
      actions={<Button onClick={() => { setIsEditing(true); setCurrentOdp({tresc:'', poprawna: false}); }}>+ Nowa Opcja</Button>}
    >
      <ConfirmationModal isOpen={delModal.open} onClose={() => setDelModal({ ...delModal, open: false })} onConfirm={confirmDelete} title="Usuwanie opcji" message={`Czy usunąć tę propozycję odpowiedzi?`} />
      {isEditing && (
        <Card className="mb-8 border-4 border-indigo-100 bg-indigo-50/20 rounded-3xl p-8 animate-fadeIn">
          <h3 className="font-black mb-6 uppercase tracking-tighter text-indigo-950">{currentOdp.id ? `Edycja opcji #${currentOdp.id}` : 'DODAWANIE NOWEJ OPCJI'}</h3>
          <form onSubmit={handleSubmit} className="space-y-6">
            <Input label="Treść odpowiedzi" value={currentOdp.tresc} onChange={(e: any) => setCurrentOdp({...currentOdp, tresc: e.target.value})} required />
            <div className="bg-white p-6 rounded-2xl border-2 border-gray-100 flex items-center space-x-4 cursor-pointer shadow-inner" onClick={() => setCurrentOdp({...currentOdp, poprawna: !currentOdp.poprawna})}>
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center transition-all ${currentOdp.poprawna ? 'bg-green-500 text-white shadow-lg shadow-green-100' : 'bg-gray-100 text-gray-400'}`}>
                    {currentOdp.poprawna ? '✓' : ''}
                </div>
                <span className="text-sm font-black uppercase tracking-widest text-gray-700">To jest poprawna odpowiedź</span>
            </div>
            <div className="flex space-x-3 justify-end pt-4"><Button type="submit" className="px-12 font-black uppercase py-4">Zatwierdź</Button><Button type="button" variant="secondary" onClick={() => { setIsEditing(false); setCurrentOdp({tresc: '', poprawna: false}); }}>Anuluj</Button></div>
          </form>
        </Card>
      )}
      <div className="grid gap-3">
        {odpowiedzi.map(o => (
          <Card key={o.id} className={`flex justify-between items-center py-5 px-8 border-2 rounded-2xl transition-all ${o.poprawna ? 'border-green-200 bg-green-50/30' : 'border-gray-50'}`}>
            <div className="flex items-center space-x-6">
                <span className="font-mono text-xs text-gray-300 font-black">#{o.id}</span>
                <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded-full ${o.poprawna ? 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.4)]' : 'bg-gray-200'}`} />
                    <span className={`font-bold text-lg ${o.poprawna ? 'text-green-800' : 'text-gray-600'}`}>{o.tresc}</span>
                </div>
            </div>
            <div className="flex space-x-2">
                <button onClick={() => handleEdit(o)} className="text-[10px] font-black bg-white border border-gray-100 shadow-sm px-4 py-2 rounded-xl hover:bg-indigo-600 hover:text-white transition-all uppercase tracking-widest">Edytuj</button>
                <button onClick={() => setDelModal({ open: true, id: o.id })} className="text-[10px] font-black bg-red-50 text-red-600 px-4 py-2 rounded-xl hover:bg-red-600 hover:text-white transition-all uppercase tracking-widest">Usuń</button>
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
                const [allResults, allUsers] = await Promise.all([wynikiService.getAllAdmin(), authService.getUsers()]);
                const uMap: {[key:number]: string} = {};
                if (Array.isArray(allUsers)) allUsers.forEach((u: any) => uMap[u.id] = u.username);
                setUserMap(uMap);
                setResults((Array.isArray(allResults) ? allResults : []).sort((a, b) => a.id - b.id)); // ASC sort
            } else if (activeTab === 'kursy_stats') {
                const [kursy, wyniki] = await Promise.all([kursService.getAll(), wynikiService.getAllAdmin()]);
                const safeKursy = Array.isArray(kursy) ? kursy : [];
                const safeWyniki = Array.isArray(wyniki) ? wyniki : [];
                const stats = safeKursy.map(k => {
                    const kWyniki = safeWyniki.filter(w => w.kurs_id === k.id);
                    const avg = kWyniki.length > 0 ? kWyniki.reduce((acc, curr) => acc + Number(curr.wynik || 0), 0) / kWyniki.length : 0;
                    return { id: k.id, name: k.nazwa_kursu, count: kWyniki.length, avg: Number(avg).toFixed(1) };
                }).sort((a, b) => a.id - b.id); // ASC sort
                setCourseStats(stats);
            } else if (activeTab === 'trudnosc') {
                const [pytania, allStats] = await Promise.all([kursService.getAllPytania(), wynikiService.getAllStats()]);
                const statsMap: {[key: number]: StatystykiPytania} = {};
                if (Array.isArray(allStats)) allStats.forEach((s: StatystykiPytania) => statsMap[s.pytanie_id] = s);
                const stats = (Array.isArray(pytania) ? pytania : []).map((p: Pytanie) => {
                    const s = statsMap[p.id];
                    return { id: p.id, tresc: p.tresc, ilosc: s ? s.ilosc_odpowiedzi : 0, procent: s ? parseFloat(s.procent_poprawnych || '0') : 0 };
                });
                stats.sort((a, b) => a.id - b.id); // ASC sort
                setQuestionStats(stats);
            }
        } catch (e) { console.error(e); } finally { setLoading(false); }
    };
    fetchData();
  }, [activeTab]);

  const handleSort = (key: string) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'asc') direction = 'desc';
    setSortConfig({ key, direction });
    const target = activeTab === 'trudnosc' ? questionStats : (activeTab === 'kursy_stats' ? courseStats : results);
    const sorted = [...target].sort((a, b) => {
        if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
        if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
        return 0;
    });
    if (activeTab === 'trudnosc') setQuestionStats(sorted); else if (activeTab === 'kursy_stats') setCourseStats(sorted); else setResults(sorted);
  };

  return (
    <AdminLayout title="Analityka" backLink="/admin">
      <div className="flex space-x-6 border-b-2 border-gray-100 mb-8 overflow-x-auto pb-4 px-2">
        {['wyniki', 'kursy_stats', 'trudnosc'].map(tab => (
            <button key={tab} className={`pb-2 px-6 font-black uppercase text-xs tracking-widest transition-all whitespace-nowrap relative ${activeTab === tab ? 'text-indigo-600' : 'text-gray-400 hover:text-gray-600'}`} onClick={() => setActiveTab(tab)}>
                {tab === 'wyniki' ? 'Rejestr Wyników' : tab === 'kursy_stats' ? 'Popularność Kursów' : 'Analiza Trudności'}
                {activeTab === tab && <div className="absolute bottom-[-16px] left-0 w-full h-1 bg-indigo-600 rounded-full" />}
            </button>
        ))}
      </div>
      {loading ? <Spinner /> : (
        <Card className="overflow-hidden p-0 border-none shadow-2xl">
           {activeTab === 'wyniki' && (
                <table className="w-full text-left border-collapse text-sm">
                    <thead className="bg-gray-50 uppercase text-[10px] text-gray-400 font-black tracking-widest border-b">
                    <tr><th className="p-5 cursor-pointer hover:text-indigo-600" onClick={() => handleSort('id')}>ID ↕</th><th className="p-5">Data</th><th className="p-5">Kurs</th><th className="p-5">Student</th><th className="p-5 text-right">Wynik</th></tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                    {results.map(r => (
                        <tr key={r.id} className="hover:bg-indigo-50/20 transition-colors">
                        <td className="p-5 font-mono text-xs text-indigo-300 font-bold">#{r.id}</td>
                        <td className="p-5 font-bold text-gray-700">{new Date(r.data_zapisu).toLocaleDateString()}</td>
                        <td className="p-5 font-black text-indigo-400">#{r.kurs_id}</td>
                        <td className="p-5 font-black uppercase text-gray-900">{userMap[r.uzytkownik_id] || `USER_${r.uzytkownik_id}`}</td>
                        <td className="p-5 text-right"><Badge color={Number(r.wynik) >= 50 ? 'green' : 'red'}>{Math.round(Number(r.wynik))}%</Badge></td>
                        </tr>
                    ))}
                    </tbody>
                </table>
           )}
           {activeTab === 'kursy_stats' && (
                <table className="w-full text-left border-collapse text-sm">
                    <thead className="bg-gray-50 uppercase text-[10px] text-gray-400 font-black tracking-widest border-b">
                        <tr><th className="p-5">Kurs</th><th className="p-5 cursor-pointer hover:text-indigo-600" onClick={() => handleSort('count')}>Rozwiązane ↕</th><th className="p-5 cursor-pointer hover:text-indigo-600" onClick={() => handleSort('avg')}>Średnia ↕</th></tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {courseStats.map(s => (
                            <tr key={s.id} className="hover:bg-indigo-50/20 transition-colors"><td className="p-5 font-black uppercase text-gray-800 tracking-tighter text-lg">{s.name}</td><td className="p-5 font-bold text-gray-500">{s.count} egz.</td><td className="p-5 font-black text-indigo-600 text-lg">{s.avg}%</td></tr>
                        ))}
                    </tbody>
                </table>
           )}
           {activeTab === 'trudnosc' && (
                <table className="w-full text-left border-collapse text-sm">
                    <thead className="bg-gray-50 uppercase text-[10px] text-gray-400 font-black tracking-widest border-b">
                    <tr><th className="p-5">Pytanie</th><th className="p-5 cursor-pointer hover:text-indigo-600" onClick={() => handleSort('ilosc')}>Liczba prób ↕</th><th className="p-5 cursor-pointer hover:text-indigo-600" onClick={() => handleSort('procent')}>Skuteczność ↕</th></tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                    {questionStats.map(s => (
                        <tr key={s.id} className="hover:bg-indigo-50/20 transition-colors">
                            <td className="p-5 max-w-xs font-bold text-gray-700">
                                <span className="text-[10px] text-indigo-300 font-mono block mb-1">#{s.id}</span>
                                <div className="truncate" title={s.tresc}>{s.tresc}</div>
                            </td>
                            <td className="p-5 font-bold text-gray-400">{s.ilosc}x</td>
                            <td className="p-5"><div className="flex items-center space-x-3"><div className="w-24 bg-gray-200 rounded-full h-3 overflow-hidden shadow-inner"><div className={`h-full transition-all duration-1000 ${s.procent > 70 ? 'bg-green-500 shadow-md' : s.procent > 40 ? 'bg-amber-500' : 'bg-red-500'}`} style={{ width: `${s.procent}%` }}></div></div><span className="font-black text-xs min-w-[35px]">{s.procent}%</span></div></td>
                        </tr>
                    ))}
                    </tbody>
                </table>
           )}
        </Card>
      )}
    </AdminLayout>
  );
};
