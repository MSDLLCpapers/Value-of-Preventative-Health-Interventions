#%% libraries

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import country_converter as coco

# %% load in data

pwt_raw = pd.read_excel("pwt110.xlsx", sheet_name = "Data")
wdi_raw = pd.read_excel("P_Data_Extract_From_World_Development_Indicators.xlsx", sheet_name = "Data")
law_order_raw = pd.read_csv("V-Dem-CY-Core-v16-1950.csv")
f_education_raw = pd.read_csv("BL_v3_F1564.csv")
m_education_raw = pd.read_csv("BL_v3_M1564.csv")
tot_raw = pd.read_excel("P_Data_Extract_From_World_Development_Indicators-tot.xlsx", sheet_name = "Data")
democracy_raw = pd.read_csv("qog_std_ts_jan26_fh_pr.csv")
inflation_raw = pd.read_excel("P_Data_Extract_From_World_Development_Indicators-inflation.xlsx", sheet_name = "Data")
dtp1_raw = pd.read_excel("Diphtheria Tetanus Toxoid and Pertussis (DTP) vaccination coverage 2026-26-06 23-34 UTC.xlsx", sheet_name = "Sheet1")
prevention_raw = pd.read_excel("hlth_sha11_hc__custom_21990053_spreadsheet.xlsx", sheet_name = "Sheet 1", skiprows=8)
immunization_raw = pd.read_excel("hlth_sha11_hc__custom_21990053_spreadsheet.xlsx", sheet_name = "Sheet 2", skiprows=8)

# %% function to rename countries appropriately

def rename_countries(df):
    """
    

    Parameters
    ----------
    df : pd.DataFrame
        A data frame containing health spending and outcomes data.

    Returns
    -------
    None.

    """
    _df = df.copy()
    _df.country = _df.country.replace({"Congo (the)": "Congo", "D.R. of the Congo": "Democratic Republic of the Congo", "Republic of Vietnam": "Vietnam"})
    _df["ISO3"] = coco.convert(_df.country, to = "ISO3")
    _df = _df.loc[_df.ISO3 != "not found", ]
    _df.country = coco.convert(_df.ISO3, to = "short_name")
    _df = _df.drop(columns = "ISO3")
    return(_df)

#%% process PWT data

"""
Masia cites Barro (2012) as the basis of their regression specification.
According to Barro (2012), the PWT data is used for the following variables:
    * PPP-adjusted real per capita GDP
        * column: rgdpo = Output-side real GDP at chained PPPs (in mil. 2021US$)
        * column: pop = Population (in millions)
        * calculation = rgdpo/pop
    * ratio to GDP of investment (private plus public)
        * column: ccon = Real consumption of households and government, at current PPPs (in mil. 2021US$)
        * column: cda = Real domestic absorption, (real consumption plus investment), at current PPPs (in mil. 2021US$)
        * column: cgdpo = Output-side real GDP at current PPPs (in mil. 2021US$)
        * calculation = (cda - ccon)/cgdpo
    * ratio to GDP of government consumption
        * column: ccon = Real consumption of households and government, at current PPPs (in mil. 2021US$)
        * column: cgdpo = Output-side real GDP at current PPPs (in mil. 2021US$)
        * calculation = ccon/cgdpo
    * openness ratio (exports plus imports relative to GDP)
        * column: csh_x = Share (in CGDPo) of merchandise exports at current PPPs
        * column: csh_m = Share (in CGDPo) of merchandise imports at current PPPs (note this is coded as negative)
        * calculation = csh_x + abs(csh_m)
"""

cols_to_keep = ["country", "year", "rgdpo", "pop", "ccon", "cda", "cgdpo", "csh_x", "csh_m"]

pwt_df = pwt_raw[cols_to_keep]

pwt_df["PCGDP"] = pwt_df["rgdpo"]/pwt_df["pop"]
pwt_df["Investment_Ratio"] = (pwt_df["cda"]-pwt_df["ccon"])/pwt_df["cgdpo"]
pwt_df["Consumption_Ratio"] = pwt_df["ccon"]/pwt_df["cgdpo"]
pwt_df["Openness_Ratio"] = pwt_df["csh_x"] + abs(pwt_df["csh_m"])

pwt_df_final = pwt_df[["country", "year", "PCGDP", "Investment_Ratio", "Consumption_Ratio", "Openness_Ratio"]]
pwt_df_final.year = pd.to_numeric(pwt_df_final.year, errors="coerce")
pwt_df_final = rename_countries(pwt_df_final)

