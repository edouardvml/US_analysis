import pandas as pd
import numpy as np
pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns',20)

df_baseline = pd.read_csv('assets/BaselineHazard_byproducts.csv', 
                          delimiter = ';')

#%%
df_cumulative = df_baseline.copy()

columns_cumsum = ["BH_global", "BH_Biodentine", "BH_Septocaine", "BH_Bioroot", "BH_Orasooth", "BH_Dyclopro"]
df_cumulative[columns_cumsum] = df_baseline[columns_cumsum].cumsum()

df_cumulative.head()
#%%

df_coeff = pd.read_csv('assets/Coeff_CoxPH.csv',
                       delimiter = ";")
df_transposed = df_coeff.T.copy()
df_transposed.columns = df_transposed.iloc[0]  # Met la première ligne comme noms de colonnes
df_transposed = df_transposed.drop(df_transposed.index[0])  # Supprime cette ligne des données
df_transposed = df_transposed.apply(lambda x: pd.to_numeric(x, errors='ignore')) #apply only on numeric columns
df_coeff_hazard = df_transposed.copy().reset_index(names = 'variables')
df_coeff_hazard.head()
#%%

# Cumulative Hazard at 1 month / 3 months / 6 months
#print(df_cumulative.head(6))
df_CH = pd.DataFrame({
    "variables" : ["global", "septocaine_septanest", "Biodentine", "BioRoot", "Orasoothe", "DycloPro", ],
    "CH_1_month" : [0.159886, 0.169233, 0.019779, 0.018676, 0.016898, 0.011369],
    "CH_3_months" : [0.370441, 0.378907, 0.043128, 0.041095, 0.0367, 0.024226],
    "CH_6_months" : [0.559303, 0.537997, 0.06473, 0.063259, 0.053854, 0.035084]
    })

df_hazard = df_coeff_hazard.merge(df_CH, on = 'variables', how = 'left')
print(df_hazard)
df_hazard.to_csv('df_hazard_app_V2.csv', sep = ';', index = False)

#%%
