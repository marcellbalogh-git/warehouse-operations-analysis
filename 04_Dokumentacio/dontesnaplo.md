# Döntésnapló, adatminőségi napló és kontrollszámok

A munka közben vezetett napló kivonata. A notebook és a prezentáció a **D-xx** (döntés) és az **A-xx** (adatminőségi megállapítás) azonosítókkal hivatkozik ide. A „feladatkiíró” a próbafeladat kiírója; a kérdéseimre 2026.09.29-én válaszolt.

Rövidítések: CS1, CS2 = Csoport 1, Csoport 2; F0 = a munka első fázisa (Power BI-beállítások és tesztbetöltés).

**Tartalom:** [Döntések](#döntések) · [Adatminőségi megállapítások](#adatminőségi-megállapítások) · [Kontrollszámok](#kontrollszámok)

## Döntések

### D-01 – Hogyan töltöd be a 242 MB-os Excelt?

- **Lehetőségek:** a) Excel közvetlenül a Power BI-ba · b) egyszeri konvertálás CSV/Parquet fájlokká Pythonnal, a Power BI ezeket olvassa
- **Döntés és indoklás:** b) Python-szkript (`D01_excel_to_csv.py`), amely a nyolc munkalapot négy CSV-fájlba írja. A lapok egyszer fűződnek össze, a betöltés gyors és újrafuttatható, a szkript pedig kontrollszámokkal ellenőrzi magát (mind egyezett). A tisztítás eredetileg Power Queryben készült volna; a D-24 után a notebook végzi.

### D-02 – Egy vagy két ténytábla legyen a mozgásokra?

- **Lehetőségek:** a) egy FactMozgas a „statusz” oszloppal · b) külön FactBetarolas és FactSzedes
- **Döntés és indoklás:** a) Egy FactMozgas tábla; a betárolást és a szedést a „statusz” oszlop választja szét (BETAROLAS / SZEDES). A notebookban szűréssel, a Power BI-ban CALCULATE-tel, így az ABC–XYZ (csak szedés) és a KPI betárolási és szedési része is külön számolható. (Döntés: 2026.09.29.)

### D-03 – Melyik dátum kösse a mozgást a naptárhoz?

- **Lehetőségek:** a) lezárva · b) elkezdve
- **Döntés és indoklás:** a) A lezárva dátuma köti a mozgást a naptárhoz: ez a teljesítés pillanata, és a havi összehasonlítás (D-12) is erre épül. Csak 8 sornál esik a két dátum más hónapra. Összhangban van a D-05-tel. (Döntés: 2026.09.29.)

### D-04 – Mi legyen a teljesen azonos sorokkal?

- **Lehetőségek:** a) törlés · b) bent hagyás
- **Döntés és indoklás:** a) Törlés: minden azonos sorból egy példány marad; az összehasonlításban a forras_lap oszlop nem szerepel. Törölt sorok: 56 109 (betárolás 8 695, szedés 47 414). Indoklás: a sorok minden mezőben egyeznek, a kezdés és a lezárás másodpercre azonos, és nincs olyan azonosító (pl. rendelésszám), amely külön eseményként megkülönböztetné őket. A feladatkiíró szerint mindkét megoldás elfogadható. Hatás a két csoportra: a betárolási sorok kb. 1%-a, a szedési sorok kb. 2%-a; a KPI-t csoportonként néhány tíz forinttal változtatja (előzetes becslés). Az exportátfedést az adat nem igazolja (lásd A-05); a duplikáció oka az adatból nem állapítható meg. (Döntés: 2026.09.29.)

### D-05 – 9 szedési sor lezárási dátuma 0000-00-00.

- **Lehetőségek:** a) kizárás (nem lezárt tétel) · b) a dátum legyen az „elkezdve”
- **Döntés és indoklás:** a) A 9 lezáratlan sort (lezarva = 0000-00-00, 9998-as kód) kizárom: a lezáratlan tétel nem teljesítés. A 9998-as kód nincs a Létszámban, és más sora sincs, így a KPI-t és a teljesítménypontot nem érinti. (Döntés: 2026.09.29.)

### D-06 – Mi legyen a 0 darabos szedési sorokkal (kb. 45 ezer)?