# %% process WDI data

"""
Masia cites Barro (2012) as the basis of their regression specification.
According to Barro (2012), the WDI data is used for the following variables:
    * life expectancy at birth
        * Series Name: Life expectancy at birth, total (years)
    * total fertility rate
        * Series Name: Fertility rate, total (births per woman)
"""

cols_to_drop = ["Series Code", "Country Code"]

wdi_df = wdi_raw.drop(columns = cols_to_drop)
wdi_df.columns = wdi_df.columns.str.replace(r'\s*\[.*?\]', '', regex=True)

wdi_df2 = pd.melt(wdi_df, id_vars = ["Country Name", "Series Name"], var_name="year")
wdi_df2 = wdi_df2.loc[wdi_df2["Series Name"].isin(['Life expectancy at birth, total (years)',
       'Fertility rate, total (births per woman)']),]

wdi_df_final = wdi_df2.pivot(index = ["Country Name", "year"], columns = "Series Name", values = "value").reset_index()
wdi_df_final.year = pd.to_numeric(wdi_df_final.year, errors="coerce")
wdi_df_final['Life expectancy at birth, total (years)'] = pd.to_numeric(wdi_df_final['Life expectancy at birth, total (years)'], errors="coerce")
wdi_df_final['Fertility rate, total (births per woman)'] = pd.to_numeric(wdi_df_final['Fertility rate, total (births per woman)'], errors="coerce")

wdi_df_final = wdi_df_final.rename(columns = {"Country Name": "country"})
wdi_df_final = rename_countries(wdi_df_final)

# %% process law and order data

"""
Masia cites Barro (2012) as the basis of their regression specification.
According to Barro (2012), the source of law and order data is the International Country Risk Guide from the Political Risk Services firm. 
This data is behind a paywall, so we use the "Rule of Law" indicator from the World Bank.
    * Series Name: Rule of Law - Governance score (0-100)
    * Calculation: Divide by 100.
"""
cols_to_keep = ["country_name", "year", "v2x_rule"]
law_order_df = law_order_raw[cols_to_keep]


law_order_df_final = law_order_df.copy()
law_order_df_final = law_order_df_final.rename(columns = {"country_name": "country", "v2x_rule":"Law_Order"})
law_order_df_final = rename_countries(law_order_df_final)


# %% process education

"""
Masia cites Barro (2012) as the basis of their regression specification.
According to Barro (2012), the Barro-Lee data is used for the following variables:
    * Average years of school attainment for females
        * column: yr_sch
    * Average years of school attainment for males
        * column: yr_sch
"""

cols_to_keep = ["country", "year", "yr_sch"]
f_education_df = f_education_raw[cols_to_keep]
m_education_df = m_education_raw[cols_to_keep]

f_education_df.columns = ["country", "year", "Female_Education"]
m_education_df.columns = ["country", "year", "Male_Education"]

education_df_final = pd.merge(f_education_df, m_education_df, on = ["country", "year"], how = "outer")
education_df_final.year = pd.to_numeric(education_df_final.year, errors="coerce")
education_df_final = rename_countries(education_df_final)

# %% terms of trade

"""
Masia cites Barro (2012) as the basis of their regression specification.
According to Barro (2012), the terms of trade data comes from the WDI.
    * terms-of-trade change (growth rates over five years of export prices relative to
import prices)
        * Series Name: Net barter terms of trade index (2015 = 100)
"""

tot_df = tot_raw.drop(columns = cols_to_drop)
tot_df.columns = tot_df.columns.str.replace(r'\s*\[.*?\]', '', regex=True)

tot_df2 = pd.melt(tot_df, id_vars = ["Country Name", "Series Name"], var_name="year", value_name = "Terms_Trade")
tot_df2["Terms_Trade"] = pd.to_numeric(tot_df2["Terms_Trade"], errors = "coerce")/100

tot_df_final = tot_df2.copy()
tot_df_final.year = pd.to_numeric(tot_df_final.year, errors="coerce")

tot_df_final = tot_df_final.rename(columns = {"Country Name": "country"})
tot_df_final = tot_df_final.drop(columns = "Series Name")
tot_df_final = rename_countries(tot_df_final)

# %% democracy

