# DAX-mértékek / DAX measures

A Power BI-riport összes mértéke, a DAX query view „Define all measures in this model” gyorsparancsával kimásolva. A mértékek a notebook eredményeit (teljesítménypont, KPI) függetlenül újraszámolják; a riport Kontroll oldala mutatja, hogy minden eltérés 0,00.

All measures of the Power BI report, exported from DAX query view. They recalculate the notebook's results (performance points, KPI) independently; the report's Kontroll page shows every difference is 0.00.

```dax
DEFINE
    MEASURE '_Mertekek'[Pont] = SUM(FactMozgas[teljesitmenypont]) //teljesítménypontok összege
    MEASURE '_Mertekek'[Cikkszámok száma] = COUNTROWS(DimCikk)
    MEASURE '_Mertekek'[Pont betárolás] = CALCULATE([Pont], FactMozgas[statusz] = "BETAROLAS") //"Pont"-ból csak ami betárolás
    MEASURE '_Mertekek'[Pont szedés] = CALCULATE([Pont], FactMozgas[statusz] = "SZEDES") //"Pont"-ból ami csak szedés
    MEASURE '_Mertekek'[Létszám] = COUNTROWS(DimDolgozo) // Megszámolja a DimDolgozo-nak azokat a sorait, amelyek a cella szűrése után megmaradnak.
    MEASURE '_Mertekek'[Pont per fő] = DIVIDE([Pont], [Létszám])
    MEASURE '_Mertekek'[Darab] = SUM(FactMozgas[darab])
    MEASURE '_Mertekek'[Darab utolsó hónap] = VAR UtolsoHonap = CALCULATE(MAX(DimDatum[Honap]), ALL(DimDatum))
RETURN CALCULATE([Darab], ALL(DimDatum), DimDatum[Honap] = UtolsoHonap)
    MEASURE '_Mertekek'[Darab 3 havi átlag] = CALCULATE(AVERAGEX(VALUES(DimDatum[Honap]), [Darab]), ALL(DimDatum))
    MEASURE '_Mertekek'[Arány] = DIVIDE([Darab utolsó hónap], [Darab 3 havi átlag])
    MEASURE '_Mertekek'[Szorzó] = MIN(1, [Arány])
    MEASURE '_Mertekek'[KPI alap] = 30000 * MIN(1, DIVIDE(12, [Létszám]))
    MEASURE '_Mertekek'[KPI komponens] = DIVIDE([KPI alap], 3)
    MEASURE '_Mertekek'[Készlet rész] = [KPI komponens]
    MEASURE '_Mertekek'[Betárolás rész] = [KPI komponens] * CALCULATE([Szorzó], FactMozgas[statusz] = "BETAROLAS")
    MEASURE '_Mertekek'[Szedés rész] = [KPI komponens] * CALCULATE([Szorzó], FactMozgas[statusz] = "SZEDES")
    MEASURE '_Mertekek'[KPI DAX] = [Készlet rész] + [Betárolás rész] + [Szedés rész]
    MEASURE '_Mertekek'[KPI elmaradás] = [KPI alap] - [KPI DAX]
    MEASURE '_Mertekek'[KPI eltérés] = [KPI DAX] - SUM('KPI'[KPI])

EVALUATE
    SUMMARIZECOLUMNS(
        "Pont", [Pont],
        "Cikkszámok száma", [Cikkszámok száma],
        "Pont betárolás", [Pont betárolás],
        "Pont szedés", [Pont szedés],
        "Létszám", [Létszám],
        "Pont per fő", [Pont per fő],
        "Darab", [Darab],
        "Darab utolsó hónap", [Darab utolsó hónap],
        "Darab 3 havi átlag", [Darab 3 havi átlag],
        "Arány", [Arány],
        "Szorzó", [Szorzó],
        "KPI alap", [KPI alap],
        "KPI komponens", [KPI komponens],
        "Készlet rész", [Készlet rész],
        "Betárolás rész", [Betárolás rész],
        "Szedés rész", [Szedés rész],
        "KPI DAX", [KPI DAX],
        "KPI elmaradás", [KPI elmaradás],
        "KPI eltérés", [KPI eltérés]
    )
```
