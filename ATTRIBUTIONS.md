# Data Sources and Attributions

The files in `Data/` are **third-party datasets** redistributed here so that the
analysis in this repository can be reproduced. They were **not** created by the
authors of this repository, and they are **not** covered by this repository's CC0
dedication (see [LICENSE](LICENSE) and the *Scope* section of the
[README](README.md)). Each dataset remains subject to the terms of its original
publisher, summarised below.

Where a publisher specifies a citation, that citation is reproduced here and
should be used in any further work that reuses these files.

Third-party *software* dependencies are listed separately in
[LICENSES_THIRD_PARTY](LICENSES_THIRD_PARTY).


---

## Eurostat

**Files (19):**

| File | Eurostat dataset | Indicator |
|---|---|---|
| `demo_mlexpec__custom_21725383_spreadsheet.xlsx` | `demo_mlexpec` | Life expectancy by age and sex |
| `health_exp_2015_euros.xlsx` | `hlth_sha11_hc` | Health care expenditure by function |
| `health_exp_ntl_currency.xlsx` | `hlth_sha11_hc` | Health care expenditure by function |
| `hlth_cd_apr$defaultview_spreadsheet.xlsx` | `hlth_cd_apr` | Treatable and preventable mortality of residents by cause |
| `hlth_cd_apr__custom_19859093_spreadsheet.xlsx` | `hlth_cd_apr` | Treatable and preventable mortality of residents by cause |
| `hlth_sha11_hc__custom_19272646_spreadsheet.xlsx` | `hlth_sha11_hc` | Health care expenditure by function |
| `hlth_sha11_hc__custom_21843707_spreadsheet.xlsx` | `hlth_sha11_hc` | Health care expenditure by function |
| `hlth_sha11_hc__custom_21990053_spreadsheet.xlsx` | `hlth_sha11_hc` | Health care expenditure by function |
| `hlth_sha11_hchf__custom_19272605_spreadsheet.xlsx` | `hlth_sha11_hchf` | Expenditure for selected health care functions by financing scheme |
| `real GDP per capita.xlsx` | `sdg_08_10` | Real GDP per capita |
| `sdg_17_40__custom_19859181_spreadsheet.xlsx` | `sdg_17_40` | General government gross debt |
| `tec00001__custom_19859210_spreadsheet.xlsx` | `tec00001` | Gross domestic product at market prices |
| `tec00115__custom_21725449_spreadsheet.xlsx` | `tec00115` | Real GDP growth rate — volume |
| `tec00127__custom_19859170_spreadsheet.xlsx` | `tec00127` | General government deficit/surplus |
| `tessi190_page_spreadsheet.xlsx` | `tessi190` | Gini coefficient of equivalised disposable income |
| `tps00001_page_spreadsheet.xlsx` | `tps00001` | Population on 1 January |
| `tps00027_page_spreadsheet.xlsx` | `tps00027` | Infant mortality rate |
| `tps00198_page_spreadsheet.xlsx` | `tps00198` | Old-age-dependency ratio |
| `tps00205__custom_21724756_spreadsheet.xlsx` | `tps00205` | Life expectancy at birth by sex |

Source: Eurostat, the statistical office of the European Union.
<https://ec.europa.eu/eurostat>

Eurostat data are reusable under the European Commission's reuse policy
(Commission Decision 2011/833/EU), which permits reuse for commercial and
non-commercial purposes provided the source is acknowledged. Eurostat is not
responsible for any conclusions drawn from these data. Copyright and reuse notice:
<https://ec.europa.eu/eurostat/web/main/help/copyright-notice>

Several files are user-defined extracts (the `__custom_########` suffix) and
therefore reflect a specific selection of dimensions and a specific extraction
date. The extraction date and the date of last data update are recorded in each
file's `Summary` sheet.

---

## World Bank — World Development Indicators

**Files (3):**

| File | Indicator(s) used |
|---|---|
| `P_Data_Extract_From_World_Development_Indicators.xlsx` | Life expectancy at birth, total (`SP.DYN.LE00.IN`); Fertility rate, total (`SP.DYN.TFRT.IN`) |
| `P_Data_Extract_From_World_Development_Indicators-tot.xlsx` | Net barter terms of trade index (`TT.PRI.MRCH.XD.WD`) |
| `P_Data_Extract_From_World_Development_Indicators-inflation.xlsx` | Inflation, consumer prices, annual % (`FP.CPI.TOTL.ZG`) |

Source: World Bank, World Development Indicators.
<https://databank.worldbank.org/source/world-development-indicators>

**License: CC BY-4.0** — as declared in the `Series - Metadata` sheet of each
file. Full terms:
<https://datacatalog.worldbank.org/public-licenses#cc-by>

