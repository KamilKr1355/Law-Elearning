SELECT uk.id,uk.tresc,uk.uzytkownik_id,uk.artykul_id,uk.data_zapisu,u.username
                           FROM integracja_uzytkownika_komentarz uk
                           JOIN auth_user u on u.id=uk.uzytkownik_id
                           WHERE artykul_id = %s AND uzytkownik_id = %s;

INSERT INTO integracja_uzytkownika_komentarz(tresc,data_zapisu,artykul_id,uzytkownik_id)
                           VALUES (%s,NOW(),%s,%s)
                           RETURNING id;
                           """

UPDATE integracja_uzytkownika_komentarz
                           SET tresc = %s
                           WHERE id = %s AND uzytkownik_id = %s
                           RETURNING id;

DELETE FROM integracja_uzytkownika_komentarz
                           WHERE id = %s AND uzytkownik_id = %s
                           RETURNING id;

 DELETE FROM integracja_uzytkownika_komentarz
                           WHERE id = %s
                           RETURNING id;

SELECT id, pytanie_id, ilosc_odpowiedzi, poprawne_odpowiedzi
                FROM statystyki_statystykipytania
                WHERE pytanie_id = %s;

UPDATE statystyki_statystykipytania
                SET ilosc_odpowiedzi = ilosc_odpowiedzi + 1,
                    poprawne_odpowiedzi = poprawne_odpowiedzi + %s
                WHERE pytanie_id = %s
                RETURNING id;

INSERT INTO statystyki_statystykipytania 
                (pytanie_id, ilosc_odpowiedzi, poprawne_odpowiedzi)
                VALUES (%s, 1, %s)
                RETURNING id;

SELECT id, pytanie_id, ilosc_odpowiedzi, poprawne_odpowiedzi
                FROM statystyki_statystykipytania WHERE id = %s;

SELECT
                s.id,p.id AS pytanie_id,
                COALESCE(s.ilosc_odpowiedzi, 0) AS ilosc_odpowiedzi,
                COALESCE(s.poprawne_odpowiedzi, 0) AS poprawne_odpowiedzi
                FROM kursy_pytanie p
                LEFT JOIN statystyki_statystykipytania s ON p.id = s.pytanie_id
                ORDER BY
                COALESCE(s.poprawne_odpowiedzi, 0) / COALESCE(s.ilosc_odpowiedzi, 1)::NUMERIC ASC;

 SELECT id,tresc,data_zapisu,artykul_id,uzytkownik_id
                            FROM integracja_uzytkownika_notatka
                            WHERE uzytkownik_id = %s AND artykul_id = %s;

SELECT id,tresc,data_zapisu,artykul_id,uzytkownik_id
                            FROM integracja_uzytkownika_notatka
                            WHERE uzytkownik_id = %s;

INSERT INTO integracja_uzytkownika_notatka (tresc,data_zapisu,artykul_id,uzytkownik_id)
                            VALUES (%s,NOW(),%s,%s)
                            RETURNING id;

 UPDATE integracja_uzytkownika_notatka 
                            SET tresc = %s
                            WHERE id = %s AND uzytkownik_id = %s
                            RETURNING id;

DELETE FROM integracja_uzytkownika_notatka 
                            WHERE id = %s AND uzytkownik_id = %s
                            RETURNING id;

SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE uzytkownik_id = %s
                ORDER BY data_zapisu DESC;

SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE kurs_id = %s
                ORDER BY data_zapisu DESC;

SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE kurs_id = %s
                ORDER BY data_zapisu DESC;

SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE id = %s;

SELECT id, data_zapisu, wynik, kurs_id, uzytkownik_id
                FROM integracja_uzytkownika_wynikiegzaminu
                WHERE uzytkownik_id = %s AND kurs_id = %s
                ORDER BY data_zapisu DESC;

SELECT avg, kurs_id, uzytkownik_id, username
                FROM average_grade_for_user_kurs_view
                WHERE uzytkownik_id = %s AND kurs_id = %s;

SELECT avg_wynik, kurs_id
                FROM avg_kurs_grade
                WHERE kurs_id = %s;

INSERT INTO integracja_uzytkownika_wynikiegzaminu 
                (data_zapisu, wynik, kurs_id, uzytkownik_id)
                VALUES (NOW(), %s, %s, %s)
                RETURNING id, data_zapisu, wynik, kurs_id, uzytkownik_id;