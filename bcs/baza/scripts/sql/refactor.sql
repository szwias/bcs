BEGIN;

-- Step 1: Create a temporary table to stage incoming data
CREATE TEMP TABLE w_tmp (
    id INTEGER PRIMARY KEY,
    czy_jednodniowe boolean NOT NULL,
    data_zakonczenia date NOT NULL,
    czy_to_wyjazd boolean NOT NULL,
    typ_wydarzenia_id bigint,
    typ_wyjazdu_id bigint
);

COPY w_tmp (id, data_zakonczenia, typ_wydarzenia_id, typ_wyjazdu_id, czy_to_wyjazd, czy_jednodniowe) FROM stdin;
71	2012-03-09	23	3	t	t
...
369	2019-09-27	3	5	f	t
\.


UPDATE public.kalendarz_wydarzeniedummy d
	SET
	     czy_jednodniowe=w.czy_jednodniowe,
	     data_zakonczenia=w.data_zakonczenia,
	     czy_to_wyjazd=w.czy_to_wyjazd,
	     typ_wydarzenia_id=w.typ_wydarzenia_id,
	     typ_wyjazdu_id=w.typ_wyjazdu_id
	FROM w_tmp w
	WHERE d.wydarzeniekalendarzowe_ptr_id=w.id;

INSERT INTO public.kalendarz_wydarzeniedummy (wydarzeniekalendarzowe_ptr_id, data_zakonczenia, typ_wydarzenia_id, typ_wyjazdu_id, czy_to_wyjazd, czy_jednodniowe)
SELECT w.id, w.data_zakonczenia, w.typ_wydarzenia_id, w.typ_wyjazdu_id, w.czy_to_wyjazd, w.czy_jednodniowe
FROM w_tmp w
LEFT JOIN public.kalendarz_wydarzeniedummy d ON d.wydarzeniekalendarzowe_ptr_id = w.id
WHERE d.wydarzeniekalendarzowe_ptr_id IS NULL;



CREATE TEMP TABLE k_tmp
(
    id               INTEGER PRIMARY KEY,
    nazwa            character varying(255) COLLATE pg_catalog."default" NOT NULL,
    data_rozpoczecia date                                                NOT NULL,
    link             character varying(200) COLLATE pg_catalog."default" NOT NULL,
    opis             text COLLATE pg_catalog."default"                   NOT NULL
);


COPY k_tmp (id, nazwa, opis, data_rozpoczecia, link) FROM stdin;
71	Kudłacze	""	2012-03-09	""
...
369	Reactivation XI: Cantus	""	2019-09-27	""
\.

UPDATE public.kalendarz_wydarzeniekalendarzowe k
	SET
	    nazwa=t.nazwa,
	    data_rozpoczecia=t.data_rozpoczecia,
	    link=t.link,
	    opis=t.opis,
	    polymorphic_ctype_id=107
	FROM k_tmp t
	WHERE k.id = t.id;

INSERT INTO public.kalendarz_wydarzeniekalendarzowe (id, nazwa, data_rozpoczecia, link, opis, polymorphic_ctype_id)
SELECT t.id, t.nazwa, t.data_rozpoczecia, t.link, t.opis, 107
FROM k_tmp t
LEFT JOIN public.kalendarz_wydarzeniekalendarzowe w ON t.id = w.id
WHERE w.id IS NULL;

COMMIT;