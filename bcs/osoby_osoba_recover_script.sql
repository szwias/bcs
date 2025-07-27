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
12	Aleksandra	Król	{}	60
13	Aleksandra	Wagner	{}	60
14	Alicja	Majczak	{}	60
15	Alicja Waleria	Barć	{}	60
16	Amelia	Boufenghour	{}	60
17	Aneta	Galara	{}	60
21	Anna	Stachowiak	{}	60
18	Anna	Łopatniuk	{}	60
20	Anna	Pawlicka	{}	60
22	Anna	Wyroba	{}	60
19	Anna Maria	Kuźma	{}	60
23	Antoni	Krzyżanowski	{}	60
24	Artur	Biba	{}	60
25	Artur	Czajkowski	{}	60
26	Artur	Halcarz	{}	60
27	Artur	Miadzielec	{}	60
28	Artur	Szymański	{}	60
30	Bartłomiej	Olajossy	{}	60
29	Bartłomiej	Grzeszykowski	{}	60
32	Bartosz	Maciejewski	{}	60
31	Bartosz	Hepek	{}	60
33	Bartosz	Sieniawski	{}	60
34	Bartosz	Spytkowski	{}	60
35	Beanus	Perennus	{}	60
36	Benedykt Mateusz	Dzięcielski	{}	60
37	Błażej	Hałat	{}	60
38	Camilla	Schindler	{}	60
39	Cezary	Sołtysik	{}	60
40	Christine	Przybyła-Kowalska	{}	60
177	Czapka		{}	60
41	Damian	Zych	{Buch}	60
42	Daniel	Zgliński	{}	60
43	Dawid	Wiklik	{}	60
44	Dominik	Ciebiera	{}	60
45	Dominika	Liszka	{}	60
46	Dominika	Szponar	{}	60
47	Dorota	Drożyńska	{}	60
48	Elżbieta	Mierzejewska	{}	60
173	Elżunia	Krasiejko	{}	60
49	Eryk	Królczyk	{}	60
50	Ewa	Smuga-Codutti	{}	60
174	Feliks	Kwiatkowski	{}	60
51	Gabriela	Michalik (Mucha)	{}	60
52	Gniewko	Wawrzyńczak	{}	60
53	Grażyna	Malinowska	{}	60
55	Grzegorz	Lebedowicz	{}	60
54	Grzegorz	Dziadek	{}	60
56	Herman	Chekurda	{}	60
57	Jacek	Onisk	{}	60
59	Jakub	Kornacki	{}	60
60	Jakub	Łukasik	{}	60
58	Jakub	Bukalski	{}	60
61	Jakub	Nawrot	{}	60
63	Joanna	Lorenc	{}	60
62	Joanna	Krawczyk	{}	60
64	John	Graff-Warburton	{}	60
65	Julia	Jurczuk	{}	60
66	Julia	Musiał	{}	60
67	Kamila	Dziewońska (Paisley)	{}	60
68	Kamila	Rozesłaniec	{}	60
70	Karol	Starowicz	{}	60
72	Karolina	Kania	{}	60
71	Karolina	Dzierżawska	{}	60
73	Karolina	Mater	{}	60
74	Karolina	Szklanny	{}	60
75	Karolina	Wielgus	{}	60
69	Karol Konrad	Czekałowski	{}	60
76	Kasper	Krawet	{}	60
77	Katarzyna	Marek	{}	60
78	Katarzyna	Ostrowska	{}	60
79	Katarzyna	Smuga	{}	60
80	Katarzyna	Żanowska	{}	60
81	Kinga	Radwan	{}	60
82	Klaudia	Buchalska	{}	60
84	Konrad		{}	60
85	Konrad	Piwowarczyk	{}	60
165	Krzysztof	Trela	{}	60
87	Krzysztof	Tomczyk	{}	60
86	Krzysztof	Sadowski	{}	60
88	Ludwik	Janiszewski	{}	60
89	Łukasz	Ciepły (Lindert)	{}	60
90	Łukasz	Pryk	{}	60
91	Ma	Rysia	{}	60
95	Maciej	Małecki	{}	60
94	Maciej	Lisowski	{}	60
92	Maciej	Hyla	{}	60
93	Maciej	Krzyżanek	{}	60
96	Maciej	Solon	{}	60
97	Magdalena	Brilha	{}	60
98	Maksymilian	Depa	{}	60
99	Małgorzata	Głuszek	{}	60
100	Małgorzata	Lurzyńska	{}	60
6	Krysia	Cholewa	{}	61
9	Patrycja	Skowronek	{"Wiktoriańskie Dziecko"}	61
101	Małgorzata	Żurek	{}	60
102	Marceli	Mart-Łakomy	{}	60
103	Marcin	Loch	{}	60
105	Maria	Turakiewicz	{}	60
178	Szymon	Zwias	{Tur}	61
181	Babcia	Tadka	{}	56
184	Roberto	Martinez del Rio	{}	56
104	Maria	Babiuch	{}	60
106	Marta	Toumia	{}	60
107	Martyna	Kubiak	{}	60
109	Mateusz	Tomczyk	{}	60
110	Mateusz	Żurek	{}	60
108	Mateusz	Sułek	{}	60
116	Michał	Malata	{Mamut}	60
113	Michał	Gumułka	{}	60
112	Michał	Boryka	{}	60
167	Dawid	Otłowski	{}	60
7	Mateusz	Sokół	{Scorpio,Szczur,Scoppiato}	61
179	Wiktoria	Doleżych	{Wedel}	61
185	SSUJ		{}	56
187	Zdzisław	Gajda	{Profesor}	56
5	Konrad		{Austriak}	61
8	Mateusz	Warmus	{"Najpiękniejszy Bean"}	61
180	Andrzej	Pawłowski	{}	56
183	Frederic	Widart	{}	56
186	Stefano	Campagna	{"Kwaśny Krab"}	56
1	Adrianna	Kapelak	{}	60
2	Agata	Grochowina	{}	60
3	Agnieszka	Albrychiewicz	{}	60
10	Aleksander	Wędrychowski	{}	60
115	Michał	Lenik	{}	60
114	Michał	Kasperek	{}	60
111	Michalina	Kokosińska	{}	60
118	Monika	Kwater-Boryka	{}	60
117	Monika	Góralik	{}	60
119	Monika	Stępień	{}	60
121	Natalia	Lisowska	{}	60
122	Natalia	Stachura	{}	60
120	Natalia	Ciesielska (Olajossy)	{}	60
171	Nie	dotyczy	{}	60
170	Nie	wiem	{}	60
123	Olga	Wajda	{}	60
124	Pamela Anna	Drozd	{}	60
125	Patrycja	Karauda	{}	60
127	Patrycja	Szaniawska	{}	60
126	Patrycja	Malinowska-Majdak	{}	60
128	Patryk	Gujda	{}	60
129	Paula	Dybowska	{}	60
130	Paulina	Kozioł	{}	60
131	Paulina	Tomżyńska	{}	60
132	Paweł	Grzegorczyk	{}	60
134	Paweł	Nawrot	{}	60
133	Paweł	Mucha	{}	60
136	Piotr	Litwin	{}	60
135	Piotr	Bulica	{}	60
137	Piotr	Szewczyk	{}	60
138	Piotr	Szota	{}	60
139	Przemysław	Jankowski	{}	60
140	Richard	Staryszak	{}	60
141	Robert	Ścieszka	{}	60
142	Roksana	Kidawa	{}	60
143	Sandra	Chandzlik	{}	60
144	Sebastian	Stala	{}	60
145	Stanisław	Stokłosa	{}	60
146	Stefan	Bocheński	{}	60
147	Szymon	Stankiewicz	{}	60
148	Tadeusz	Hessel	{}	60
150	Tomasz	Krok	{}	60
149	Tomasz	Andrzej Cieciora	{}	60
151	Urszula	Kasprzyk	{}	60
152	Wacław	Chmiel	{}	60
153	Wawrzyniec	Ordziniak	{}	60
154	Weronika	Manista	{}	60
172	Weronika	Marchewka	{}	60
155	Wiktor	Sobol	{}	60
156	Wiktoria	Kałka	{}	60
158	Zofia	Krasińska-Krawet	{}	60
159	Zuzanna	Żmuda	{}	60
4	Kacper	Wilk	{Szogun,"Czwarty Wilk Noboda"}	61
188	Profesor	Czerwiński	{}	56
189	NZS UJ		{}	56
190	Ktoś	Cubuk	{}	69
157	Zdzisław	Gajda	{}	60
182	Christobalt	Miltrugno	{}	56
191	Loïc	Smars	{}	56
192	Olga	Zatońska	{}	69
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
