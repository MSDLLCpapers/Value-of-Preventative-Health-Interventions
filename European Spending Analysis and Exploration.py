# %% load in libraries

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS

# %% load in data

che = pd.read_excel("Data/hlth_sha11_hc__custom_19272646_spreadsheet.xlsx", skiprows=8, sheet_name = "Sheet 1")
che = che.loc[:, ~che.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

che_gov = pd.read_excel("Data/hlth_sha11_hchf__custom_19272605_spreadsheet.xlsx", skiprows=9, sheet_name = "Sheet 2")
che_gov = che_gov.loc[:, ~che_gov.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

prev = pd.read_excel("Data/hlth_sha11_hc__custom_19272646_spreadsheet.xlsx", skiprows=8, sheet_name = "Sheet 36")
prev = prev.loc[:, ~prev.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

prev_gov = pd.read_excel("Data/hlth_sha11_hchf__custom_19272605_spreadsheet.xlsx", skiprows=9, sheet_name = "Sheet 167")
prev_gov = prev_gov.loc[:, ~prev_gov.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

imm = pd.read_excel("Data/hlth_sha11_hc__custom_19272646_spreadsheet.xlsx", skiprows=8, sheet_name = "Sheet 38")
imm = imm.loc[:, ~imm.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

imm2 = pd.read_excel("Data/Immunization expenditure 2026-05-02 15-55 UTC.xlsx", sheet_name = "Sheet1")
imm2 = imm2[["COUNTRYNAME", "YEAR", "INDCODE", "VALUE"]].rename(columns={"COUNTRYNAME": "country", "YEAR": "year", "VALUE": "value"})

pop = pd.read_excel("Data/tps00001_page_spreadsheet.xlsx", skiprows=7, sheet_name = "Sheet 1")
pop = pop.loc[:, ~pop.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

debt = pd.read_excel("Data/sdg_17_40__custom_19859181_spreadsheet.xlsx", skiprows=9, sheet_name = "Sheet 2")
debt = debt.loc[:, ~debt.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

debt_euros = pd.read_excel("Data/sdg_17_40__custom_19859181_spreadsheet.xlsx", skiprows=9, sheet_name = "Sheet 1")
debt_euros = debt_euros.loc[:, ~debt_euros.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

pcgdp = pd.read_excel("Data/tec00001__custom_19859210_spreadsheet.xlsx", skiprows=8, sheet_name = "Sheet 3")
pcgdp = pcgdp.loc[:, ~pcgdp.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

gdp_euros = pd.read_excel("Data/tec00001__custom_19859210_spreadsheet.xlsx", skiprows=8, sheet_name = "Sheet 1")
gdp_euros = gdp_euros.loc[:, ~gdp_euros.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

deflator = pd.read_excel("Data/ECB Data Portal long_20260305094301.xlsx", sheet_name = "DATA(MNA)")
deflator = deflator[["TIME PERIOD", "OBS.VALUE"]]

deficit = pd.read_excel("Data/tec00127__custom_19859170_spreadsheet.xlsx", skiprows=9, sheet_name = "Sheet 3")
deficit = deficit.loc[:, ~deficit.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

deficit_euros = pd.read_excel("Data/tec00127__custom_19859170_spreadsheet.xlsx", skiprows=9, sheet_name = "Sheet 1")
deficit_euros = deficit_euros.loc[:, ~deficit_euros.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

mort_all = pd.read_excel("Data/hlth_cd_apr__custom_19859093_spreadsheet.xlsx", skiprows=10, sheet_name = "Sheet 2")
mort_all = mort_all.loc[:, ~mort_all.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

mort_prev = pd.read_excel("Data/hlth_cd_apr__custom_19859093_spreadsheet.xlsx", skiprows=10, sheet_name = "Sheet 4")
mort_prev = mort_prev.loc[:, ~mort_prev.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

mort_trt = pd.read_excel("Data/hlth_cd_apr__custom_19859093_spreadsheet.xlsx", skiprows=10, sheet_name = "Sheet 6")
mort_trt = mort_trt.loc[:, ~mort_trt.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

age_dep = pd.read_excel("Data/tps00198_page_spreadsheet.xlsx", skiprows = 7, sheet_name = "Sheet 1")
age_dep = age_dep.loc[:, ~age_dep.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

life_exp = pd.read_excel("Data/tps00205__custom_21724756_spreadsheet.xlsx", skiprows = 9, sheet_name = "Sheet 1")
life_exp = life_exp.loc[:, ~life_exp.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

inf_mort = pd.read_excel("Data/tps00027_page_spreadsheet.xlsx", skiprows = 8, sheet_name = "Sheet 1")
inf_mort = inf_mort.loc[:, ~inf_mort.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

life_exp65 = pd.read_excel("Data/demo_mlexpec__custom_21725383_spreadsheet.xlsx", skiprows = 9, sheet_name = "Sheet 1")
life_exp65 = life_exp65.loc[:, ~life_exp65.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

gini = pd.read_excel("Data/tessi190_page_spreadsheet.xlsx", skiprows=8, sheet_name = "Sheet 1")
gini = gini.loc[:, ~gini.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

gdp_growth = pd.read_excel("Data/tec00115__custom_21725449_spreadsheet.xlsx", skiprows=8, sheet_name = "Sheet 1")
gdp_growth = gdp_growth.loc[:, ~gdp_growth.columns.str.contains('^Unnamed')].rename(columns={"TIME": "country"})

# %% basic data processing

eu_countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
                "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
                "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
                "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
                "Slovenia", "Spain", "Sweden"]


def process_data(df: pd.DataFrame, category) -> pd.DataFrame:
    """


    Parameters
    ----------
    df : pd.DataFrame
        A data frame with European health-related data.
    category : string
        A string description to give to the type of data.

    Returns
    -------
    pd.DataFrame

    """
    _df = df.loc[df["country"].isin(eu_countries),]
    years = df.filter(regex="^2").columns
    cols = ["country"] + list(years)
    _df = _df[cols].replace({":":np.nan})
    _df["category"] = category
    _df2 = pd.melt(_df, id_vars=['country', "category"], value_vars=years)
    _df2 = _df2.rename(columns={"variable": "year"})
    _df2.year = _df2.year.astype(int)
    return(_df2)

che_df = process_data(che, "Total Health Expenditure")
prev_df = process_data(prev, "Preventive Health Expenditure")
imm_df = process_data(imm, "Immunization Health Expenditure")
pop_df = process_data(pop, "Population")
debt_df = process_data(debt, "Debt per GDP")
pcgdp_df = process_data(pcgdp, "PCGDP")
deficit_df = process_data(deficit, "Deficit per GDP")
mort_all_df = process_data(mort_all, "All Mortality")
mort_prev_df = process_data(mort_prev, "Preventable Mortality")
mort_trt_df = process_data(mort_trt, "Treatable Mortality")
life_exp_df = process_data(life_exp, "Life Expectancy")
inf_mort_df = process_data(inf_mort, "Infant Mortality")
life_exp65_df = process_data(life_exp65, "Life Expectancy 65")
gini_df = process_data(gini, "Gini")
gdp_growth_df = process_data(gdp_growth, "GDP Growth")

# %% process imm2
# for countries without immunization spending in Eurostat, we turn to the WHO Immunization data portal

imm2_df = imm2.loc[imm2.INDCODE == "FIN_TOTAL_VAC", ]
imm2_df = imm2_df.replace({"NR": np.nan, "ND": np.nan})
imm2_df.value = imm2_df.value.astype(float) / 1000000
imm2_df["category"] = "Immunization Health Expenditure"
imm2_df = imm2_df.drop("INDCODE", axis=1)
imm2_df.year = imm2_df.year.astype(int)
imm2_df = imm2_df.loc[imm2_df.country != "Hungary", ]
imm2_df = imm2_df.replace({"Netherlands (Kingdom of the)": "Netherlands"})

all_df = pd.concat([che_df, prev_df, imm_df, pop_df, debt_df, pcgdp_df, deficit_df, mort_all_df, mort_prev_df, mort_trt_df, life_exp_df,
                    inf_mort_df, life_exp65_df, gini_df, gdp_growth_df])
all_df.year = all_df.year.astype(int)

for country in imm2_df.country.unique():
    for year in all_df.loc[(all_df.country == country) & (all_df.category == "Immunization Health Expenditure"), "year"].unique():
        if np.isnan(all_df.loc[(all_df.country == country) & (all_df.year == year) & (all_df.category == "Immunization Health Expenditure"), "value"]).values[0] == np.True_:
            all_df.loc[(all_df.country == country) & (all_df.year == year) & (all_df.category == "Immunization Health Expenditure"), "value"] = imm2_df.loc[(imm2_df.country == country) & (imm2_df.year == year) & (imm2_df.category == "Immunization Health Expenditure"), "value"].values[0]

all_df = all_df.sort_values(["country", "year", "category"])

# %% Summarize spending by country and year

graph_df = all_df.pivot(index=["country", "year"], columns="category", values="value").reset_index()
graph_df["Total Health Expenditure per Capita"] = graph_df["Total Health Expenditure"]*1000000/graph_df["Population"]
graph_df["Preventive Health Expenditure per Capita"] = graph_df["Preventive Health Expenditure"]*1000000/graph_df["Population"]
graph_df["Immunization Health Expenditure per Capita"] = graph_df["Immunization Health Expenditure"]*1000000/graph_df["Population"]

summ_df = all_df[all_df.category.isin(["Immunization Health Expenditure", "Preventive Health Expenditure", "Total Health Expenditure"])]
summ_df2 = summ_df.pivot(index=["category", "country"], columns="year", values="value")
summ_df2 = summ_df2.sort_index(level=[0,1], ascending = [False, True])

row_sums = summ_df2.groupby(level=0).sum()

years = summ_df2.columns
summ_df_pct = summ_df2.copy()
for year in years:
    for country in summ_df_pct.index.get_level_values("country").unique():
        summ_df_pct.loc[("Preventive Health Expenditure", country), year] = summ_df2.loc[("Preventive Health Expenditure", country), year]/summ_df2.loc[("Total Health Expenditure", country), year]*100
        summ_df_pct.loc[("Immunization Health Expenditure", country), year] = summ_df2.loc[("Immunization Health Expenditure", country), year]/summ_df2.loc[("Total Health Expenditure", country), year]*100

summ_df_both = summ_df2.copy()
for year in years:
    for country in summ_df_both.index.get_level_values("country").unique():
        summ_df_both.loc[("Preventive Health Expenditure", country), year] = summ_df2.loc[("Preventive Health Expenditure", country), year].round(0).astype(str) + " (" + summ_df_pct.loc[("Preventive Health Expenditure", country), year].round(1).astype(str) + "%)"
        summ_df_both.loc[("Immunization Health Expenditure", country), year] = summ_df2.loc[("Immunization Health Expenditure", country), year].round(0).astype(str) + " (" + summ_df_pct.loc[("Immunization Health Expenditure", country), year].round(1).astype(str) + "%)"

summ_df_both[years] = summ_df_both[years].replace('nan (nan%)', '', regex=False)

prev_max_df1 = pd.DataFrame(summ_df_pct[summ_df_pct.index.get_level_values('category') == "Preventive Health Expenditure"].idxmax())
prev_max_df2 = pd.DataFrame(summ_df_pct[summ_df_pct.index.get_level_values('category') == "Preventive Health Expenditure"].max())

max_pct_df = pd.concat([prev_max_df1, prev_max_df2], axis=1).reset_index()
max_pct_df.columns = ["year", "country", "value"]

imm_max_df1 = pd.DataFrame(summ_df_pct[summ_df_pct.index.get_level_values('category') == "Immunization Health Expenditure"].idxmax())
imm_max_df2 = pd.DataFrame(summ_df_pct[summ_df_pct.index.get_level_values('category') == "Immunization Health Expenditure"].max())

max_pct_df2 = pd.concat([imm_max_df1, imm_max_df2], axis=1).reset_index()
max_pct_df2.columns = ["year", "country", "value"]

summ_df_up = summ_df2.copy()
for year in years:
    a_max = summ_df_pct.loc[summ_df_pct.index.get_level_values('category') == "Preventive Health Expenditure", year].max()
    aa_max = summ_df_pct.loc[summ_df_pct.index.get_level_values('category') == "Immunization Health Expenditure", year].max()
    for country in summ_df_up.index.get_level_values("country").unique():
        if np.isnan(summ_df_up.loc[("Preventive Health Expenditure", country), year]) == np.True_:
            continue
        else:
            summ_df_up.loc[("Preventive Health Expenditure", country), year] = (a_max/100)*summ_df2.loc[("Total Health Expenditure", country), year]
        if np.isnan(summ_df_up.loc[("Immunization Health Expenditure", country), year]) == np.True_:
            continue
        else:
            summ_df_up.loc[("Immunization Health Expenditure", country), year] = (aa_max/100)*summ_df2.loc[("Total Health Expenditure", country), year]

row_sums_up = summ_df_up.groupby(level=0).sum()

prev_inc2 = summ_df_up.sum() - summ_df2.sum()
prev_inc2.mean() * 1_000_000

below_avg_prev = {}
below_avg_imm = {}
summ_df_avg = summ_df2.copy()
for year in years:
    a_mean = summ_df_pct.loc[summ_df_pct.index.get_level_values('category') == "Preventive Health Expenditure", year].mean()
    aa_mean = summ_df_pct.loc[summ_df_pct.index.get_level_values('category') == "Immunization Health Expenditure", year].mean()
    below_avg_prev[year] = []
    below_avg_imm[year] = []
    for country in summ_df_avg.index.get_level_values("country").unique():
        if summ_df_pct.loc[("Preventive Health Expenditure", country), year] < a_mean:
            summ_df_avg.loc[("Preventive Health Expenditure", country), year] = (a_mean / 100) * summ_df2.loc[("Total Health Expenditure", country), year]
            below_avg_prev[year].append(country)
        if summ_df_pct.loc[("Immunization Health Expenditure", country), year] < aa_mean:
            summ_df_avg.loc[("Immunization Health Expenditure", country), year] = (aa_mean / 100) * summ_df2.loc[("Total Health Expenditure", country), year]
            below_avg_imm[year].append(country)

prev_inc = summ_df_avg.sum() - summ_df2.sum()
prev_inc.mean() * 1_000_000

row_sums_avg = summ_df_avg.groupby(level=0).sum()

row_sums["Average"] = row_sums.median(axis = 1)
row_sums_up["Average"] = row_sums_up.median(axis = 1)
row_sums_avg["Average"] = row_sums_avg.median(axis = 1)

counts = {}
for lst in below_avg_prev.values():
    for item in lst:
        counts[item] = counts.get(item, 0) + 1

df_counts1 = pd.DataFrame(list(counts.items()), columns=['country', 'count'])

counts2 = {}
for lst in below_avg_imm.values():
    for item in lst:
        counts2[item] = counts2.get(item, 0) + 1

df_counts2 = pd.DataFrame(list(counts2.items()), columns=['country', 'count'])

df_counts3 = graph_df.groupby('country')[['Preventive Health Expenditure', 'Immunization Health Expenditure']].count().reset_index()

df_counts = df_counts3.merge(df_counts1, how="outer", on="country")
df_counts = df_counts.merge(df_counts2, how="outer", on="country")

# %% run exploratory regressions

reg_df = graph_df.copy()
reg_df.columns = reg_df.columns.str.replace(" ", "_")
reg_df['L1_Preventive_Health_Expenditure_per_Capita'] = reg_df.groupby(['country'])['Preventive_Health_Expenditure_per_Capita'].shift(1)

panel_df = reg_df.copy()
panel_df = panel_df.set_index(["country", "year"])

panel_df["Other_Health_Expenditure_per_Capita"] = panel_df["Total_Health_Expenditure_per_Capita"] - panel_df["Preventive_Health_Expenditure_per_Capita"]
panel_df["Percent_Preventive"] = panel_df["Preventive_Health_Expenditure_per_Capita"]/panel_df["Total_Health_Expenditure_per_Capita"]
panel_df["Percent_Other"] = panel_df["Other_Health_Expenditure_per_Capita"]/panel_df["Total_Health_Expenditure_per_Capita"]
panel_df["Preventable_Mortality"] = panel_df["Preventable_Mortality"]
panel_df["Infant_Mortality"] = panel_df["Infant_Mortality"]
panel_df["Percent_Preventive"] = panel_df["Percent_Preventive"]*100
panel_df["Percent_Other"] = panel_df["Percent_Other"]*100

# regress preventable mortality on preventive health spending
model1 = PanelOLS.from_formula("Preventable_Mortality~Preventive_Health_Expenditure_per_Capita+Other_Health_Expenditure_per_Capita+EntityEffects+TimeEffects", data=panel_df)
result1 = model1.fit(cov_type="clustered", cluster_entity=True)
print(result1)

predicted_vals = result1.predict(data=panel_df)
fixed_effects = result1.estimated_effects
predictions = predicted_vals.join(fixed_effects, how="outer")

predictions["prev mort"] = predictions["predictions"] + predictions["estimated_effects"]

panel_df_up = panel_df.copy()
for year in years:
    for country in panel_df_up.index.get_level_values("country").unique():
        if np.isnan(panel_df_up.loc[(country, year), "Preventive_Health_Expenditure_per_Capita"]) == np.True_:
            continue
        else:
            panel_df_up.loc[(country, year), "Preventive_Health_Expenditure_per_Capita"] = (max_pct_df.loc[max_pct_df["year"] == year, "value"].values[0]/100)*panel_df_up.loc[(country, year), "Total_Health_Expenditure_per_Capita"]

predicted_vals_up = result1.predict(data=panel_df_up)
fixed_effects_up = result1.estimated_effects
predictions_up = predicted_vals_up.join(fixed_effects_up, how="outer")

predictions_up["prev mort"] = predictions_up["predictions"] + predictions_up["estimated_effects"]

panel_df_avg = panel_df.copy()
for year in years:
    for country in panel_df_avg.index.get_level_values("country").unique():
      panel_df_avg.loc[(country, year), "Preventive_Health_Expenditure_per_Capita"] = summ_df_avg.loc[("Preventive Health Expenditure", country), year]*1000000/panel_df_avg.loc[(country, year), "Population"]
      panel_df_avg.loc[(country, year), "Immunization_Health_Expenditure_per_Capita"] = summ_df_avg.loc[("Immunization Health Expenditure", country), year]*1000000/panel_df_avg.loc[(country, year), "Population"]

predicted_val_avg = result1.predict(data=panel_df_avg)
fixed_effect_avg = result1.estimated_effects
predictions_avg = predicted_val_avg.join(fixed_effect_avg, how="outer")

predictions_avg["prev mort"] = predictions_avg["predictions"] + predictions_avg["estimated_effects"]

act_pred_mort = panel_df[["Preventable_Mortality"]].copy()
act_pred_mort = act_pred_mort.join(predictions[["prev mort"]], rsuffix=" main", how="outer")
act_pred_mort = act_pred_mort.join(predictions_up[["prev mort"]], rsuffix=" high", how="outer")
act_pred_mort = act_pred_mort.join(predictions_avg[["prev mort"]], rsuffix=" avg", how="outer")

avg_pred_mort = act_pred_mort["prev mort"].median()
avg_pred_mort_high = act_pred_mort["prev mort high"].median()
avg_pred_mort_avg = act_pred_mort["prev mort avg"].median()

# regress life expectancy on percent of spending on health
model2 = PanelOLS.from_formula("Life_Expectancy~Preventive_Health_Expenditure_per_Capita+Other_Health_Expenditure_per_Capita+EntityEffects+TimeEffects", data=panel_df)
result2 = model2.fit(cov_type="clustered", cluster_entity=True)
print(result2)

model3 = PanelOLS.from_formula("Life_Expectancy_65~Preventive_Health_Expenditure_per_Capita+Other_Health_Expenditure_per_Capita+EntityEffects+TimeEffects", data=panel_df)
result3 = model3.fit(cov_type="clustered", cluster_entity=True)
print(result3)

csv1 = result1.summary.as_csv()
csv2 = result2.summary.as_csv()
csv3 = result3.summary.as_csv()

with open("Exploratory_Regression_Results.csv", "w") as f:
    f.write(csv1)
    f.write(csv2)
    f.write(csv3)
    