- **Lehetőségek:** a) bent hagyás · b) kizárás
- **Döntés és indoklás:** A 0 darabos szedési sorok a darabalapú mutatókban maradnak (nem torzítanak), a tételsor-alapú ABC-ből kizárom őket. A feladatkiíró megerősítette (2026.09.29.). Kiegészítés (2026.10.04.): a teljesítménypontban a 0 darabos szedési sorok pontjai bent maradnak (A-07 a)): a rendszer ezekre a sorokra is adott pontot, a feladat a megszerzett pontokat kérdezi. A két csoportban 8 296 sor, 12 401 pont (1,5%); a kizárásuk hatását a notebook 5.3-as cellája kiírja (egy főre 31 414,7 → 30 893,3, illetve 31 741,3 → 31 331,7).

### D-07 – Mi legyen az „1”-es ügyintézővel (kb. 223 ezer sor, 0 mp)?

- **Lehetőségek:** a) „Rendszer” dolgozóként jelölés · b) kizárás
- **Döntés és indoklás:** a) „Rendszer” dolgozóként jelölöm: az ABC–XYZ-ben benne marad (valós kereslet), a dolgozói kimutatásokban nem szerepel. A feladatkiíró megerősítette (2026.09.29.).

### D-08 – Mi legyen a Létszám táblán kívüli ügyintézőkkel (532 kód + az „1”)?

- **Lehetőségek:** a) „Csoporton kívüli” kategória · b) kizárás
- **Döntés és indoklás:** a) „Csoporton kívüli” kategória. A KPI és a teljesítménypont csak a két csoportra készül, az ABC–XYZ a teljes forgalomra, de csak a szedésre. A feladatkiíró megerősítette (2026.09.29.).

### D-09 – A csoportlétszámot kódok vagy személyek alapján számolod?

- **Lehetőségek:** a) kódok: CS1 = 12, CS2 = 15 · b) nevek: CS1 = 11, CS2 = 15
- **Döntés és indoklás:** a) Kódok alapján: CS1 = 12, CS2 = 15 fő. Minden ügyintézőkódot külön személynek tekintek, így a két Németh Dórát (563, 7834) és a két Farkas Bélát (9783, 6156) is azonos nevű, de különböző munkatársnak veszem. Az adatokból ez nem dönthető el (egy kód saját tételei is 88–96%-ban átfedik egymást időben, ezért az egyidejű munka nem bizonyíték), a névismétlődés viszont 27 főnél, gyakori nevekkel várható. A döntés a KPI-t egyik értelmezésben sem változtatja meg: CS1 legfeljebb 12 fő, CS2 mindkét esetben 15 fő. A vizuálokon a dolgozók „Név (kód)” formában szerepelnek, különben a Power BI az azonos neveket egy sávba vonná össze. A feladatkiírónak küldött kérdésekben feltevésként jeleztem, és megerősítették.

### D-10 – Mi legyen a létszámkorrekció képlete?

- **Lehetőségek:** a) 30 000 × 12 / létszám · b) más levonási logika
- **Döntés és indoklás:** a) 30 000 × 12 / létszám, ha a létszám 12 fölött van: CS1 = 30 000 Ft, CS2 = 24 000 Ft. A feladatkiíró megerősítette (2026.09.29.).

### D-11 – Mihez hasonlítod az utolsó hónapot?

- **Lehetőségek:** a) június vs. április–június átlaga · b) június vs. április–május átlaga
- **Döntés és indoklás:** a) A júniust az április, május és június havi összegeinek átlagához mérem. A feladatkiíró megerősítette (2026.09.29.).

### D-12 – A június csak 23 napos (06.23-ig tart). Hogyan veted össze?

- **Lehetőségek:** a) nyers havi összeggel · b) napi átlaggal (aktív napra vagy munkanapra vetítve)
- **Döntés és indoklás:** a) Nyers havi összeggel, a feladatkiíró kérésére (2026.09.29.): a részleges júniust kell a háromhavi átlaghoz mérni. Az általam javasolt napi átlag (b) érzékenységi számításként szerepel (notebook 6.4): napi átlaggal mind a négy arány 1 fölött van (CS1 betárolás 1,174, szedés 1,105; CS2 betárolás 1,119, szedés 1,039), így mindkét csoport a teljes alapot kapná.

### D-13 – Hogyan arányosítasz, ha az utolsó hónap elmarad?