This license **requires attribution**, which is the reason these files may not be
redistributed under CC0. Underlying data for these series originate with the UN
Population Division (World Population Prospects), UNCTAD, and the IMF
(International Financial Statistics), as recorded in each file's metadata sheet.

---

## World Health Organization

**Files (2):**

| File | Dataset |
|---|---|
| `Immunization expenditure 2026-05-02 15-55 UTC.xlsx` | Immunization expenditure indicators, collected via the WHO/UNICEF Joint Reporting Form on Immunization (JRF) |
| `Diphtheria Tetanus Toxoid and Pertussis (DTP) vaccination coverage 2026-26-06 23-34 UTC.xlsx` | WHO/UNICEF Estimates of National Immunization Coverage (WUENIC), 2024 Revision (completed 15 July 2025), covering 1980–2024 |

Sources, as cited inside the files themselves:

* Immunization financing indicators —
  <https://www.who.int/teams/immunization-vaccines-and-biologicals/vaccine-access/planning-and-financing/immunization-financing-indicators>
* WHO/UNICEF Estimates of National Immunization Coverage —
  <https://www.who.int/teams/immunization-vaccines-and-biologicals/immunization-analysis-and-insights/global-monitoring/immunization-coverage/who-unicef-estimates-of-national-immunization-coverage>
* WHO Immunization data portal — <https://data.who.int/indicators/i/F8E084C>

WHO displays these data as reported by national authorities. Reuse is subject to
WHO's terms of use and copyright policy:
<https://www.who.int/about/policies/publishing/copyright>

---

## European Central Bank

**File:** `ECB Data Portal long_20260305094301.xlsx`

GDP deflator series, ECB Data Portal, series key
`MNA.Q.Y.I9.W2.S1.S1.B.B1GQ._Z._Z._Z.IX.D.N`:
<https://data.ecb.europa.eu/data/datasets/MNA/MNA.Q.Y.I9.W2.S1.S1.B.B1GQ._Z._Z._Z.IX.D.N>

Source: European Central Bank. ECB Data Portal content may be reused with
acknowledgement of the source; see the ECB copyright notice at
<https://www.ecb.europa.eu/services/using-our-site/html/index.en.html>

---

## Penn World Table 11.0

**File:** `pwt110.xlsx`

The citation requested on the file's own `Info` sheet:

> Feenstra, Robert C., Robert Inklaar and Marcel P. Timmer (2015), "The Next
> Generation of the Penn World Table", *American Economic Review*, 105(10),
> 3150–3182.

Available for download, with full documentation, at <https://www.ggdc.net/pwt>
(also reachable via the Groningen Growth and Development Centre at
<https://www.rug.nl/ggdc/productivity/pwt/>)

---

## Barro-Lee Educational Attainment Dataset

**Files:** `BL_v3_F1564.csv`, `BL_v3_M1564.csv`
(average years of schooling, female and male, ages 15–64)

> Barro, Robert J. and Jong-Wha Lee (2013), "A New Data Set of Educational
> Attainment in the World, 1950–2010", *Journal of Development Economics*, 104,
> 184–198.

Dataset home: <http://www.barrolee.com/>

---

## V-Dem (Varieties of Democracy)

**File:** `V-Dem-CY-Core-v16-1950.csv`
(Country-Year Core dataset, version 16; the `v2x_rule` rule-of-law index is the
variable used)

V-Dem asks that both the dataset and the project's methodology reference be
cited. Please cite the Country-Year Core dataset v16, Varieties of Democracy
(V-Dem) Project, together with the corresponding V-Dem Codebook and Methodology
for v16. Current citation forms and DOIs are published at:
<https://v-dem.net/data/the-v-dem-dataset/>

---

## Quality of Government (QoG) Standard Time-Series

**File:** `qog_std_ts_jan26_fh_pr.csv`
(the `fh_pr` Freedom House political rights variable is the variable used)

Source: The Quality of Government Institute, University of Gothenburg — Quality
of Government Standard Dataset, time-series, January 2026 version. Citation
forms and codebook: <https://www.gu.se/en/quality-government/qog-data>

The `fh_pr` variable is compiled by QoG from **Freedom House**, *Freedom in the
World* (political rights rating), which should be credited as the original
source: <https://freedomhouse.org/report/freedom-world>

---

## Embedded images

Eurostat spreadsheet extracts contain the Eurostat logo (`xl/media/image1.png`)
as supplied by Eurostat's download service. It is a European Union trademark,
included only as part of the unmodified source files, and is not licensed under
this repository's CC0 dedication.