"""
Masia cites Barro (2012) as the basis of their regression specification.
According to Barro (2012), the democracy indicator (political rights) comes from Freedom House.
    * The political-rights variable (converted from seven categories to a 0-1 scale, with 1
representing highest rights)
        * column: fh_pr
"""

cols_to_keep = ["cname", "year", "fh_pr"]
democracy_df = democracy_raw[cols_to_keep]
democracy_df["Democracy"] = (7-democracy_df["fh_pr"])/6
democracy_df_final = democracy_df.copy()

democracy_df_final.year = pd.to_numeric(democracy_df_final.year, errors="coerce")
democracy_df_final = democracy_df_final.rename(columns = {"cname": "country"})
democracy_df_final = rename_countries(democracy_df_final)

# %% inflation

"""
Masia cites Barro (2012) as the basis of their regression specification.
According to Barro (2012), the inflatoin data comes from the WDI.
    * inflation rate 
        * Series Name: Inflation, consumer prices (annual %)
"""

inflation_df = inflation_raw.drop(columns = cols_to_drop)
inflation_df.columns = inflation_df.columns.str.replace(r'\s*\[.*?\]', '', regex=True)

inflation_df2 = pd.melt(inflation_df, id_vars = ["Country Name", "Series Name"], var_name="year", value_name = "Inflation_Rate")
inflation_df2["Inflation_Rate"] = pd.to_numeric(inflation_df2["Inflation_Rate"], errors = "coerce")

inflation_df_final = inflation_df2.copy()
inflation_df_final.year = pd.to_numeric(inflation_df_final.year, errors="coerce")
inflation_df_final = inflation_df_final.rename(columns = {"Country Name": "country"})
inflation_df_final = inflation_df_final.drop(columns = "Series Name")
inflation_df_final = rename_countries(inflation_df_final)

# %% process DTP1

dtp1_df = dtp1_raw[["NAME", "YEAR", "COVERAGE_CATEGORY", "COVERAGE"]]
dtp1_df = dtp1_df.loc[dtp1_df.COVERAGE_CATEGORY == "WUENIC",]
dtp1_df = dtp1_df.drop(columns = "COVERAGE_CATEGORY")
dtp1_df.columns = ["country", "year", "DTP1"]
dtp1_df_final = dtp1_df.copy()
dtp1_df_final = rename_countries(dtp1_df_final)

# %% process prevention and immunization spending

prevention_df = prevention_raw.loc[:, ~prevention_raw.columns.str.contains('^Unnamed')].rename(columns= {"TIME": "country"})
years = list(prevention_df.filter(regex="^1").columns) + list(prevention_df.filter(regex="^2").columns)
cols = ["country"] + list(years)
prevention_df = prevention_df[cols].replace({":":np.nan})
prevention_df2 = pd.melt(prevention_df, id_vars=['country'], value_vars=years, var_name = "year", value_name="Preventive_Spending")
prevention_df2.year = prevention_df2.year.astype(int)
prevention_df2.Preventive_Spending = pd.to_numeric(prevention_df2.Preventive_Spending, errors = "coerce")
prevention_df_final = rename_countries(prevention_df2)

immunization_df = immunization_raw.loc[:, ~immunization_raw.columns.str.contains('^Unnamed')].rename(columns= {"TIME": "country"})
years = list(immunization_df.filter(regex="^1").columns) + list(immunization_df.filter(regex="^2").columns)
cols = ["country"] + list(years)
immunization_df = immunization_df[cols].replace({":":np.nan})
immunization_df2 = pd.melt(immunization_df, id_vars=['country'], value_vars=years, var_name = "year", value_name="Immunization_Spending")
immunization_df2.year = immunization_df2.year.astype(int)
immunization_df2.Immunization_Spending = pd.to_numeric(immunization_df2.Immunization_Spending, errors = "coerce")
immunization_df_final = rename_countries(immunization_df2)

# %% combine data

