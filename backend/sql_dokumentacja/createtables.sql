
CREATE TABLE kursy_kurs (
    id SERIAL PRIMARY KEY,
    nazwa_kursu VARCHAR(50) NOT NULL
);


CREATE TABLE kursy_rozdzial (
    id SERIAL PRIMARY KEY,
    kurs_id INTEGER NOT NULL,
    nazwa_rozdzialu VARCHAR(255) NOT NULL,
    FOREIGN KEY (kurs_id) REFERENCES kursy_kurs (id) ON DELETE CASCADE
);

CREATE TABLE kursy_artykul (
    id SERIAL PRIMARY KEY,
    rozdzial_id INTEGER NOT NULL,
    tresc TEXT NOT NULL,
    tytul TEXT NOT NULL,
    nr_artykulu VARCHAR(10) NOT NULL,
    FOREIGN KEY (rozdzial_id) REFERENCES kursy_rozdzial (id) ON DELETE CASCADE
);


CREATE TABLE kursy_pytanie (
    id SERIAL PRIMARY KEY,
    artykul_id INTEGER NOT NULL,
    tresc TEXT NOT NULL,
    FOREIGN KEY (artykul_id) REFERENCES kursy_artykul (id) ON DELETE CASCADE
);


CREATE TABLE kursy_odpowiedz (
    id SERIAL PRIMARY KEY,
    pytanie_id INTEGER NOT NULL,
    tresc TEXT NOT NULL,
    poprawna BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (pytanie_id) REFERENCES kursy_pytanie (id) ON DELETE CASCADE
);

CREATE TABLE kursy_uzytkownik_kurs (
    id SERIAL PRIMARY KEY,
    uzytkownik_id INTEGER NOT NULL,
    kurs_id INTEGER NOT NULL,
    data_zapisu TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uzytkownik_id) REFERENCES auth_user (id) ON DELETE CASCADE,
    FOREIGN KEY (kurs_id) REFERENCES kursy_kurs (id) ON DELETE CASCADE,
    
    CONSTRAINT kursy_uzytkownik_kurs_uzytkownik_id_kurs_id_key UNIQUE (uzytkownik_id, kurs_id)
);

CREATE TABLE integracja_uzytkownika_zapisartykulu (
    id SERIAL PRIMARY KEY,
    uzytkownik_id INTEGER NOT NULL,
    artykul_id INTEGER NOT NULL,
    data_zapisu TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uzytkownik_id) REFERENCES auth_user (id) ON DELETE CASCADE,
    FOREIGN KEY (artykul_id) REFERENCES kursy_artykul (id) ON DELETE CASCADE,
    
    CONSTRAINT integracja_uzytkownika_zapisartykulu_unique UNIQUE (uzytkownik_id, artykul_id)
);

CREATE TABLE integracja_uzytkownika_notatka (
    id SERIAL PRIMARY KEY,
    uzytkownik_id INTEGER NOT NULL,
    artykul_id INTEGER NOT NULL,
    tresc TEXT NOT NULL,
    data_zapisu TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uzytkownik_id) REFERENCES auth_user (id) ON DELETE CASCADE,
    FOREIGN KEY (artykul_id) REFERENCES kursy_artykul (id) ON DELETE CASCADE
);

CREATE TABLE integracja_uzytkownika_komentarz (
    id SERIAL PRIMARY KEY,
    uzytkownik_id INTEGER NOT NULL,
    artykul_id INTEGER NOT NULL,
    tresc TEXT NOT NULL,
    data_zapisu TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uzytkownik_id) REFERENCES auth_user (id) ON DELETE CASCADE,
    FOREIGN KEY (artykul_id) REFERENCES kursy_artykul (id) ON DELETE CASCADE
);

CREATE TABLE integracja_uzytkownika_progresspytan (
    id SERIAL PRIMARY KEY,
    uzytkownik_id INTEGER NOT NULL,
    pytanie_id INTEGER NOT NULL,
    status VARCHAR(2) NOT NULL DEFAULT 'NW', 
    data_aktualizacji TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uzytkownik_id) REFERENCES auth_user (id) ON DELETE CASCADE,
    FOREIGN KEY (pytanie_id) REFERENCES kursy_pytanie (id) ON DELETE CASCADE,
    
    CONSTRAINT integracja_uzytkownika_progresspytan_unique UNIQUE (uzytkownik_id, pytanie_id)
);

CREATE TABLE integracja_uzytkownika_wynikiegzaminu (
    id SERIAL PRIMARY KEY,
    uzytkownik_id INTEGER NOT NULL,
    kurs_id INTEGER NOT NULL,
    data_zapisu TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    wynik REAL NOT NULL, 
    
    FOREIGN KEY (uzytkownik_id) REFERENCES auth_user (id) ON DELETE CASCADE,
    FOREIGN KEY (kurs_id) REFERENCES kursy_kurs (id) ON DELETE CASCADE,
    
    CONSTRAINT wynik_egzaminu_zakres CHECK (wynik >= 0.0 AND wynik <=100.0) 
);

CREATE TABLE integracja_uzytkownika_ocenaartykulu (
    id SERIAL PRIMARY KEY,
    uzytkownik_id INTEGER NOT NULL,
    artykul_id INTEGER NOT NULL,
    ocena SMALLINT NOT NULL, -- Wartość 1-5
    data TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uzytkownik_id) REFERENCES auth_user (id) ON DELETE CASCADE,
    FOREIGN KEY (artykul_id) REFERENCES kursy_artykul (id) ON DELETE CASCADE,
    
    CONSTRAINT ocena_zakres CHECK (ocena >= 1 AND ocena <= 5),
    CONSTRAINT ocena_unikalna UNIQUE (uzytkownik_id, artykul_id)
);

CREATE TABLE statystyki_statystykipytania (
    id SERIAL,
    pytanie_id INTEGER PRIMARY KEY, 
    ilosc_odpowiedzi INTEGER NOT NULL DEFAULT 0,
    poprawne_odpowiedzi INTEGER NOT NULL DEFAULT 0,
    
    FOREIGN KEY (pytanie_id) REFERENCES kursy_pytanie (id) ON DELETE CASCADE,
    
    CONSTRAINT ilosc_odpowiedzi_pozytywna CHECK (ilosc_odpowiedzi >= 0),
    CONSTRAINT poprawne_odpowiedzi_pozytywna CHECK (poprawne_odpowiedzi >= 0)
);