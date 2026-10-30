"""
D-01: raktari_teljesitmeny_export.xlsx -> CSV-fájlok a Python-notebook betöltéséhez

Bemenet: 01_Forras/raktari_teljesitmeny_export.xlsx (8 munkalap, kb. 3,85 millió sor)
Kimenet: 02_Staging mappa: letszam.csv, betarolas.csv, szedes.csv, tarhely.csv

A szkript nem tisztít: minden sort és értéket változatlanul átír.
Egyetlen egységesítés: a dátum/idő értékek ÉÉÉÉ-HH-NN óó:pp:mm formát kapnak.
A tisztítás (duplikátumok, 0000-00-00 dátumok stb.) a notebook 2. szakaszában történik
(05_Notebook/raktari_elemzes.ipynb).

Telepítés: pip install pandas python-calamine   (pandas 2.2 vagy újabb kell)
Futtatás:  python D01_excel_to_csv.py
"""

import time
from pathlib import Path

import pandas as pd

# ---- Beállítások ----------------------------------------------------------

MAPPA = Path(__file__).resolve().parent
FORRAS = MAPPA / "01_Forras" / "raktari_teljesitmeny_export.xlsx"
CEL_MAPPA = MAPPA / "02_Staging"

# Melyik CSV-fájl mely munkalapokból áll össze.
CSV_LAPOK = {
    "letszam.csv": ["Létszám"],
    "betarolas.csv": ["Betárolási teljesítmény 1", "Betárolási teljesítmény 2"],
    "szedes.csv": ["Szedési teljesítmény 1", "Szedési teljesítmény 2",
                   "Szedési teljesítmény 3"],
    "tarhely.csv": ["Tárhelyek tartalma 1", "Tárhelyek tartalma 2"],
}

# Kontrollszámok: a forrás-Excel átvizsgálásakor mért értékek (nyers adat, tisztítás előtt).
KONTROLL = {
    "letszam.csv": {"sor": 27},
    "betarolas.csv": {"sor": 825_337, "darab": 3_220_889, "teljesitmenypont": 1_238_171},
    "szedes.csv": {"sor": 2_188_553, "darab": 3_291_405, "teljesitmenypont": 3_283_147},
    "tarhely.csv": {"sor": 834_925, "Darab": 5_401_239},
}

DATUM_OSZLOPOK = ["elkezdve", "lezarva"]


# ---- Segédfüggvény --------------------------------------------------------

def datum_iso(ertek):
    """Az Excel-dátumot ISO szöveggé alakítja, minden mást változatlanul hagy."""
    if isinstance(ertek, pd.Timestamp):
        return ertek.strftime("%Y-%m-%d %H:%M:%S")
    return ertek


# ---- Fő program -----------------------------------------------------------

def main():
    if not FORRAS.exists():
        raise SystemExit(f"Nem találom a forrásfájlt: {FORRAS}")
    CEL_MAPPA.mkdir(exist_ok=True)
    kezdes = time.time()
    minden_ok = True

    with pd.ExcelFile(FORRAS, engine="calamine") as xls:
        for csv_nev, lapok in CSV_LAPOK.items():
            print(f"\n{csv_nev}")
            szamlalo = dict.fromkeys(KONTROLL[csv_nev], 0)

            with open(CEL_MAPPA / csv_nev, "w", encoding="utf-8-sig", newline="") as f:
                for lap in lapok:
                    df = xls.parse(lap, dtype=object, na_filter=False)

                    if lap == lapok[0]:
                        fejlec = list(df.columns)
                    elif list(df.columns) != fejlec:
                        raise SystemExit(f"Eltérő oszlopok a(z) '{lap}' lapon!")

                    for oszlop in DATUM_OSZLOPOK:
                        if oszlop in df.columns:
                            df[oszlop] = df[oszlop].map(datum_iso)

                    df["forras_lap"] = lap
                    df.to_csv(f, sep=";", index=False, header=(lap == lapok[0]))

                    szamlalo["sor"] += len(df)
                    for oszlop in szamlalo:
                        if oszlop != "sor":
                            szamlalo[oszlop] += pd.to_numeric(df[oszlop], errors="coerce").sum()
                    print(f"  {lap}: {len(df):,} sor ({time.time() - kezdes:.0f} mp)")
                    del df

            for mutato, ertek in szamlalo.items():
                vart = KONTROLL[csv_nev][mutato]
                egyezik = ertek == vart
                minden_ok = minden_ok and egyezik
                print(f"  kontroll, {mutato}: {ertek:,.0f} (várt: {vart:,}) "
                      f"{'OK' if egyezik else 'ELTÉRÉS!'}")

    print(f"\nKész {time.time() - kezdes:.0f} mp alatt. Kimenet: {CEL_MAPPA}")
    if minden_ok:
        print("Minden kontrollszám egyezik.")
    else:
        print("FIGYELEM: van eltérés a kontrollszámokban!")


if __name__ == "__main__":
    main()
