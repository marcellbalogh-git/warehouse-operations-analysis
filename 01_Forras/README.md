# 01_Forras – source data (not included)

The source file `raktari_teljesitmeny_export.xlsx` (242 MB, 8 sheets, about 3.85 million rows) was provided for the recruitment task and is not published in this repository. To rerun the pipeline, place it here and run `D01_excel_to_csv.py` from the repository root.

| Sheet | Rows | Columns |
|---|---|---|
| Létszám (headcount) | 27 | nev, felettes, ugyintezo_kod |
| Betárolási teljesítmény 1–2 (put-away) | 800 000 + 25 337 | Cikkszam, Termekcsoportkodnev, Gyartokod, Termekcsoportkod, darab, ugyintezo, elkezdve, statusz, lezarva, teljesitmenypont |
| Szedési teljesítmény 1–3 (picking) | 800 000 + 800 000 + 588 553 | same as put-away |
| Tárhelyek tartalma 1–2 (storage locations) | 800 000 + 34 925 | Raktár, Tárhely típus, Tárhely, Cikkszam, Termekcsoportkodnev, Gyartokod, Termekcsoportkod, Tól (mm), Hossz (mm), Mélység (mm), Magasság (mm), Darab, Tiltott? |

---

**Magyarul:** a forrásfájl (`raktari_teljesitmeny_export.xlsx`) a próbafeladathoz készült, ezért nem része a repónak. Az újrafuttatáshoz ide kell tenni, majd a repó gyökeréből futtatni a `D01_excel_to_csv.py` szkriptet.
