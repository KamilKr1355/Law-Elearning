
import axios from 'axios';
import type { 
  User, Kurs, Rozdzial, ArtykulView, Notatka, Komentarz, 
  QuizQuestion, WynikEgzaminu, 
  Artykul, Pytanie, Odpowiedz, ZapisArtykulu, OcenaArtykuluCombined,
  KursProgress, StatystykiPytania, KursDni, LeaderboardEntry
} from '../types';

const API_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8001/api';
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const setAuthToken = (token: string) => {
    if (token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
        delete api.defaults.headers.common['Authorization'];
    }
};

api.interceptors.request.use(
  (config) => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        const user = JSON.parse(userStr);
        if (user.token) {
          config.headers.Authorization = `Bearer ${user.token}`;
        }
      } catch (e) {}
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authService = {
  login: async (data: any) => {
    const response = await api.post('/users/login/', data);
    return { access: response.data.access };
  },
  register: async (data: any) => {
    const response = await api.post('/users/register/', data);
    return response.data;
  },
  getProfile: async () => {
    const response = await api.get('/users/profile/');
    return response.data;
  },
  updateProfile: async (data: any) => {
    try {
        const response = await api.put('/users/profile/', data);
        return response.data;
    } catch (error: any) {
        return data;
    }
  },
  getUsers: async () => {
    const response = await api.get('/users/');
    return response.data;
  },
  promoteToAdmin: async (pk: number | string) => {
    const response = await api.put(`/users/${pk}/promote/`);
    return response.data;
  },
  toggleUserBan: async (pk: number | string) => {
    const response = await api.put(`/users/${pk}/ban/`);
    return response.data;
  },
  deleteUser: async (pk: number | string) => {
    const response = await api.delete(`/users/${pk}/delete/`);
    return response.data;
  }
};

