# Knesset 25 Legislative Effectiveness Scores

Legislative Effectiveness Scores (LES) for all 148 Members of the 25th Israeli Knesset
(November 2022 - present). All data is sourced directly from the official Knesset API
and scored using the methodology of Volden, Wiseman and Wittmer (2010).

---

Data

| File | Description |
|------|-------------|
| [data/processed/knesset25_les_public.csv](data/processed/knesset25_les_public.csv) | Name, faction, gender, LES and bills passed (for journalists and general use) |
| [data/processed/knesset25_les_full.csv](data/processed/knesset25_les_full.csv) | Full dataset including bill stage breakdown (for researchers) |
| [CODEBOOK.md](CODEBOOK.md) | Field descriptions and LES calculation details |

Google Sheets (view and sort): https://docs.google.com/spreadsheets/d/1b6idjuwsKlYzzv4ge7UpMt9c46YJkzxHtlq6CfKR3OQ/edit?usp=sharing

---

What is LES?

LES measures how effective a member of parliament is at advancing legislation,
not just how many bills they submit but how far those bills progress.

| Stage | Weight |
|-------|--------|
| Bill failed or cancelled | 0 |
| Submitted to the Knesset | 1 |
| Prepared for first reading | 2 |
| First reading passed | 3 |
| Prepared for second and third reading | 4 |
| Passed third reading (enacted into law) | 5 |

---

Repository structure

knesset25-les/
+-- data/
|   +-- processed/
|       +-- knesset25_les_public.csv
|       +-- knesset25_les_full.csv
+-- calculate_les_k25.py
+-- CODEBOOK.md
+-- README.md

---

Updating the data

Knesset 25 is still active. To refresh the scores, run calculate_les_k25.py
after pulling fresh data from the Knesset API.

---

Methodology

Volden, C., Wiseman, A.E., and Wittmer, D.E. (2010). The Legislative Effectiveness
of Women in Congress. Journal of Politics, 72(4), 1-15.

Data source: Official Knesset API (knesset.gov.il/OdataV4/ParliamentInfo)

---

Attribution

All underlying data is sourced from the official Knesset API (public domain).
LES calculation and data cleaning by Shiri Kadishson Yanay (Tel Aviv University).
Please cite if you use this dataset.