- **Lehetőségek:** komponens × (utolsó / átlag), 0 és 1 közé korlátozva
- **Döntés és indoklás:** Komponens × (június / háromhavi átlag), felülről 1-nél korlátozva. A feladatkiíró megerősítette, hogy az átlag feletti teljesítésért nem jár plusz összeg (2026.09.29.).

### D-14 – Mi alapján számolod a készlet KPI-részt?

- **Lehetőségek:** a) a teljes 1/3 jár, mert nincs teljesítményfeltétel · b) minőségi szorzó (pl. a nem tiltott, nem 0 darabos sorok aránya)
- **Döntés és indoklás:** a) A készletrész mindkét csoportnak teljes értékben jár (1/3). A feladatkiíró megerősítette (2026.09.29.); a tárhelyadat a legfrissebb állapot pillanatképe. A TILTOTT sorokról külön döntök (D-23).

### D-15 – Mi legyen az ABC alapja és a határai?

- **Lehetőségek:** a) szedési tételsorok száma (gyakoriság) · b) szedett darab
- **Döntés és indoklás:** a) A szedési tételsorok száma alapján, cikkszámonként, csak a szedésre, a 0 darabos sorok nélkül, az „1”-es kóddal. A feladatkiíró megerősítette (2026.09.29.). Határok (2026.10.03.): 80 / 15 / 5% kumulált tételsorarány; az azonos tételsorszámú cikkszámok azonos osztályba kerülnek (a határ a 80%-ot, illetve a 95%-ot átlépő cikkszám tételsorszáma): A ≥ 6, B 2–5, C 1 tételsor. Sorrend szerinti vágásnál a 6 tételsoros 10 890 cikkszámból 9 767 A, 1 123 B lenne, csak az ábécérend miatt.

### D-16 – Milyen időegységgel és határokkal számolod az XYZ-t?

- **Lehetőségek:** heti / havi / napi bontás; CV-határok
- **Döntés és indoklás:** Heti tételsorok száma a 11 teljes ISO-héten (15–25.); a részleges 14. (04.01–04.05.) és 26. (06.22–06.23.) hét kimarad (velük az X 3 970-ről 2 071-re csökkenne). Teljes cikkszám × hét rács a nulla hetekkel (nélkülük 233 378 cikkszám lenne X). CV = szórás / átlag, populációs szórás (ddof=0). X: CV ≤ 0,5; Y: 0,5 < CV ≤ 1,0; Z: CV > 1,0. A csak részleges héten szedett 7 043 cikkszám (CV = 0/0) Z. A B és a C szükségszerűen Z. (2026.10.03.)

### D-17 – Hol számolod az ABC–XYZ-t?

- **Lehetőségek:** a) Power Query vagy számított oszlop (statikus) · b) DAX mérőszám (dinamikus)
- **Döntés és indoklás:** a) Statikus oszlopok a DimCikk-ben (Tetelsor, ABC, CV, XYZ, ABC_XYZ), a notebook számolja. A nem szedett 180 412 cikkszám „Nincs szedés” kategóriát kap, Tetelsor = 0, CV üres. (2026.10.03.)

### D-18 – Mit jelent a „létszámalapú” teljesítménypont?

- **Lehetőségek:** a) egyéni pontok · b) csoportpont / fő
- **Döntés és indoklás:** Mindkettő: dolgozónkénti pontszám („Név (kód)” formában) és csoportonként az egy főre jutó pont. A feladatkiíró mindkettőt elfogadta (2026.09.29.).

### D-19 – Mi legyen a kiugró értékekkel (darab max. 9 760; 1 napnál hosszabb szedések)?

- **Lehetőségek:** bent hagyás / jelölés / kizárás
- **Döntés és indoklás:** Bent hagyás, jelölőoszlop nélkül. Az ABC–XYZ tételsor-alapú, ezért nem érinti. A két csoportban 5 ilyen sor van (mind CS2 szedés, áprilisban és májusban, összesen 9 944 db); a kizárásuk a CS2 szedési arányát 0,866-ről 0,894-re, a KPI-t 22 622,82-ről 22 846,08 Ft-ra változtatná (+223,26 Ft; notebook 6.4, érzékenység). Az időtartamot egyik mutató sem használja. (2026.10.03.)

### D-20 – Hogyan hivatkozik a Power BI a CSV-fájlokra?