barro_reg_df = pd.merge(pwt_df_final, wdi_df_final, on = ["country", "year"], how = "outer")
barro_reg_df = pd.merge(barro_reg_df, law_order_df_final, on = ["country", "year"], how = "outer")
barro_reg_df = pd.merge(barro_reg_df, education_df_final, on = ["country", "year"], how = "outer")
barro_reg_df = pd.merge(barro_reg_df, tot_df_final, on = ["country", "year"], how = "outer")
barro_reg_df = pd.merge(barro_reg_df, democracy_df_final, on = ["country", "year"], how = "outer")
barro_reg_df = pd.merge(barro_reg_df, inflation_df_final, on = ["country", "year"], how = "outer")
barro_reg_df = pd.merge(barro_reg_df, dtp1_df_final, on = ["country", "year"], how = "outer")
barro_reg_df = pd.merge(barro_reg_df, prevention_df_final, on = ["country", "year"], how = "outer")
barro_reg_df = pd.merge(barro_reg_df, immunization_df_final, on = ["country", "year"], how = "outer")

barro_reg_df["Preventive_Spending"] = barro_reg_df["Preventive_Spending"].replace({0: np.nan})
barro_reg_df["Immunization_Spending"] = barro_reg_df["Immunization_Spending"].replace({0: np.nan})

barro_reg_df["Female_Education"] = barro_reg_df.groupby("country")["Female_Education"].ffill()
barro_reg_df["Male_Education"] = barro_reg_df.groupby("country")["Male_Education"].ffill()
barro_reg_df["ln_Preventive_Spending"] = np.log(barro_reg_df["Preventive_Spending"])
barro_reg_df["ln_Immunization_Spending"] = np.log(barro_reg_df["Immunization_Spending"])

for country in barro_reg_df.country.unique():
    barro_reg_df.loc[(barro_reg_df.country == country), "lagged_DTP1"] = barro_reg_df.loc[(barro_reg_df.country == country), "DTP1"].shift(-5)
    barro_reg_df.loc[(barro_reg_df.country == country), "lagged_ln_Preventive_Spending"] = barro_reg_df.loc[(barro_reg_df.country == country), "ln_Preventive_Spending"].shift(-5)
    barro_reg_df.loc[(barro_reg_df.country == country), 'avg_lagged_DTP1'] = barro_reg_df.loc[(barro_reg_df.country == country), 'lagged_DTP1'].rolling(window=5).mean()
    barro_reg_df.loc[(barro_reg_df.country == country), 'avg_lagged_ln_Preventive_Spending'] = barro_reg_df.loc[(barro_reg_df.country == country), 'lagged_ln_Preventive_Spending'].rolling(window=5).mean()
    barro_reg_df.loc[(barro_reg_df.country == country), "lagged_ln_Immunization_Spending"] = barro_reg_df.loc[(barro_reg_df.country == country), "ln_Immunization_Spending"].shift(-5)
    barro_reg_df.loc[(barro_reg_df.country == country), 'avg_lagged_ln_Immunization_Spending'] = barro_reg_df.loc[(barro_reg_df.country == country), 'lagged_ln_Immunization_Spending'].rolling(window=5).mean()

barro_reg_df2 = barro_reg_df.copy()
barro_reg_df2.year = barro_reg_df2.year.astype(int)
barro_reg_df2["ln_PCGDP"] = np.log(barro_reg_df2["PCGDP"])
barro_reg_df2["ln_Fertility_Rate"] = np.log(barro_reg_df2["Fertility rate, total (births per woman)"])
barro_reg_df2["Inverse_Life_Expectancy"] = 1/barro_reg_df2["Life expectancy at birth, total (years)"]

for country in barro_reg_df2.country.unique():
    first_year = barro_reg_df2.loc[barro_reg_df2.country == country, "year"].min()
    last_year = barro_reg_df2.loc[barro_reg_df2.country == country, "year"].max()
    years = list(range(first_year, last_year+1, 5)) + [last_year+1]
    years = list(dict.fromkeys(years))
    for i, t in enumerate(years):
        start_year = t
        try:
            end_year = years[i+1]-1
            sub_years = list(range(start_year, end_year+1))
            for year in sub_years:
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "PCGDP_Growth"] = (1/len(sub_years))*(barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == end_year), "ln_PCGDP"].values[0]-barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "ln_PCGDP"].values[0])
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "interval"] = i+1
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "lagged_ln_PCGDP"] = barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "ln_PCGDP"]
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "avg_lagged_DTP1"] = barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "avg_lagged_DTP1"]
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "avg_lagged_Preventive_Spending"] = barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "avg_lagged_Preventive_Spending"]
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "avg_lagged_Immunization_Spending"] = barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "avg_lagged_Immunization_Spending"]
        except:
            continue
        
