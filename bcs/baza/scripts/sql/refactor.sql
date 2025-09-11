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
74	2012-03-29	10	5	f	t
73	2012-03-24	3	5	f	t
76	2012-04-21	16	5	f	t
77	2012-05-12	3	5	f	t
51	2011-10-27	35	5	f	t
79	2012-05-18	13	5	f	t
81	2012-05-19	23	6	t	t
33	2011-05-28	23	6	t	t
80	2012-05-18	3	5	f	t
84	2012-06-29	22	5	f	t
85	2012-07-01	28	5	f	t
88	2012-10-01	20	5	f	t
89	2012-10-03	18	5	f	t
90	2012-10-05	3	5	f	t
92	2012-10-06	35	5	f	t
93	2012-10-24	10	5	f	t
94	2012-11-02	23	4	t	t
95	2012-12-06	5	5	f	t
87	2012-08-05	23	4	t	f
86	2012-07-31	36	5	f	f
83	2012-09-30	1	5	f	f
116	2013-12-18	32	5	f	t
96	2012-12-07	5	5	f	f
97	2013-02-20	2	5	f	t
99	2013-03-07	31	5	f	t
38	2011-07-21	2	5	f	t
100	2013-03-08	10	5	f	t
101	2013-03-20	16	5	f	t
102	2013-04-13	3	5	f	t
104	2013-05-28	10	5	f	t
105	2013-06-01	2	5	f	t
106	2013-10-06	12	5	f	f
107	2013-10-04	3	5	f	t
109	2013-10-05	28	5	f	t
110	2013-11-06	10	5	f	t
108	2013-10-23	10	5	f	t
112	2013-11-14	16	5	f	t
114	2013-12-05	10	5	f	t
113	2013-11-30	29	5	f	t
117	2014-02-27	31	5	f	t
118	2014-03-07	3	5	f	t
120	2014-04-04	23	3	t	t
122	2014-04-27	33	5	f	t
123	2014-05-09	35	5	f	t
126	2014-05-16	3	5	f	t
125	2014-05-17	13	5	f	f
128	2014-06-27	3	5	f	t
129	2014-06-28	25	5	f	t
130	2014-10-04	12	5	f	f
131	2014-10-23	18	5	f	t
133	2014-11-06	10	5	f	t
134	2014-11-21	19	5	f	t
103	2013-05-14	13	5	f	f
9	2011-01-16	3	5	f	t
25	2010-05-12	20	5	f	t
11	2011-02-12	3	5	f	t
27	2011-03-05	21	5	f	t
67	2012-02-09	33	5	f	t
66	2012-02-12	23	4	t	t
39	2011-09-16	28	5	f	t
40	2011-09-16	3	5	f	t
1	2009-08-20	8	5	f	t
15	2011-03-25	6	5	f	t
12	2011-03-12	3	5	f	t
14	2011-03-18	5	5	f	t
16	2011-04-03	17	5	f	t
18	2011-04-16	3	5	f	t
22	2011-05-14	3	5	f	t
21	2011-05-07	24	5	f	t
20	2011-04-30	25	5	f	t
17	2011-04-06	5	5	f	t
24	2010-04-28	5	5	f	t
3	2010-01-28	3	5	f	t
41	2011-09-29	17	5	f	t
19	2011-04-19	16	5	f	t
30	2011-05-21	13	5	f	t
31	2011-05-21	3	5	f	t
32	2011-05-23	26	5	f	t
34	2011-06-02	14	5	f	t
35	2011-06-04	16	5	f	t
36	2011-06-30	27	5	f	t
37	2011-07-04	27	5	f	t
50	2011-10-23	17	5	f	t
42	2011-10-01	12	5	f	t
52	2011-11-04	10	5	f	t
54	2011-11-07	20	5	f	t
57	2011-11-17	31	5	f	t
44	2011-10-06	10	5	f	t
47	2011-10-07	2	5	f	t
48	2011-10-20	10	5	f	t
49	2011-10-22	30	5	f	t
53	2011-11-05	22	5	f	t
56	2011-11-12	31	5	f	t
58	2011-11-27	3	5	f	t
60	2011-12-01	10	5	f	t
64	2011-12-17	32	5	f	t
65	2012-01-15	18	5	f	t
70	2012-03-01	14	5	f	t
72	2012-03-16	34	5	f	t
26	2025-05-11	23	4	t	f
23	2011-05-21	1	5	f	f
61	2011-12-05	23	4	t	f
55	2011-11-16	23	4	t	f
62	2011-12-16	38	5	f	t
46	2011-10-07	29	5	f	t
8	2010-11-06	20	5	f	t
6	2010-10-01	12	5	f	t
135	2014-11-28	37	5	f	t
136	2014-12-07	14	5	f	t
137	2014-12-17	3	5	f	t
139	2015-03-05	10	5	f	t
140	2015-03-14	34	5	f	t
141	2015-03-27	3	5	f	t
142	2015-04-10	23	3	t	t
143	2015-05-10	13	5	f	f
145	2015-05-08	3	5	f	t
144	2015-06-10	10	5	f	t
147	2015-06-12	9	5	f	t
148	2015-06-30	29	5	f	t
150	2015-10-15	10	5	f	t
152	2015-11-05	10	5	f	t
153	2015-11-14	3	5	f	t
154	2015-11-21	19	5	f	t
155	2015-11-25	35	5	f	t
156	2015-12-19	38	5	f	t
158	2015-12-19	3	5	f	t
159	2016-01-20	10	5	f	t
160	2016-01-07	10	5	f	t
162	2016-03-05	3	5	f	t
163	2016-03-16	34	5	f	t
164	2016-03-31	10	5	f	t
165	2016-04-13	10	5	f	t
166	2016-04-24	23	3	t	f
168	2016-05-14	13	5	f	f
167	2016-05-05	10	5	f	t
171	2016-06-01	10	5	f	t
172	2016-06-11	9	5	f	t
173	2016-09-25	23	1	t	f
174	2016-09-30	28	5	f	t
175	2016-10-02	12	5	f	f
180	2016-11-13	10	5	f	t
178	2016-10-26	18	5	f	t
196	2017-05-14	13	5	f	f
179	2016-11-17	10	5	f	t
182	2016-11-19	40	5	f	t
184	2016-12-07	16	5	f	t
185	2016-12-17	10	5	f	t
186	2015-04-30	25	5	f	t
188	2017-01-12	10	5	f	t
189	2017-01-21	10	5	f	t
190	2017-03-04	3	5	f	t
191	2017-03-14	10	5	f	t
192	2017-03-24	23	3	t	t
193	2017-03-30	23	3	t	t
194	2017-04-05	2	5	f	t
195	2017-04-20	17	5	f	t
197	2017-05-12	3	5	f	t
199	2017-05-24	10	5	f	t
200	2017-06-01	10	5	f	t
201	2017-06-03	21	5	f	t
203	2017-06-10	9	5	f	t
204	2017-09-18	23	8	t	f
205	2017-10-01	12	5	f	f
206	2017-10-12	18	5	f	t
208	2017-10-25	10	5	f	t
209	2017-11-10	3	5	f	t
210	2017-11-25	19	5	f	t
211	2017-11-29	39	5	f	t
212	2017-12-06	10	5	f	t
213	2017-12-16	32	5	f	t
214	2018-01-11	10	5	f	t
215	2018-01-20	35	5	f	t
216	2018-02-01	10	5	f	t
217	2018-02-18	10	5	f	t
218	2018-02-28	10	5	f	t
151	2015-10-22	18	5	f	t
219	2018-03-18	23	3	t	f
220	2018-03-18	10	5	f	f
221	2018-04-04	41	5	f	t
222	2018-04-07	5	5	f	t
223	2018-04-14	3	5	f	t
224	2018-04-28	10	5	f	t
225	2018-05-11	5	5	f	t
269	2020-01-16	10	5	f	t
227	2018-05-20	13	5	f	f
228	2018-05-18	3	5	f	t
230	2018-06-09	9	5	f	t
232	2018-09-08	9	5	f	t
233	2018-09-24	23	1	t	f
234	2018-10-01	12	5	f	f
236	2018-09-28	8	5	f	t
237	2018-10-17	41	5	f	t
238	2018-10-24	18	5	f	t
239	2018-11-13	39	5	f	t
240	2018-11-23	3	5	f	t
241	2018-11-30	37	5	f	t
242	2018-12-01	2	5	f	t
243	2018-12-05	39	5	f	t
244	2018-12-05	10	5	f	t
245	2018-12-15	32	5	f	t
246	2019-01-17	10	5	f	t
247	2019-02-16	2	5	f	t
248	2019-02-27	10	5	f	t
249	2019-03-15	3	5	f	t
250	2019-03-20	14	5	f	t
251	2019-03-29	23	3	t	t
252	2019-04-06	8	5	f	t
270	2020-02-21	10	5	f	t
253	2019-05-26	13	5	f	f
255	2019-05-24	3	5	f	t
256	2019-06-07	17	5	f	t
257	2019-06-07	14	5	f	t
258	2019-06-08	9	5	f	t
259	2019-09-19	23	1	t	f
260	2019-09-24	2	5	f	t
271	2020-02-28	41	5	f	t
261	2019-10-01	12	5	f	f
263	2019-10-09	18	5	f	t
264	2019-11-30	39	5	f	f
265	2019-11-22	5	5	f	t
266	2019-11-22	3	5	f	t
267	2019-12-04	10	5	f	t
268	2019-12-14	32	5	f	t
274	2020-06-30	9	5	f	t
275	2020-10-08	18	5	f	t
272	2020-05-15	10	5	f	t
276	2020-10-24	42	5	f	t
277	2020-11-05	43	5	f	t
278	2020-12-09	43	5	f	t
279	2020-12-28	43	5	f	t
281	2021-02-12	43	5	f	t
282	2021-02-27	28	5	f	t
273	2020-06-06	2	5	f	t
235	2018-09-08	16	5	f	t
284	2021-04-22	43	5	f	t
285	2021-06-02	10	5	f	t
283	2021-02-12	10	5	f	t
287	2021-06-18	2	5	f	t
288	2021-06-30	9	5	f	t
289	2021-10-02	12	5	f	f
291	2021-09-30	3	5	f	t
292	2021-10-22	18	5	f	t
293	2021-11-10	3	5	f	t
294	2021-11-06	7	5	f	t
295	2021-11-11	21	5	f	t
297	2021-11-13	19	5	f	t
298	2021-11-13	29	5	f	t
300	2021-11-16	8	5	f	t
301	2021-11-22	1	5	f	t
302	2021-11-26	35	5	f	t
303	2021-12-09	10	5	f	t
304	2021-12-16	40	5	f	t
305	2021-12-16	3	5	f	t
306	2022-01-13	10	5	f	t
307	2022-01-22	10	5	f	t
335	2023-01-26	10	5	f	t
308	2022-02-03	8	5	f	t
309	2022-02-03	8	5	f	t
310	2022-02-11	10	5	f	t
311	2022-02-12	28	5	f	t
312	2022-03-03	14	5	f	t
313	2022-03-09	28	5	f	t
314	2022-03-09	28	5	f	t
315	2022-03-26	10	5	f	t
316	2022-03-26	39	5	f	t
317	2022-04-01	23	3	t	t
318	2022-04-22	3	5	f	t
319	2022-04-23	17	5	f	t
320	2022-05-23	13	5	f	f
321	2022-06-06	6	5	f	t
322	2022-06-11	41	5	f	t
323	2022-09-24	23	1	t	f
336	2023-02-10	10	5	f	t
325	2022-10-02	12	5	f	f
326	2022-10-21	18	5	f	t
324	2022-09-30	3	5	f	t
328	2022-11-14	39	5	f	t
329	2022-11-17	3	5	f	t
331	2022-12-17	32	5	f	t
330	2022-12-01	37	5	f	t
333	2022-12-07	10	5	f	t
334	2023-01-12	10	5	f	t
337	2023-02-24	10	5	f	t
339	2023-03-09	10	5	f	t
338	2023-03-17	3	5	f	t
341	2023-03-30	10	5	f	t
342	2023-04-13	10	5	f	t
343	2023-05-21	13	5	f	f
345	2023-05-21	3	5	f	t
346	2023-06-02	10	5	f	t
348	2023-06-16	10	5	f	t
349	2023-06-30	9	5	f	t
350	2023-10-01	12	5	f	f
352	2023-09-29	3	5	f	t
353	2023-10-12	41	5	f	t
354	2023-10-19	18	5	f	t
355	2023-10-26	10	5	f	t
356	2023-11-12	40	5	f	t
357	2023-11-15	3	5	f	t
358	2023-11-26	40	5	f	t
359	2023-11-30	10	5	f	t
360	2023-12-03	40	5	f	t
361	2023-12-06	10	5	f	t
362	2023-12-15	32	5	f	t
363	2013-05-10	3	5	f	t
364	2011-10-02	3	5	f	t
365	2014-10-03	3	5	f	t
366	2016-09-30	3	5	f	t
367	2017-09-29	3	5	f	t
368	2018-09-28	3	5	f	t
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
74	Czapkowy ostry dyżur 6 - Pożegnanie z Anną-Marią!	""	2012-03-29	""
73	Karczma wiosenna pt. “Powitanie semestru”	""	2012-03-24	""
76	Zebranie w sprawie statutu Bractwa	""	2012-04-21	""
77	Karczma piwna przed Juwenaliową	""	2012-05-12	""
51	Oktoberfest	""	2011-10-27	""
79	Juwenalia 2012	""	2012-05-16	""
81	Stiftungfest	""	2012-05-19	""
33	Wyjazd na Stiftungfest	Aśka Lorenc: "Wyjazd na Stiftungfest do Opola - rewizyta u zaprzyjaźnionej korporacji Salia Silesia"	2011-05-28	""
80	Juwenaliowa Karczma Piwna z Belgami!	""	2012-05-18	""
84	Wakacyjna posiadówka czapkowa - zamiast odwiedzin u profesora	""	2012-06-29	""
85	Czapka podbija świat! Edycja Druga	""	2012-07-01	""
88	Inauguracja roku akademickiego 2012/2013	""	2012-10-01	""
89	Czapkowe wybory	""	2012-10-03	""
90	Karczma Reaktywacyjna 3	""	2012-10-05	""
92	Czapka Open Party	""	2012-10-06	""
93	Ostry Dyżur 2012 vol.1	""	2012-10-24	""
94	Bankiet Europejski	""	2012-11-02	""
95	'O obyczajowości żaków krakowskich w XVI wieku', Mariusz Wolny	""	2012-12-06	""
87	Czapka na Pine Gouine 4: Rabelais	""	2012-08-03	""
86	Ordre de la Bretelle - wakacyjne odwiedziny	""	2012-07-27	""
83	Promuję Bractwo - umieszczam informację o jego stronie	""	2012-06-18	""
116	Karczma wigilijna BCS UJ 2013	""	2013-12-18	""
96	'O obyczajowości żaków krakowskich w XVI wieku', Mariusz Wolny	""	2012-12-06	""
97	Jacobs Czapka Winter Special	Cubuk zgubił czapkę - Pumba zrobił wydarzenie, żeby pokazać jej losy	2013-02-20	""
99	GAUDEAMUS - czapkowe śpiewanie	""	2013-03-07	""
38	Petycja w sprawie niezamykania Klubu "Buda"	Klub jest zamknięty z powodu remontu akademika i Czapka organizuje petycję.	2011-07-21	""
100	Ostry Dyżur 2013	""	2013-03-08	""
101	Walne Zgromadzenie BCS UJ	""	2013-03-20	""
102	Karczma wiosenna 2013 BCS UJ	""	2013-04-13	""
104	Majowy Ostry Dyżur	""	2013-05-28	""
105	Loża medyków (zjazd absolwentów z lat 1952-1957)  zaprasza reprezentację Czapki	""	2013-06-01	""
106	Reactivation Party V	""	2013-09-30	""
107	Karczma Reaktywacyjna	""	2013-10-04	""
109	Czapka zdobywa świat 2.0	""	2013-10-05	""
110	Ostry dyżur - vol. 2	""	2013-11-06	""
108	Ostry dyżur czas zacząć! - vol. 1	""	2013-10-23	""
112	Walne Zgromadzenie BCS UJ	""	2013-11-14	""
114	Ostry Dyżur - vol. 4	""	2013-12-05	""
113	Wizyta u Profesora	""	2013-11-30	""
117	Lekcja śpiewania z BCS UJ 2014	""	2014-02-27	""
118	Tradycyjna Karczma BCS UJ	""	2014-03-07	""
120	Kudłacze	""	2014-04-04	""
122	Wiosenny Obiad BCS UJ	""	2014-04-27	""
123	Piątkowa balanga w Budzie	""	2014-05-09	""
126	Karczma Juwenaliowa 2014	""	2014-05-16	""
125	Juwenalia 2014	""	2014-05-13	""
128	Karczma Posesyjna BCS UJ	""	2014-06-27	""
129	Grill u profesora Gajdy	""	2014-06-28	""
130	Czapka Reactivation Party VI	""	2014-10-03	""
131	Wybory Zarządu BCS UJ	""	2014-10-23	""
133	Ostry Dyżur vol.1 z BCS UJ	""	2014-11-06	""
134	Ułańskie Zdrowie	""	2014-11-21	""
103	Juwenalia 2013	""	2013-05-07	""
9	Czapkowa Karczma Karnawałowa	""	2011-01-16	""
25	Złożenie kwiatów pod grobem królowej Jadwigi	""	2010-05-12	""
11	Czapkowa Karczma Posesyjna	""	2011-02-12	""
27	Puchar Prorektora CMUJ	""	2011-03-05	""
67	Obiad posesyjny	""	2012-02-09	""
66	Wyjazd do Belgii	""	2012-02-08	""
39	Czapka zdobywa świat!	Pierwsza edycja konkursu, w którym członkowie BCS przysyłają swoje czapki z różnych stron świata, w których spędzają wakacje.	2011-07-23	""
40	Czapkowa karczma zwycięzców	""	2011-09-16	""
1	Założenie BCS	Aśka Lorenc: "data powstania Bractwa Czapki Studenckiej. Oprócz noszenia czapek ważny jest folklor studencki: integracja, śpiew, wymienianie się pinsami, koleżeństwo. \r\nCzapka działa w ramach Collegium Medicum UJ. Wielu studentów ze wszystkich wydziałów posiada swoje własne czapki. "	2009-08-20	""
15	Konferencja medyczna we Wrocławiu	Aśka Lorenc: "Czapka medyczna (i nie tylko) wpada do Wrocławia. We Wrocławiu ma miejsce konferencja medyczna i twórcy Czapki chcą skorzystać z okazji, by promować zwyczaj jej noszenia. "	2011-03-25	""
12	Wielka Karczma Piwna	""	2011-03-12	""
14	Wykład dla Stowarzyszenia Absolwentów UJ	Wykład Tadeusza na temat czapki studenckiej UJ dla Stowarzyszenia Absolwentów UJ (piwnica przy ul. Grodzkiej 53)	2011-03-18	""
16	Wycieczka na Kopiec Kościuszki	Aśka Lorenc: "Studenci wielu wydziałów bierają się pod akademikiem Żaczek i wspólnie idą na Kopiec Kościuszki, śpiewając m.in pieśni żołnierskie. "	2011-04-03	""
18	Czapkowa Karczma w klimatach międzywojennych	""	2011-04-16	""
22	Majowa Karczma Piwna	""	2011-05-14	""
21	Czapkowa eskapada rowerowa szlakiem Bema	""	2011-05-07	""
20	Grill pod Żaczkiem: urodziny Geologa	""	2011-04-30	""
17	Wykład na Wydziale Polonistyki	""	2011-04-06	""
24	Prelekcja Roberto o folklorze studenckim	""	2010-04-28	""
3	Pierwsza karczma	""	2010-01-28	""
41	Wycieczka do browaru w Tychach	""	2011-09-29	""
19	Spotkanie statutowe BCS	""	2011-04-19	""
30	Juwenalia 2011	""	2011-05-19	""
31	Polsko-belgijsko-francuska Karczma Piwna	""	2011-05-21	""
32	Rozśpiewany rejs	""	2011-05-23	""
34	Wizyta w Muzeum Anatomii	""	2011-06-02	""
35	Wybory wydziałowych reprezentanów do Zarządu oraz Zarządu "Centralnego"	""	2011-06-04	""
36	Czapka dołącza do koncertu Vacancy & Los Purkos	""	2011-06-30	""
37	Koncert Jurka Bożyka	""	2011-07-04	""
50	Oprowadzanie pierwszaków szlakiem historycznouniwersytecko-baromlecznym	""	2011-10-23	""
42	Czapka Reactivation Party 2	""	2011-10-01	""
52	Czapkowy Ostry Dyżur 3 - "Morska fala"	""	2011-11-04	""
54	Uniwersytecki Dzień Pamięci	""	2011-11-07	""
57	Wspólne śpiewanie piosenek rajdowych z prof. Czerwińskim, organizatorem rajdów Eskulapów	""	2011-11-17	""
44	Ostry Dyżur czapkowy - spotkanie informacyjne BCS	""	2011-10-06	""
47	Tour des bars	""	2011-10-07	""
48	Ostry Dyżur Czapkowy	""	2011-10-20	""
49	Wywiad czapek dla MMKrakow.pl	""	2011-10-22	""
53	Spontaniczna czapkowa posiadówka na Woli	""	2011-11-05	""
56	43 lekcja śpiewania w Święto Niepodległości z Loch Camelot	""	2011-11-12	""
58	Karczma Andrzejkowa	""	2011-11-27	""
60	Czapkowy Ostry Dyżur 4	""	2011-12-01	""
64	Wigilia BCS UJ	""	2011-12-17	""
65	Wybory - Wielki Mistrz, Kasztelan, Skarbnik	""	2012-01-15	""
70	Czapkowe wyjście kulturalne nr 1 w 2012	""	2012-03-01	""
72	Idy Marcowe	""	2012-03-16	""
26	Faerie Matricularum	""	2025-05-08	""
23	Przygarnij Belga w Juwenalia!	nocleg w czasie Juwenaliów	2011-05-17	""
61	Bankiet Tradycji Studenckich	""	2011-12-03	""
55	Czapka na CIBA	""	2011-11-11	""
62	Kolędowanie pod Novum wraz z NZS UJ	""	2011-12-16	""
46	Kawa czy Herbata a w niej czapka!	""	2011-10-07	""
8	Uniwersytecki Dzień Pamięci	Aśka Lorenc: "Bractwo  biorze udział w Uniwersyteckim Dniu Pamięci (rocznicy Sondernaktion Krakau) - dużo fotek tego dnia robiła nam Anka Kaczmarz z Dziennika Polskiego (miała nam je wysłać i nie wysłała!).	2010-11-06	""
6	Czapka Reactivation Party	Aśka Lorenc: "Bractwo spotyka się dość spontanicznie. Większość członków stanowią osoby z CMUJ, ale spotkania są organizowane w taki sposób, aby włączyć jak najwięcej osób. "	2010-10-01	""
135	Czapkowe Andrzejki z BCS UJ	""	2014-11-28	""
136	Czapkowe mikołajkowe wyjście do Muzeum Armii Krajowej	""	2014-12-07	""
137	Karczma Wigilijna 2014	""	2014-12-17	""
139	Ostry Dyżur Przedwiosenny	""	2015-03-05	""
140	Idy Czapkowe 2015	""	2015-03-14	""
141	Karczma Wiosenna 2015	""	2015-03-27	""
142	Kudłacze vol. 3 - szalony wypad w góry Czapki Studenckiej	""	2015-04-10	""
143	Juwenalia 2015	""	2015-05-07	""
145	Karczma Juwenaliowa 2015	""	2015-05-08	""
144	Ostry Dyżur Przedsesyjny	""	2015-06-10	""
147	Ognisko przedsesyjne	""	2015-06-12	""
148	Tres faciunt collegium: grill u Profesora	""	2015-06-30	""
150	Ostry dyżur vol. 1	""	2015-10-15	""
152	Piracki Ostry Dyżur	""	2015-11-05	""
153	Karczma Jesienna BCS UJ	""	2015-11-14	""
154	Ułańskie Zdrowie	""	2015-11-21	""
155	Western Party BCS UJ	""	2015-11-25	""
156	Kolędowanie pod Collegium Novum	""	2015-12-19	""
158	Karczma Wigilijna BCS UJ	""	2015-12-19	""
159	Styczniowy Ostry Dyżur	""	2016-01-20	""
160	Sylwester z Czapką	""	2016-01-07	""
162	Karczma Wiosenna BCS UJ	""	2016-03-05	""
163	Idy Marcowe	""	2016-03-16	""
164	Poświąteczny Ostry Dyżur	""	2016-03-31	""
165	Kwietniowy Ostry Dyżur	""	2016-04-13	""
166	Rajd BCS UJ na Kudłacze 2016	""	2016-04-22	""
168	Juwenalia 2016	""	2016-05-12	""
167	Majowy Ostry Dyżur	""	2016-05-05	""
171	Czerwcowy Ostry Dyżur	""	2016-06-01	""
172	Ognisko przedsesyjne BCS UJ	""	2016-06-11	""
173	Czapkowy Adapciak 2016	""	2016-09-22	""
174	Konkurs Wakacyjny	""	2016-09-30	""
175	Reaktywacja BCS UJ	""	2016-09-30	""
180	Listopadowy Ostry Dyżur	""	2016-11-13	""
178	Wybory zarządu VIII kadencji BCS UJ + Walne Zgromadzenie	""	2016-10-26	""
196	Juwenalia 2017	""	2017-05-11	""
179	Drugi Listopadowy Ostry Dyżur	""	2016-11-17	""
182	Fantastyczne Czapki i jak je znaleźć	""	2016-11-19	""
184	Walne Zgromadzenie	""	2016-12-07	""
185	Wigilia Czapkowa	""	2016-12-17	""
186	Ruszt u Małeckiego	""	2015-04-30	""
188	Styczniowy Ostry Dyżur	""	2017-01-12	""
189	Styczniowy Ostry Dyżur II	""	2017-01-21	""
190	Wiosenna Karczma	""	2017-03-04	""
191	Marcowy Ostry Dyżur	""	2017-03-14	""
192	Kudłacze 2017	""	2017-03-24	""
193	Marcowy Ostry Dyżur II	""	2017-03-30	""
194	Cercle Marie Haps vs Czapka Studencka : Calotte vs Czapka	""	2017-04-05	""
195	Rewizyta Żółtego Szalika	""	2017-04-20	""
197	Karczma juwenaliowa	""	2017-05-12	""
199	Majowy Ostry Dyżur	""	2017-05-24	""
200	Czerwcowy Ostry Dyżur	""	2017-06-01	""
201	Zakończenie sezonu na izoarenie	""	2017-06-03	""
203	Ognisko Przedsesyjne 2017	""	2017-06-10	""
204	Czapkowy obóz integracyjny 2017	""	2017-09-15	""
205	Reaktywacja BCS UJ	""	2017-09-29	""
206	Wybory Czapkowe - Walne Zgromadzenie	""	2017-10-12	""
208	Październikowy Ostry Dyżur	""	2017-10-25	""
209	Jesienna Karczma BCS UJ	""	2017-11-10	""
210	Ułańskie Zdrowie	""	2017-11-25	""
211	Wielka Rekrutacja 2017	""	2017-11-29	""
212	Mikołajkowy Ostry Dyżur	""	2017-12-06	""
213	Wigilia Czapkowa	""	2017-12-16	""
214	Styczniowy Ostry Dyżur	""	2018-01-11	""
215	Czapkowy Bal Karnawałowy	""	2018-01-20	""
216	Ostry Dyżur a La Calotte	""	2018-02-01	""
217	Ostry Dyżur - piwoterapia złamanych serc	""	2018-02-18	""
218	Posesyjny Ostry Dyżur	""	2018-02-28	""
151	Walne Zgromadzenie BCS UJ 2015/2016	Obietnice wyborcze:\r\n- ustanowienie kalendarza imprez	2015-10-22	""
219	Kudłacze 2018	""	2018-03-16	""
220	Wiosenny Ostry Dyżur	""	2018-03-21	""
221	Depositio Beanorum	""	2018-04-04	""
222	Czapka studencka oznaką prawdziwego żaka II	""	2018-04-07	""
223	Karczma Wiosenna BCS UJ	""	2018-04-14	""
224	Kwietniowy Ostry Dyżur	""	2018-04-28	""
225	Europejskie i polskie tradycje studenckie	""	2018-05-11	""
269	Piżama CzaParty - Przedsesyjny Ostry Dyżur	""	2020-01-16	""
227	Juwenalia 2018	""	2018-05-16	""
228	Międzynarodowa Karczma	""	2018-05-18	""
230	Ognisko Przedsesyjne BCS UJ	""	2018-06-09	""
232	Walne Zgromadzenie	Nadanie dewizy "In varietate unitas", przyjęcie statutu zgodnego z UJ, przyjęcie nowego herbu Bractwa (autor: Robert Fidura)	2018-09-08	""
233	Adapciak BCS UJ	""	2018-09-21	""
234	Reaktywacja 2018	""	2018-09-28	""
236	Pakt Bractw w Bractwem Żółtego Szalika	""	2018-09-28	""
237	Depositio Beanorum	""	2018-10-17	""
238	Wybory	""	2018-10-24	""
239	Wielka Rekrutacja BCS UJ	""	2018-11-13	""
240	Karczma Jesienna 2018	""	2018-11-23	""
241	Andrzejki BCS UJ	""	2018-11-30	""
242	Starej czapkowej gwardii spotkanie na szczycie	""	2018-12-01	""
243	Czapka studencka? A co to?	""	2018-12-05	""
244	Mikołajkowy Ostry Dyżur	""	2018-12-05	""
245	Wigilia Czapkowa	""	2018-12-15	""
246	Przedsesyjny Ostry Dyżur	""	2019-01-17	""
247	Starej czapkowej gwardii spotkanie na szczycie #2	""	2019-02-16	""
248	Posesyjny Ostry Dyżur - śpiewogranie	""	2019-02-27	""
249	Karczma Wiosenna BCS UJ	""	2019-03-15	""
250	Teatr z Czapką - Dzienniki Gwiazdowe	""	2019-03-20	""
251	Kudłacze 2019	""	2019-03-29	""
252	Bankiet 10-lecia BCS UJ	""	2019-04-06	""
270	Bal(folk) Czapkowy Taneczny Ostry Dyżur	""	2020-02-21	""
253	Juwenalia 2019	""	2019-05-23	""
255	Karczma Juwenaliowa 2019	""	2019-05-24	""
256	Spotkanie z Animusem	""	2019-06-07	""
257	Teatr z Czapką vol. 2 - Skąpiec	""	2019-06-07	""
258	Ognisko Posesyjne BCS UJ	""	2019-06-08	""
259	Adapciak 2019 BCS UJ	""	2019-09-16	""
260	Martinus się broni	""	2019-09-24	""
271	Depositio Beanorum	""	2020-02-28	""
261	Reaktywacja XI	""	2019-09-27	""
263	Wybory 2019/2020	""	2019-10-09	""
264	Wielka Rekrutacja BCS UJ	""	2019-10-24	""
265	Wykład Czapka Studencka	""	2019-11-22	""
266	Karczma	""	2019-11-22	""
267	Ostry Dyżur Mikołajkowy	""	2019-12-04	""
268	Wigilia Czapkowa 2019	""	2019-12-14	""
274	Ognisko Posesyjne 2020	""	2020-06-30	""
275	Nadzwyczajne Walne Zgromadzenie BCS UJ (MS TEAMS)	""	2020-10-08	""
272	Wirtualny Ostry Dyżur (Discord)	""	2020-05-15	""
276	Czapkowe Among Us	""	2020-10-24	""
277	Czapkowy Wieczór Filmowy: Asterix i Obelix (on-line)	""	2020-11-05	""
278	Czapkowy Wieczór Filmowy: Hydrozagadka (on-line)	""	2020-12-09	""
279	Czapkowy Świąteczny Wieczór Filmowy: Kevin sam w domu (on-line)	""	2020-12-28	""
281	Posesyjny Ostry Dyżur: film (on-line)	""	2021-02-12	""
282	Wielki konkurs czapkowy na zdjęcia, filmy, prace plastyczne/literackie…	""	2021-02-27	""
273	Hommage a Maurice	""	2020-06-06	""
235	Walne Zgromadzenie	Nadanie dewizy "In varietate unitas", przyjęcie statutu zgodnego z UJ, przyjęcie nowego herbu Bractwa (autor: Robert Fidura)	2018-09-08	""
284	Czapkowy Wieczór Filmowy: Znachor (on-line)	""	2021-04-22	""
285	Top secret Ostry dyżur	""	2021-06-02	""
283	Posesyjny Ostry Dyżur: film (on-line)	""	2021-02-12	""
287	Jednoosobowa delegacja BCS UJ na Komerszu z okazji XI rocznicy reaktywacji Konwentu Arcadia	""	2021-06-18	""
288	Top secret ognisko	""	2021-06-30	""
289	Reaktywacja XIII	""	2021-09-30	""
291	Karczma Reaktywacyjna	""	2021-09-30	""
292	Walne zgromadzenie BCS UJ	""	2021-10-22	""
293	Karczma Jesienna BCS UJ	""	2021-11-10	""
294	Sprzątanie grobów z prof. Gajdą	""	2021-11-06	""
295	Monika Kwater i Mateusz Żurek biegną w górskim Biegu Niepodległości ze skawiny do Mogilan	""	2021-11-11	""
297	Ułańskie Zdrowie	""	2021-11-13	""
298	Spotkanie z prof. Gajdą po Ułańskim Zdrowiu	""	2021-11-13	""
300	Czapka uruchamia kanał na Instagramie	""	2021-11-16	""
301	Zapytaj, Zamów, Zakładaj	""	2021-11-22	""
302	Impreza Andrzejkowa (+wróżby)	""	2021-11-26	""
303	Ostry Dyżur Mikołajkowy	""	2021-12-09	""
304	Wyjście do kina na "Nasze Magiczne Encanto"	""	2021-12-16	""
305	Karczma Wigilijna	""	2021-12-16	""
306	Noworoczny Ostry Dyżur	""	2022-01-13	""
307	Przedsesyjny Ostry Dyżur	""	2022-01-22	""
335	Przedsesyjny Ostry Dyżur	""	2023-01-26	""
308	Zapytaj, Zamów, Zakładaj" dofinansowane przez Samorząd Studentów UJ	""	2022-02-03	""
309	Zapytaj, Zamów, Zakładaj" dofinansowane przez Samorząd Studentów UJ	""	2022-02-03	""
310	Śródsesyjny Ostry Dyżur	""	2022-02-11	""
311	Ogłoszenie wyników 1. edycji konkursu na nowe zwrotki Czapkowych Opowieści	11 głosami wygrała ją Olga Zatońska. Stworzyła ku chwale Bractwa następujące zwrotki:\r\n1. Rok za rokiem mija szybko\r\nJuż jest lato już jest zima\r\nPorzucone dzieci płaczą\r\nA Pryka wciąż nima!\r\n2. Przy gitarze Kotlet smutno\r\nśpiewać kolędy próbuje\r\nnikt nie słucha, każdy z Ciepłym\r\nTannenbaum fałszuje\r\n3. O noszenie szala mistrza\r\npojedynek się odbywał\r\nGomułka już nie mógł piwa\r\nna głowę je wylał!	2022-02-12	""
312	Wyjście do teatru na spektakl “Dwaj mistrzowie komedii” wg Fredro i Moliera, w którym grał "Koziołek"	""	2022-03-03	""
313	Mateusz Żurek (Magister Cantandi) przedłuża konkurs na czapkowe zwrotki Czapkowych Opowieści i Czapkowej Siekiery Motyki	""	2022-03-09	""
314	Magister Cantandi przedłuża konkurs na czapkowe zwrotki Czapkowych Opowieści i Czapkowej Siekiery Motyki	""	2022-03-09	""
315	Zielony Ostry Dyżur (św. Patryka zamiast Id Marcowych)	""	2022-03-26	""
316	Wirtualny Dzień Otwarty UJ	Czapka ma swój wirtualny pokój, w którym nadaje Wielki Mistrz wraz z częścią Zarządu ze Starego Portu	2022-03-26	""
317	Kudłacze 2022	""	2022-04-01	""
318	Karczma Wiosenna BCS UJ w klimacie wielkanocnego śniadania	""	2022-04-22	""
319	Trzyosobowa delegacja na imprezę do Zielonej Góry	""	2022-04-23	""
320	Juwenalia 2022	""	2022-05-19	""
321	Konferencja Gaudeamus Igitur! Kultura studencka na przestrzeni wieków	""	2022-06-06	""
322	Depositio beanorum	""	2022-06-11	""
323	Adapciak BCS UJ 2022	""	2022-09-22	""
336	Międzysesyjny Ostry Dyżur	""	2023-02-10	""
325	Reaktywacja 2022	""	2022-09-29	""
326	Walne Zgromadzenie BCS UJ	""	2022-10-21	""
324	Karczma Reaktywacyjna	""	2022-09-30	""
328	Chemiku, załóż czapkę! Promocja na Wydziale Chemii UJ	""	2022-11-14	""
329	Karczma Jesienna	""	2022-11-17	""
331	Wigilia BCS UJ	""	2022-12-17	""
330	Andrzejki BCS UJ	""	2022-12-01	""
333	Mikołajkowy Ostry Dyżur	""	2022-12-07	""
334	Noworoczny Ostry Dyżur	""	2023-01-12	""
337	Posesyjny Ostry Dyżur	""	2023-02-24	""
339	Przedwiosenny Ostry Dyżur	""	2023-03-09	""
338	Karczma Idy Marcowe	""	2023-03-17	""
341	Wiosenny Ostry Dyżur	""	2023-03-30	""
342	Ostry Dyżur Wielkanocny	""	2023-04-13	""
343	Juwenalia 2023	""	2023-05-18	""
345	Karczma Juwenaliowa	""	2023-05-21	""
346	Czerwcowy Ostry Dyżur	""	2023-06-02	""
348	Przedsesyjny Ostry Dyżur	""	2023-06-16	""
349	Ognisko Posesyjne	""	2023-06-30	""
350	Reaktywacja 2023	""	2023-09-28	""
352	Karczma Reaktywacyjna	""	2023-09-29	""
353	Awaryjne Depositio Beanorum	""	2023-10-12	""
354	Walne Zgromadzenie BCS UJ	""	2023-10-19	""
355	Halloweenowy Ostry Dyżur	""	2023-10-26	""
356	Czapka w kinie (Chłopi)	""	2023-11-12	""
357	Karczma Jesienna	""	2023-11-15	""
358	Czapka w kinie (Napoleon)	""	2023-11-26	""
359	Andrzejkowy Ostry Dyżur	""	2023-11-30	""
360	Czapka w kinie (Igrzyska Śmierci: Ballada Ptaków i Węży)	""	2023-12-03	""
361	Mikołajkowy Ostry Dyżur	""	2023-12-06	""
362	Karczma Wigilijna BCS UJ	""	2023-12-15	""
363	Cantus Juwenaliowy	""	2013-05-10	""
364	International Cantus	""	2011-10-02	""
365	Traditonal Cantus	""	2014-10-03	""
366	Cantus	""	2016-09-30	""
367	Reactivation Cantus	""	2017-09-29	""
368	Cantus: X Reactivation	""	2018-09-28	""
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