- **Lehetőségek:** a) beégetett teljes útvonal mind a négy lekérdezésben · b) egy StagingMappa paraméter, amelyhez a lekérdezések a fájlnevet fűzik
- **Döntés és indoklás:** b) StagingMappa paraméter (Text, záró `\`-rel), a Source lépésekben `File.Contents(StagingMappa & "letszam.csv")`. A projektmappa feljebb költöztetésekor derült ki, miért éri meg: a beégetett útvonalak mind a négy lekérdezésben egyszerre törtek el. Később KimenetMappa lett belőle (D-27).

### D-21 – Automatikus típusfelismerés és modellbeállítások betöltéskor?

- **Lehetőségek:** a) alapértelmezés: típusfelismerés az első 200 sor alapján, automatikus kapcsolatok, Auto date/time · b) mind kikapcsolva, a típusok és a kapcsolatok kézzel
- **Döntés és indoklás:** b) Current File → Data Load: típusfelismerés, a három kapcsolat-beállítás, Auto date/time és a háttér-előnézet KI; Global: Auto date/time for new files KI. Betöltéskor „Do not detect data types”, a Promoted Headers után megjelenő Changed Type lépést törlöm. A típusokat kézzel állítom be, a dátumokat Using Locale (English, US) konverzióval.

### D-22 – Hogyan épüljön fel a Power Query?

- **Lehetőségek:** a) fájlonként egy lekérdezés, benne minden tisztító és modellező lépés · b) staging réteg (stg_ lekérdezések: forrás + típusok), erre Reference-szel épülnek a modelltáblák; a staging betöltése KI
- **Döntés és indoklás:** b) Négy stg_ lekérdezés (stg_Letszam, stg_Betarolas, stg_Szedes, stg_Tarhely) egy Staging csoportban, a StagingMappa paraméterrel. **Okafogyott:** a D-24 után a tisztítás és a modellezés a notebookba került, a stg_ lekérdezéseket töröltem (D-27).

### D-23 – Mi legyen a TILTOTT jelölésű tárhelysorokkal (401 729 sor, 48%)?

- **Lehetőségek:** a) kizárás a készletből · b) bent hagyás, külön kategóriaként (szabad / tiltott)
- **Döntés és indoklás:** b) A TILTOTT sorok külön kategóriaként (szabad / tiltott) maradnak a készletben. A súlyuk nagy: a sorok 48%-a és a készletdarab 39%-a (2 123 994 / 5 401 239 db), ezért sem kivágni, sem jelölés nélkül összemosni nem érdemes; a vizuálon szűrővel kivehetők. A KPI-t nem érinti, mert a készletrész teljes 1/3 (D-14). (Döntés: 2026.09.29.)

### D-24 – Hol készüljenek a számítások (tisztítás, adatmodell, ABC–XYZ, teljesítménypont, KPI)?

- **Lehetőségek:** a) Python notebookban; a Power BI a kész táblákat tölti be, a pontok és a KPI DAX-ban is (kontroll) · b) Power Queryben és DAX-ban; a notebook ugyanezt külön megismétli
- **Döntés és indoklás:** a) A notebook végzi a tisztítást, az adatmodellt, az ABC–XYZ-t, a teljesítménypontot és a KPI-t; a Power BI a notebook kimeneti tábláit tölti be, a pontok és a KPI DAX-ban is elkészülnek kontrollként. A feladatkiíró Python-notebookot kért, amely az adatmodellezéstől a KPI-ig bemutatja a számítást, így minden számítás egyszer készül el, és a notebook meg a riport ugyanazt mutatja. (Döntés: 2026.09.29.) Módosítás (2026.10.06., időhiány miatt): előbb a vizuálok készültek el, utána a DAX-kontroll. A DAX-kontroll végül teljes terjedelemben elkészült: minden eltérés 0,00.

### D-25 – Honnan töltsön be a notebook: a 02_Staging CSV-kből vagy közvetlenül a forrás-Excelből?

- **Lehetőségek:** a) a CSV-kből; a D01_excel_to_csv.py szkriptet is leadom, és a notebook bevezetője leírja a futtatás sorrendjét · b) közvetlenül az Excelből (önálló, de lassabb betöltés)
- **Döntés és indoklás:** a) A notebook a 02_Staging CSV-kből tölt be. A leadott csomagba a D01 szkript is bekerül; a notebook bevezetője leírja a sorrendet: forrás-Excel a 01_Forras mappába → D01 szkript → notebook. (Döntés: 2026.09.29.)

### D-26 – Milyen formátumban adja át a notebook a táblákat a Power BI-nak?

- **Lehetőségek:** a) Parquet (új függőség: pyarrow) · b) CSV (nincs új függőség)
- **Döntés és indoklás:** a) Parquet, a 06_Kimenet mappába, táblánként egy fájl; az export visszaolvasással ellenőrzi az értékeket és a típusokat. A pyarrow 25.0.1 telepítve, a Környezet cella kiírja a verzióját; Restart + Run All után minden kontroll egyezik. A Power BI-ban csak a két Datum oszlopot (FactMozgas, DimDatum) kell Date típusra állítani, mert a notebookban dátum/idő, 00:00 időponttal. (Döntés: 2026.10.01.)

### D-27 – Mi legyen a Power BI F0-s stg_ lekérdezéseivel (CSV-forrás, StagingMappa) a D-24 a) után?

- **Lehetőségek:** a) törlés; a pbix egyetlen forrása a 06_Kimenet (KimenetMappa paraméter) · b) megtartás betöltés nélkül (Enable load KI) a Staging csoportban
- **Döntés és indoklás:** a) A négy stg_ lekérdezés törölve, a StagingMappa paraméter átnevezve KimenetMappa-ra (…\06_Kimenet\, záró `\`-rel); 10 Parquet-lekérdezés (Parquet.Document), csoportok: Parameters, Modell, Eredmény. A D-22 (staging réteg a Power Queryben) okafogyott: a szerepét a notebook vette át. Az F0-s állapotról biztonsági másolat készült. A 11 tábla sorainak száma = a notebook. (Döntés: 2026.10.06.)

### D-28 – Hogyan kapcsolódjanak a notebook eredménytáblái (PontDolgozo, PontCsoport, PontHavi, KPI, KPIHavi) a modellhez?

- **Lehetőségek:** a) DimCsoport (4 sor, a DimDolgozo Csoport oszlopából, Distinct) mint közös „1” oldal; a PontDolgozo az ugyintezo szerint a DimDolgozo-hoz · b) kapcsolat nélkül, önálló táblákként
- **Döntés és indoklás:** a) DimCsoport → DimDolgozo → FactMozgas / PontDolgozo; DimCsoport → PontCsoport, PontHavi, KPI, KPIHavi. Mind a 10 kapcsolat Many to one, Single, aktív; a PontDolgozo, PontCsoport és KPI esetén a Power BI 1:1-et (kétirányú szűrés) ajánlott, ezt kézzel *:1-re állítottam, hogy a szűrés csak a dimenzióból induljon. A PontDolgozo csak a DimDolgozo-hoz kapcsolódik, hogy egy szűrési út legyen. (Döntés: 2026.10.06.) Módosítás (2026.10.30.): a DimCsoport eredetileg a DimDolgozo lekérdezés Reference-éből készült; ez a repóba költöztetéskor, betöltéskor „A cyclic reference was encountered during evaluation” hibát adott, ezért a DimCsoport most közvetlenül a `DimDolgozo.parquet` fájlt olvassa (az eredmény ugyanaz a 4 sor).

## Adatminőségi megállapítások

A mennyiségek a nyers adatra vonatkoznak, ha a sor másként nem jelzi.

| ID | Tábla | Megállapítás | Mennyiség | Kapcsolódik |
|---|---|---|---|---|
| A-01 | Összes | Az Excel 8 munkalapon kb. 3,85 millió sort tartalmaz. A betárolás 2, a szedés 3, a tárhely 2 lapra van szétosztva (laponként max. 800 ezer sor), ezért össze kell fűzni őket. | Betárolás: 825 337; Szedés: 2 188 553; Tárhely: 834 925; Létszám: 27 | D-01, D-02 |
| A-02 | Létszám | CS1-ben 12, CS2-ben 15 kód van. Németh Dóra kétszer szerepel a CS1-ben (563, 7834), Farkas Béla mindkét csoportban (CS1: 9783, CS2: 6156). A kódok egyediek, a nevek nem. | 27 sor, 25 egyedi név | D-09 |
| A-03 | Mozgás | 533 ügyintéző kód nem szerepel a Létszám táblában (az „1”-essel együtt). A 27 ismert kód mind aktív. | a betárolási sorok 82%-a, a szedési sorok 81%-a | D-08 |
| A-04 | Szedés | Az „1”-es ügyintéző soraiban az elkezdve és a lezárva mindig azonos (0 mp), ez rendszer- vagy automatikus könyvelésre utal. | 225 515 sor (duplikátumszűrés után 223 306) | D-07 |
| A-05 | Mozgás | Teljesen azonos sorok (a forras_lap oszlop nélkül összehasonlítva). 23 243 duplikált rekord példányai több munkalapon vannak (ebből 1 933 mindhárom szedési lapon), nem szomszédos lapokon is (pl. Szedés 1 és 3: 6 056 rekord), tehát nem a lapokra bontás határán keletkeztek. Egy rekordnak legfeljebb 36 példánya van (pontosítva: 2026.09.29.). | 56 109 felesleges sor (betárolás: 8 695; szedés: 47 414) | D-04 |
| A-06 | Szedés | A lezarva értéke „0000-00-00 00:00:00”, és mind a 9998-as ügyintézőhöz tartozik (akinek más sora nincs). Dátum/idő típusnál hibát ad. | 9 sor | D-05 |
| A-07 | Szedés | darab = 0, a sorok mégis kaptak teljesítménypontot. | 46 364 sor (duplikátumszűrés után 45 408) | D-06 |
| A-08 | Mozgás | Az időszak 2026.04.01. 00:17 – 2026.06.23. 21:36, tehát a június csak 23 napos. 05.01-én (ünnepnap) nincs adat, betárolás 04.05-én és 05.24-én (vasárnap) sem. | 3 hónap, ebből 1 részleges | D-11, D-12 |
| A-09 | Betárolás | Az időtartam (lezarva − elkezdve) minden sorban pontosan 60 mp, így betárolásnál nem informatív. | 825 337 sor | – |
| A-10 | Szedés | Az időtartam mediánja kb. 9,6 perc, de vannak extrém hosszúak. | 1 905 sor > 4 óra; 45 sor > 1 nap | D-19 |
| A-11 | Mozgás | Darab-kiugrók: max. 9 760 (szedés) és 7 694 (betárolás), miközben a 99. percentilis csak 10, illetve 36 db. | 19 szedési és 54 betárolási sor > 1 000 db | D-19 |
| A-12 | Cikk | A cikkszám-törzsadat konzisztens: minden cikkszámhoz forrástól függetlenül pontosan egy termékcsoport és egy gyártókód tartozik. Nincs szóköz- vagy formátumhiba („code” + szám). | 450 149 egyedi cikkszám (mozgás: 295 990; tárhely: 407 722) | DimCikk |
| A-13 | Cikk | A gyártókód vagy betű + 2 számjegy (pl. O31, K46), vagy 3 számjegy (pl. 020, 753). A vezető nullás kódokat az automatikus típusfelismerés számmá alakítja (020 → 20). Az „O” betűs kódok valódi betűk, nem hibák. | 806 gyártókód (összes forrás), ebből 55 vezető nullás; a szedésben 687, ebből 50 | Szöveg típus |
| A-14 | Cikk | A „Külső tükör burkolat nélkül” termékcsoportnév két kóddal szerepel (760, 826). | 1 157 kód, 1 156 név | A kód legyen a kulcs |
| A-15 | Tárhely | 33 raktár (50–82). Tárhelytípusok: P, *, D, w, K, F, E, ?, üres. A típus és a méret hiányzik a 63–65., 68–75., 77–80. és 82-es raktárnál. | 125 654 sor típus és méret nélkül | D-14 |
| A-16 | Tárhely | A sorok 48%-a „TILTOTT”, raktáranként 0 és 100% között. Vannak 0 darabos sorok is. | 401 729 tiltott sor; 3 978 sor 0 darabos | D-14 |
| A-17 | Tárhely | A tábla pillanatkép: nincs benne dátum és ügyintéző. Így sem az időbeli alakulás nem mutatható, sem csoporthoz nem rendelhető. | – | D-14 |
| A-18 | Tárhely | Egy tárhelyen több cikkszám is lehet (58 ezer tárhelyen 6 vagy több). A Tárhely + Cikkszám pár egyedi, duplikátum nincs. | 165 328 tárhely | – |
| A-19 | Cikk | 41 886 szedett cikkszám jelenleg nincs tárhelyen, és 179 330 tárhelyen lévő cikkszámot nem szedtek a 3 hónap alatt. Ezért a DimCikk-et az összes forrásból kell felépíteni. | – | DimCikk |
| A-20 | Szedés | Az elkezdve és a lezarva a szedési lapokon szövegként van tárolva (ÉÉÉÉ-HH-NN óó:pp:mm), a betárolási lapokon viszont valódi Excel-dátumként. A D-01 szkript a CSV-ben mindkettőt egységes ISO szöveggé alakítja. A notebook dátum/idő típusra alakítja (2.3), az A-06-os sorok kezelése után. | 2 188 553 sor (mindhárom szedési lap) | D-01, D-05, D-21 |

## Kontrollszámok

A notebook (2.7, 4.7, 4.8, 5.3, 6.3) és a Power BI-riport (DAX-kontroll) ugyanezekre a számokra fut ki.

| Mérőszám | Nyers adat | Tisztítás után (D-04 + D-05) | Power BI-ban | Egyezik? |
|---|---|---|---|---|
| Betárolási tételsorok | 825 337 | 816 642 | 816 642 + 2 141 130 = 2 957 772 (FactMozgas sorai) | igen (összesen) |
| Betárolt darab | 3 220 889 | 3 175 566 |  |  |
| Betárolási teljesítménypont | 1 238 171 | 1 225 119 | 1 225 119 + 3 211 882 = 4 437 001 ([Pont] mérték) | igen (összesen) |
| Szedési tételsorok | 2 188 553 | 2 141 130 | ld. fent: a FactMozgas 2 957 772 sora | igen (összesen) |
| Szedett darab | 3 291 405 | 3 210 184 |  |  |
| Szedési teljesítménypont | 3 283 147 | 3 211 882 | ld. fent: [Pont] összesen 4 437 001 | igen (összesen) |
| Egyedi ügyintéző kódok (mozgás) | 560 | 559 (a 9998-as kód kiesik) | 559 (DimDolgozo sorai) | igen |
| Egyedi cikkszámok (összes forrás) | 450 149 | 450 149 | 450 149 (DimCikk sorai) | igen |
| Tárhelysorok / készletdarab | 834 925 / 5 401 239 | 834 925 / 5 401 239 | 834 925 / 5 401 239 (FactKeszlet; Készlet oldal) | igen |
| Teljesítménypont, Csoport 1 / Csoport 2 (notebook 5.2–5.3) | – | 376 976 / 476 120 (egy főre 31 414,7 / 31 741,3) | 376 976 / 476 120 ([Pont] DAX és PontCsoport); pont/fő 31 414,67 / 31 741,33 ([Pont per fő]) | igen |
| KPI, Csoport 1 / Csoport 2 (notebook 6.3) | – | 29 271,57 / 22 622,82 Ft (alap 30 000 / 24 000; elmaradás 728,43 / 1 377,18) | 29 271,57 / 22 622,82 Ft ([KPI DAX] = KPI tábla; [KPI eltérés] 0,00) | igen |
| ABC–XYZ mátrix, cikkszámok (notebook 4.7) | – | AX 3 970, AY 28 740, AZ 43 499, BZ 108 934, CZ 84 594 (269 737) | ugyanez (ABC-XYZ oldal, mátrix) | igen |
| Készletdarab ABC szerint (notebook 4.8) | – | A 3 862 909, B 663 745, C 263 078, Nincs szedés 611 507 | ugyanez (Készlet oldal) | igen |

**Havi összegek tisztítás után (az összes ügyintéző, a lezárás dátuma szerint):**

| Hónap (tisztítás után) | Betárolt darab | Betárolási napok | Szedett darab | Szedési napok | Szedett db / nap |
|---|---|---|---|---|---|
| 2026. április | 1 114 944 | 29 | 1 129 983 | 30 | 37 666 |
| 2026. május | 1 144 928 | 29 | 1 184 196 | 30 | 39 473 |
| 2026. június (06.23-ig) | 915 694 | 23 | 896 005 | 23 | 38 957 |