barro_reg_df2["lagged_ln_PCGDP"] = barro_reg_df2.groupby("country")["lagged_ln_PCGDP"].ffill()

barro_reg_df_final = barro_reg_df2.groupby(["country", "interval"]).mean()
barro_reg_df_final = barro_reg_df_final.replace({-np.inf:np.nan, np.inf:np.nan})

# %% run Barro and Masia specifications using our data

model = PanelOLS.from_formula("PCGDP_Growth~lagged_ln_PCGDP+Inverse_Life_Expectancy+ln_Fertility_Rate+Law_Order+Investment_Ratio+Female_Education+Male_Education+Consumption_Ratio+Openness_Ratio+Terms_Trade+Democracy+I(Democracy**2)+Inflation_Rate+TimeEffects", data=barro_reg_df_final)
result = model.fit(cov_type="clustered")
print(result)
csv1 = result.summary.as_csv()

model2 = PanelOLS.from_formula("PCGDP_Growth~lagged_ln_PCGDP+avg_lagged_DTP1+Inverse_Life_Expectancy+ln_Fertility_Rate+Law_Order+Investment_Ratio+Female_Education+Male_Education+Consumption_Ratio+Openness_Ratio+Terms_Trade+Democracy+I(Democracy**2)+Inflation_Rate+TimeEffects", data=barro_reg_df_final)
result2 = model2.fit(cov_type="clustered")
print(result2)
csv2 = result2.summary.as_csv()
    
# %% run Barro and Masia specifications for EU countries and modify
cc = coco.CountryConverter()

barro_reg_df2 = barro_reg_df.copy()
barro_reg_df2 = barro_reg_df2.loc[barro_reg_df2.year > 1950, ]
for country in barro_reg_df2.country.unique():
    barro_reg_df2.loc[(barro_reg_df2.country == country), "lagged_DTP1"] = barro_reg_df2.loc[(barro_reg_df2.country == country), "DTP1"].shift(-3)
    barro_reg_df2.loc[(barro_reg_df2.country == country), "lagged_Preventive_Spending"] = barro_reg_df2.loc[(barro_reg_df2.country == country), "Preventive_Spending"].shift(-3)
    barro_reg_df2.loc[(barro_reg_df2.country == country), "lagged_Immunization_Spending"] = barro_reg_df2.loc[(barro_reg_df2.country == country), "Immunization_Spending"].shift(-3)
    barro_reg_df2.loc[(barro_reg_df2.country == country), "lagged_ln_Preventive_Spending"] = barro_reg_df2.loc[(barro_reg_df2.country == country), "ln_Preventive_Spending"].shift(-3)
    barro_reg_df2.loc[(barro_reg_df2.country == country), 'avg_lagged_DTP1'] = barro_reg_df2.loc[(barro_reg_df2.country == country), 'lagged_DTP1'].rolling(window=3).mean()
    barro_reg_df2.loc[(barro_reg_df2.country == country), 'avg_lagged_ln_Preventive_Spending'] = barro_reg_df2.loc[(barro_reg_df2.country == country), 'lagged_ln_Preventive_Spending'].rolling(window=3).mean()
    barro_reg_df2.loc[(barro_reg_df2.country == country), "lagged_ln_Immunization_Spending"] = barro_reg_df2.loc[(barro_reg_df2.country == country), "ln_Immunization_Spending"].shift(-3)
    barro_reg_df2.loc[(barro_reg_df2.country == country), 'avg_lagged_ln_Immunization_Spending'] = barro_reg_df2.loc[(barro_reg_df2.country == country), 'lagged_ln_Immunization_Spending'].rolling(window=3).mean()

barro_reg_df2.year = barro_reg_df2.year.astype(int)
barro_reg_df2["ln_PCGDP"] = np.log(barro_reg_df2["PCGDP"])
barro_reg_df2["ln_Fertility_Rate"] = np.log(barro_reg_df2["Fertility rate, total (births per woman)"])
barro_reg_df2["Inverse_Life_Expectancy"] = 1/barro_reg_df2["Life expectancy at birth, total (years)"]

