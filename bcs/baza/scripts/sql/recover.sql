BEGIN;

-- Step 1: Create a temporary table to stage incoming data
CREATE TEMP TABLE osoba_tmp (
    id INTEGER PRIMARY KEY,
    imie TEXT,
    nazwisko TEXT,
    przezwiska TEXT[],
    polymorphic_ctype_id INTEGER
);

-- Step 2: Load data into the temporary table
COPY osoba_tmp (id, imie, nazwisko, przezwiska, polymorphic_ctype_id) FROM stdin;
11	Aleksandra	Klekocińska	{}	60
...
193	XXX		{Spumante}	60
\.

-- Step 3: Update existing records in the target table
UPDATE public.osoby_osoba o
SET
    imie = t.imie,
    nazwisko = t.nazwisko,
    przezwiska = t.przezwiska,
    polymorphic_ctype_id = t.polymorphic_ctype_id
FROM osoba_tmp t
WHERE o.id = t.id;

-- Step 4: Insert new records that do not exist in the target table
INSERT INTO public.osoby_osoba (id, imie, nazwisko, przezwiska, polymorphic_ctype_id)
SELECT t.id, t.imie, t.nazwisko, t.przezwiska, t.polymorphic_ctype_id
FROM osoba_tmp t
LEFT JOIN public.osoby_osoba o ON o.id = t.id
WHERE o.id IS NULL;

COMMIT;