export const kursService = {
  getAll: async () => {
    const response = await api.get('/kursy/');
    return response.data;
  },
  getOne: async (id: string) => {
    const response = await api.get(`/kursy/${id}/`);
    return response.data; 
  },
  getRozdzialy: async (kursId: string) => {
    const response = await api.get(`/kursy/${kursId}/rozdzialy/`);
    return response.data;
  },
  getArtykuly: async (kursId: string) => {
    const response = await api.get(`/kursy/${kursId}/artykuly/`);
    return response.data;
  },
  getArtykulyByRozdzial: async (rozdzialId: number | string) => {
    const response = await api.get(`/kursy/rozdzial/${rozdzialId}/artykuly/`);
    return response.data;
  },
  getArtykulDetail: async (id: string) => {
    const response = await api.get(`/kursy/artykuly2/${id}/`);
    return response.data;
  },
  getArtykulDnia: async (kursId: string | number) => {
    const response = await api.get(`/kursy/artykul-dnia/${kursId}`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post('/kursy/', data);
    return response.data;
  },
  update: async (id: number, data: any) => {
    const response = await api.put(`/kursy/${id}/`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await api.delete(`/kursy/${id}/`);
    return response.data;
  },
  createRozdzial: async (kursId: number, data: any) => {
    const response = await api.post(`/kursy/${kursId}/rozdzialy/`, data);
    return response.data;
  },
  updateRozdzial: async (id: number, data: any) => {
    const response = await api.put(`/kursy/rozdzialy/${id}/`, data);
    return response.data;
  },
  deleteRozdzial: async (id: number) => {
    const response = await api.delete(`/kursy/rozdzialy/${id}/`);
    return response.data;
  },
  createArtykul: async (kursId: number, data: any) => {
    const response = await api.post(`/kursy/${kursId}/artykuly/`, data);
    return response.data;
  },
  updateArtykul: async (id: number, data: any) => {
    const response = await api.put(`/kursy/artykuly/${id}/`, data);
    return response.data;
  },
  deleteArtykul: async (id: number) => {
    const response = await api.delete(`/kursy/artykuly/${id}/`);
    return response.data;
  },
  getAllPytania: async () => {
    const response = await api.get('/kursy/pytania/');
    return response.data;
  }
};

export const contentAdminService = {
  getPytaniaByArtykul: async (artykulId: number) => {
    const response = await api.get(`/kursy/pytania/artykul/${artykulId}/`);
    return response.data;
  },
  getPytanie: async (id: number) => {
    const response = await api.get(`/kursy/pytania/zmien/${id}/`);
    return response.data;
  },
  createPytanie: async (data: any) => {
    const response = await api.post('/kursy/pytania/', data);
    return response.data;
  },
  updatePytanie: async (id: number, data: any) => {
    const response = await api.put(`/kursy/pytania/zmien/${id}/`, data);
    return response.data;
  },
  deletePytanie: async (id: number) => {
    const response = await api.delete(`/kursy/pytania/zmien/${id}/`);
    return response.data;
  },
  getOdpowiedzi: async (pytanieId: number) => {
    const response = await api.get(`/kursy/odpowiedzi/pytanie/${pytanieId}/`);
    return response.data;
  },
  createOdpowiedz: async (data: any) => {
    const response = await api.post('/kursy/odpowiedzi/', data);
    return response.data;
  },
  updateOdpowiedz: async (id: number, data: any) => {
    const response = await api.put(`/kursy/odpowiedz/${id}/`, data);
    return response.data;
  },
  deleteOdpowiedz: async (id: number) => {
    const response = await api.delete(`/kursy/odpowiedz/${id}/`);
    return response.data;
  },
};

export const aktywnoscService = {
  getNotatki: async (artykulId?: number) => {
    const params = artykulId ? { artykul_id: artykulId } : {};
    const response = await api.get('/aktywnosc/moje-notatki/', { params });
    return response.data;
  },
  getNotatkiKursu: async (kursId: string | number) => {
    const response = await api.get(`/aktywnosc/notatki-kursu/${kursId}/`);
    return response.data;
  },
  addNotatka: async (data: { tresc: string, artykul_id: number }) => {
    const response = await api.post('/aktywnosc/moje-notatki/', data);
    return response.data;
  },
  updateNotatka: async (id: number, tresc: string) => {
    const response = await api.put(`/aktywnosc/moje-notatki/${id}/`, { tresc });
    return response.data;
  },
  deleteNotatka: async (id: number) => {
    const response = await api.delete(`/aktywnosc/moje-notatki/${id}/`);
    return response.data;
  },
  getKomentarze: async (artykulId: string) => {
    const response = await api.get(`/aktywnosc/artykuly/${artykulId}/komentarze/`);
    if (Array.isArray(response.data) && response.data.length > 0 && response.data[0] === "message") {
        return [];
    }
    return response.data;
  },
  addKomentarz: async (artykulId: string, tresc: string) => {
    const response = await api.post(`/aktywnosc/artykuly/${artykulId}/komentarze/`, { tresc });
    return response.data;
  },
  updateKomentarz: async (id: number, tresc: string) => {
    const response = await api.put(`/aktywnosc/komentarze/${id}/`, { tresc });
    return response.data;
  },
  deleteKomentarz: async (id: number) => {
    const response = await api.delete(`/aktywnosc/komentarze/${id}/`);
    return response.data;
  },
  getOcena: async (artykulId: string): Promise<OcenaArtykuluCombined> => {
    const response = await api.get(`/aktywnosc/oceny/artykul/${artykulId}/`);
    return response.data;
  },
  setOcena: async (artykulId: string, ocena: number) => {
    const response = await api.post(`/aktywnosc/oceny/artykul/${artykulId}/`, { ocena });
    return response.data;
  },
  getPytaniaNauka: async (kursId: string) => {
    const response = await api.get(`/aktywnosc/nauka/kurs/${kursId}/`);
    return response.data;
  },
  updatePostepNauki: async (data: { pytanie_id: number, is_correct: boolean }) => {
    const response = await api.post('/statystyki/update/', data);
    return response.data;
  },
  updateStatusPytania: async (pytanieId: number, status: string) => {
    const response = await api.post('/aktywnosc/progress/pytanie/aktualizuj/', { 
        pytanie_id: pytanieId, 
        status: status 
    });
    return response.data;
  },
  getPostepKursu: async (kursId: string): Promise<KursProgress> => {
      const response = await api.get(`/aktywnosc/progress/kurs/${kursId}/`);
      return response.data;
  },
  deletePostepKursu: async (kursId: string | number) => {
    const response = await api.delete(`/aktywnosc/progress/usun/${kursId}/`);
    return response.data;
  },
  getZapisane: async () => {
    const response = await api.get('/aktywnosc/moje-zapisy/');
    return response.data;
  },
  checkZapis: async (artykulId: number | string) => {
    try {
        const response = await api.get(`/aktywnosc/moje-zapisy/${artykulId}/`);
        if (response.status === 200 && response.data?.istnieje) {
            return true;
        }
        return false;
    } catch (error) {
        return false;
    }
  },
  addZapis: async (artykulId: number) => {
    const response = await api.post('/aktywnosc/moje-zapisy/', { artykul_id: artykulId });
    return response.data;
  },
  deleteZapis: async (artykulId: number) => {
    const response = await api.delete(`/aktywnosc/moje-zapisy/${artykulId}/`);
    return response.data;
  }
};

export const quizService = {
  start: async (kursNazwa: string, rozdzialy?: string) => {
    const params: any = { kursy: kursNazwa, liczba_pytan: 20 };
    if (rozdzialy) {
        params.rozdzialy = rozdzialy;
    }
    const response = await api.get('/aktywnosc/quiz/start/', { params });
    return response.data;
  },
  check: async (data: { kurs_id: number, odpowiedzi: {pytanie_id: number, wybrana_opcja: number}[] }) => {
    const response = await api.post('/aktywnosc/quiz/sprawdz/', data);
    return response.data;
  },
};

export const wynikiService = {
  getAll: async () => {
    const response = await api.get('/aktywnosc/wyniki-egzaminu/');
    return response.data;
  },
  getAllAdmin: async () => {
    const response = await api.get('/aktywnosc/wyniki-wszystkich-egzaminow/');
    return response.data;
  },
  getStats: async (pytanieId: number | string): Promise<StatystykiPytania> => {
     const response = await api.get(`/statystyki/pytanie/${pytanieId}/`);
     return response.data;
  },
  getAllStats: async (): Promise<StatystykiPytania[]> => {
    const response = await api.get('/statystyki/pytania/');
    return response.data;
  },
  getStatsLast7Days: async (): Promise<KursDni[]> => {
    const response = await api.get('/statystyki/kursy-dni/');
    return response.data;
  },
  getLeaderboard: async (): Promise<LeaderboardEntry[]> => {
    const response = await api.get('/statystyki/leaderboard/');
    return response.data;
  },
  getCourseAverage: async (kursId: string) => {
    const response = await api.get(`/aktywnosc/wyniki-egzaminu/srednia-kursu/${kursId}/`);
    return response.data;
  },
};

export default api;
