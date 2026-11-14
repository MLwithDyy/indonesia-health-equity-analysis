# Data sources

All tables come from Statistics Indonesia (Badan Pusat Statistik, BPS), province level, year 2024. They were downloaded from the BPS statistical tables on 14 November 2026. BPS content is copyrighted by BPS; this project cites the source for every table and uses it for non-commercial analysis. Check the BPS terms of use before redistributing anything.

## Tables used

| Short name | BPS table title | Unit | Year | File | Page |
|---|---|---|---|---|---|
| Life expectancy | Angka Harapan Hidup (AHH) Menurut Provinsi dan Jenis Kelamin | years, male and female | 2024 | `Angka_Harapan_Hidup__AHH__Menurut_Provinsi_dan_Jenis_Kelamin__2024.csv` | https://www.bps.go.id/id/statistics-table/2/NTAxIzI=/angka-harapan-hidup-ahh-menurut-provinsi-dan-jenis-kelamin-tahun.html |
| Poverty | Persentase Penduduk Miskin (P0) Menurut Provinsi dan Daerah | percent, urban, rural and total; March and September | 2024 | `Persentase_Penduduk_Miskin__P0__Menurut_Provinsi_dan_Daerah__2024.csv` | https://www.bps.go.id/id/statistics-table/2/MTkyIzI=/persentase-penduduk-miskin-p0-menurut-provinsi-dan-daerah-persen.html |
| GRDP per capita | [Seri 2010] Produk Domestik Regional Bruto Per Kapita | thousand rupiah, current and constant 2010 prices | 2024 | `_Seri_2010__Produk_Domestik_Regional_Bruto_Per_Kapita__2024.csv` | https://www.bps.go.id/id/statistics-table/2/Mjg4IzI=/seri-2010-produk-domestik-regional-bruto-per-kapita-ribu-rupiah.html |
| School participation | Angka Partisipasi Sekolah (APS) Menurut Provinsi dan Kelompok Umur | percent, ages 7-12, 13-15, 16-18, 19-23 | 2024 | `Angka_Partisipasi_Sekolah__APS__Menurut_Provinsi_dan_Kelompok_Umur__2024.csv` | https://www.bps.go.id/id/statistics-table/2/MjIxMSMy/angka-partisipasi-sekolah-aps-menurut-provinsi-dan-kelompok-umur.html |
| Sanitation | Proporsi Rumah Tangga Yang Memiliki Akses Terhadap Layanan Sanitasi Layak | percent of households | 2024 | `Proporsi_Rumah_Tangga_Yang_Memiliki_Akses_Terhadap_Layanan_Sanitasi_Layak__2024.csv` | https://www.bps.go.id/id/statistics-table/2/MTI2NyMy/proporsi-rumah-tangga-yang-memiliki-akses-terhadap-layanan-sanitasi-layak-persen.html |

Optional, not used in the analysis: population by province and sex (2025), used only for a data-quality check against the national totals.

## What was done to the data

- The CSVs have multi-row headers and a national row. The cleaning code (`notebooks/`) reads them with fixed row offsets and drops the national row (INDONESIA) before analysis.
- Province names are identical across all tables, so tables are merged on the name. The merge is checked to be one-to-one with 38 provinces.
- Poverty: the "Tahunan" (annual) columns are empty in the source, as BPS publishes poverty for March and September. The project uses the mean of the two rounds of the total rate. DKI Jakarta has no rural value, which is expected and not used.
- Life expectancy: the project's value is the mean of male and female values (not the official BPS total).
- GRDP per capita: log of the current-price value.
- Added by me: a region label for each province (Sumatera, Jawa, Bali-Nusa Tenggara, Kalimantan, Sulawesi, Maluku, Papua) and a flag for the six Papua provinces.

## Data-quality checks

- All 38 provinces present in every table, with identical names.
- No missing values in the analysis variables.
- Population-weighted means of the 38 provinces are close to the national row for every table (for example life expectancy for men 70.38 against 70.32, sanitation 83.45 against 83.60, APS 16-18 74.58 against 74.64), so no column is shifted or mislabelled.
- Population by sex adds up to the total, and the provinces add up to the national population.

## Tables considered and not used

- **Health facilities by province** (hospitals and community health centres): the table I could download stops at 2015, and two of its three columns did not behave like the labels (the "special hospitals" column totals 77,112 nationwide, which is not plausible), so it was not used. A more recent table (2025, with inpatient and non-inpatient centres) would not download.
- **Health workers by province:** the page would not load its table.
- **Stunting by province (SSGI 2024, Ministry of Health):** I could only find it in reports and charts, not as a downloadable table.

## Redistribution

The raw BPS files are not copied into this repository unless BPS terms allow it. The repository contains the cleaning code, the processed table `data/processed/province_health_2024.csv`, and the links above so anyone can download the originals.

## Attribution

Source: Badan Pusat Statistik (BPS), statistical tables listed above, accessed 14 November 2026.