for country in barro_reg_df2.country.unique():
    first_year = barro_reg_df2.loc[barro_reg_df2.country == country, "year"].min()
    last_year = barro_reg_df2.loc[barro_reg_df2.country == country, "year"].max()
    years = list(range(first_year, last_year+1, 3)) + [last_year+1]
    years = list(dict.fromkeys(years))
    for i, t in enumerate(years):
        start_year = t
        try:
            end_year = years[i+1]-1
            sub_years = list(range(start_year, end_year+1))
            for year in sub_years:
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "PCGDP_Growth"] = (1/len(sub_years))*(barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == end_year), "ln_PCGDP"].values[0]-barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "ln_PCGDP"].values[0])
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "interval"] = i+1
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "lagged_ln_PCGDP"] = barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "ln_PCGDP"]
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "avg_lagged_DTP1"] = barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "avg_lagged_DTP1"]
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "avg_lagged_Preventive_Spending"] = barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "avg_lagged_Preventive_Spending"]
                barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == year), "avg_lagged_Immunization_Spending"] = barro_reg_df2.loc[(barro_reg_df2.country == country) & (barro_reg_df2.year == start_year), "avg_lagged_Immunization_Spending"]
        except:
            continue
        
barro_reg_df2["lagged_ln_PCGDP"] = barro_reg_df2.groupby("country")["lagged_ln_PCGDP"].ffill()
barro_reg_df2 = barro_reg_df2.loc[barro_reg_df2.country.isin(cc.EU27.name_short), ]

sum_cols = ["Preventive_Spending", "Immunization_Spending", "lagged_Preventive_Spending", "lagged_Immunization_Spending"]
first_cols = ["Inverse_Life_Expectancy", "ln_Fertility_Rate", "lagged_ln_PCGDP"]
groupby_cols = ["country", "interval"]
agg_dict = {col: 'mean' for col in barro_reg_df2.columns if col not in groupby_cols}
for col in sum_cols:
    agg_dict[col] = 'sum'
for col in first_cols:
    agg_dict[col] = 'first'
    
barro_reg_df_eu = barro_reg_df2.groupby(groupby_cols).agg(agg_dict)
barro_reg_df_eu["sum_ln_Preventive_Spending"] = np.log(barro_reg_df_eu["Preventive_Spending"])
barro_reg_df_eu["sum_ln_Immunization_Spending"] = np.log(barro_reg_df_eu["Immunization_Spending"])
barro_reg_df_eu["sum_ln_lagged_Preventive_Spending"] = np.log(barro_reg_df_eu["lagged_Preventive_Spending"])
barro_reg_df_eu["sum_ln_lagged_Immunization_Spending"] = np.log(barro_reg_df_eu["lagged_Immunization_Spending"])

barro_reg_df_eu = barro_reg_df_eu.replace({-np.inf:np.nan, np.inf:np.nan})

model3 = PanelOLS.from_formula("PCGDP_Growth~lagged_ln_PCGDP+Inverse_Life_Expectancy+ln_Fertility_Rate+Law_Order+Investment_Ratio+Female_Education+Male_Education+Consumption_Ratio+Openness_Ratio+Terms_Trade+Democracy+I(Democracy**2)+Inflation_Rate+TimeEffects", data=barro_reg_df_eu)
result3 = model3.fit(cov_type="clustered", cluster_time = True)
print(result3)
csv3 = result3.summary.as_csv()

model4 = PanelOLS.from_formula("PCGDP_Growth~lagged_ln_PCGDP+lagged_DTP1+Inverse_Life_Expectancy+ln_Fertility_Rate+Law_Order+Investment_Ratio+Female_Education+Male_Education+Consumption_Ratio+Openness_Ratio+Terms_Trade+Democracy+I(Democracy**2)+Inflation_Rate+TimeEffects", data=barro_reg_df_eu)
result4 = model4.fit(cov_type="clustered", cluster_time = True)
print(result4)
csv4 = result4.summary.as_csv()

model5= PanelOLS.from_formula("PCGDP_Growth~lagged_ln_PCGDP+sum_ln_lagged_Immunization_Spending+ln_Fertility_Rate+Law_Order+Investment_Ratio+Consumption_Ratio+Openness_Ratio+Terms_Trade+Democracy+I(Democracy**2)+Inflation_Rate+TimeEffects", data=barro_reg_df_eu)
result5 = model5.fit(cov_type="clustered", cluster_time = True)
print(result5)
csv5= result5.summary.as_csv()

with open("Masia_Replication_and_Modification.csv", "w") as f:
    f.write(csv1)
    f.write(csv2)
    f.write(csv3)
    f.write(csv4)
    f.write(csv5)