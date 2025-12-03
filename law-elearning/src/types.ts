
export interface User {
  id: number;
  username: string;
  email?: string;
  name?: string;
  isAdmin?: string | boolean; // API returns boolean true/false, logic handles conversion
  token?: string;
}

export interface Kurs {
  id: number;
  nazwa_kursu: string;
}

export interface Rozdzial {
  id: number;
  nazwa_rozdzialu: string;
  kurs_id: number;
}

export interface Artykul {
  id: number;
  tresc: string;
  tytul: string;
  nr_artykulu: string;
  rozdzial_id: number;
}

export interface ArtykulView {
  id: number;
  artykul_id: number;
  tresc: string;
  nazwa_kursu: string;
  tytul?: string; // Added optional for list views
  rozdzial_id?: number;
  nr_artykulu?: string;
}

export interface Pytanie {
  id: number;
  tresc: string;
  artykul_id: number;
  odpowiedzi?: Odpowiedz[]; // Optional for frontend UI composition
}

export interface Odpowiedz {
  id: number;
  tresc: string;
  poprawna: boolean;
  pytanie_id: number;
}

export interface Notatka {
  id: number;
  tresc: string;
  uzytkownik_id: number;
  artykul_id: number;
  data_zapisu: string;
}

export interface ZapisArtykulu {
    id: number;
    artykul_id: number; // REQUIRED now
    tytul: string;
    data_zapisu: string;
}

export interface Komentarz {
  id: number;
  tresc: string;
  uzytkownik_id: number;
  username: string;
  artykul_id: number;
  data_zapisu: string;
}

export interface OcenaArtykulu {
  id: number;
  ocena: number;
  artykul_id: number;
}

export interface OcenaArtykuluCombined {
  artykul_id: number;
  srednia_ocena: number;
  moja_ocena?: OcenaArtykulu | null;
}

export interface QuizQuestion {
  id: number;
  tresc: string;
  odpowiedzi: { id: number; tresc: string }[];
}

export interface QuizResult {
  punkty: number;
  poprawne: number[];
  wynik: number;
}

export interface WynikEgzaminu {
  id: number;
  data_zapisu: string;
  wynik: number;
  kurs_id: number;
  uzytkownik_id: number;
}

export interface StatystykiPytania {
  id: number;
  pytanie_id: number;
  ilosc_odpowiedzi: number;
  poprawne_odpowiedzi: number;
  procent_poprawnych: string; // backend sends string usually "50.0" or similar
}

export interface KursProgress {
  lista_postepu: any[];
  podsumowanie: {
    total_questions: number;
    completed_count: number;
    progress_percentage: number;
  }
}
