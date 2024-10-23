import pandas as pd
import numpy as np
import streamlit as st

from utils import get_account_type_dummies, get_interaction_type_dummies

pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns',30)

df_hazard = pd.read_csv('df_hazard_app.csv', 
                          delimiter = ';')

st.title("Cox-PH model - US Analysis")
st.header("")
# --- Première ligne : Deux colonnes pour les variables client et interaction ---
col1, col2 = st.columns(2)

with col1:
    st.header(":red[Account type]")
    # Variables correspondant au type du client
    account_type = st.selectbox("Account type :", ['Solo Practice', 'Group DSO', 'Governement', 'Mid Market'])
    potential_real = st.selectbox("Potential Real (0, 1 ou 2) :", [0, 1, 2])
    st.write("Inside sales :")
    flag_inside_sales_checkbox = st.checkbox("True", value=False)
    flag_inside_sales = int(flag_inside_sales_checkbox)

with col2:
    st.header(":red[Interaction nature]")
    # Données sur l'interaction elle-même
    interaction_type = st.selectbox("", ['Phone call', 'Cold call', 'Co-Travel', 'Appointment'])
    st.subheader("Had interaction past 3 months", divider = "red")
    # Interactions passées
    flag_had_phone_call_checkbox = st.checkbox("Phone call", value=False)
    flag_had_phone_call = int(flag_had_phone_call_checkbox)
    flag_had_cold_call_checkbox = st.checkbox("Cold call", value=False)
    flag_had_cold_call = int(flag_had_cold_call_checkbox)
    flag_had_co_travel_checkbox = st.checkbox("Co-Travel", value=False)
    flag_had_co_travel = int(flag_had_co_travel_checkbox)
    flag_had_appointment_checkbox = st.checkbox("Appointment", value=False)
    flag_had_appointment = int(flag_had_appointment_checkbox)

# --- Deuxième partie : Caractéristiques des commandes du client ---
st.header(":red[Past purchase]")

# Utilisation de st.columns pour disposer les widgets sur deux colonnes
col3, col4 = st.columns(2)

with col3:
    st.subheader("Has purchased one of these Septodont products", divider = "red")
    # Widgets pour les produits commandés (cases à cocher)
    flag_has_ordered_bioroot_checkbox = st.checkbox("Bioroot", value=False)
    flag_has_ordered_bioroot = int(flag_has_ordered_bioroot_checkbox)
    flag_has_ordered_biodentine_checkbox = st.checkbox("Biodentine", value=False)
    flag_has_ordered_biodentine = int(flag_has_ordered_biodentine_checkbox)
    flag_has_ordered_Orasoothe_checkbox = st.checkbox("Orasoothe", value=False)
    flag_has_ordered_Orasoothe = int(flag_has_ordered_Orasoothe_checkbox)
    flag_has_ordered_DycloPro_checkbox = st.checkbox("DycloPro", value=False)
    flag_has_ordered_DycloPro = int(flag_has_ordered_DycloPro_checkbox)

with col4:
    st.subheader("Count of previous orders", divider = "red")
    # Widgets pour le nombre de commandes (selectbox)
    order_count_septo = st.selectbox("Septocaine/Septanest", [0, 1, 2, 3])
    order_count_other_pain = st.selectbox("Pain management (others)", [0, 1, 2, 3, 4, 5])
    order_count_other_th = st.selectbox("Therapeutic products (others)", [0, 1, 2, 3])



account_type_DSO, account_type_government, account_type_mid_market = get_account_type_dummies(account_type)
interaction_type_cold_call, interaction_type_co_travel, interaction_type_appointment = get_interaction_type_dummies(interaction_type)

# Liste pour stocker les résultats
results = []

# Parcourir chaque observation dans le dataframe
for idx, row in df_hazard.iterrows():
    variable = row['variables']
    # Customer account type
    beta_flag_inside_sales = row['flag_insides_sales']
    beta_potential_real = row['potential_real']
    beta_account_type_DSO = row.get('account_type_DSO', 0)
    beta_account_type_government = row.get('account_type_Governement', 0)
    beta_account_type_mid_market = row.get('account_type_mid-market', 0)
    # Interaction type
    beta_interaction_type_cold_call = row.get('interaction_type_cold_call', 0)
    beta_interaction_type_co_travel = row.get('interaction_type_co-travel', 0)
    beta_interaction_type_appointment = row.get('interaction_type_appointment', 0)
    # Past interactions in the last 3 months
    beta_flag_had_phone_call = row['flag_had_phone_call']
    beta_flag_had_cold_call = row['flag_had_cold_call']
    beta_flag_had_co_travel = row['flag_had_co_travel']
    beta_flag_had_appointment = row['flag_had_appointment']
    # Past orders count
    beta_other_pain_product = row['order_count_other_pain_management']
    beta_other_therapeutic = row['order_count_other_therapeutic']
    beta_septo = row['order_count_Septocaine']
    beta_flag_has_ordered_bioroot = row['flag_has_order_BioRoot']
    beta_flag_has_ordered_biodentine = row['flag_has_order_Biodentine']
    beta_flag_has_ordered_Orasoothe = row['flag_has_order_Orasoothe']
    beta_flag_has_order_DycloPro = row['flag_has_order_DycloPro']
    
    CH_1_month = row['CH_1_month']
    CH_3_months = row['CH_3_months']
    CH_6_months = row['CH_6_months']

    # Calcul du prédicteur linéaire pour l'observation
    eta = (
        beta_flag_inside_sales * flag_inside_sales +
        beta_potential_real * potential_real +
        beta_other_pain_product * order_count_other_pain +
        beta_other_therapeutic * order_count_other_th +
        beta_septo * order_count_septo +
        beta_account_type_DSO * account_type_DSO +
        beta_account_type_government * account_type_government +
        beta_account_type_mid_market * account_type_mid_market + 
        beta_interaction_type_cold_call * interaction_type_cold_call +
        beta_interaction_type_co_travel * interaction_type_co_travel +
        beta_interaction_type_appointment * interaction_type_appointment  + 
        beta_flag_had_phone_call * flag_had_phone_call + 
        beta_flag_had_cold_call * flag_had_cold_call +
        beta_flag_had_co_travel * flag_had_co_travel +
        beta_flag_had_appointment * flag_had_appointment  + 
        beta_flag_has_ordered_bioroot * flag_has_ordered_bioroot +
        beta_flag_has_ordered_biodentine * flag_has_ordered_biodentine +
        beta_flag_has_ordered_Orasoothe * flag_has_ordered_Orasoothe +
        beta_flag_has_order_DycloPro * flag_has_ordered_DycloPro
        )
    exp_eta = np.exp(eta)

    # Calcul des probabilités de survie pour l'observation
    survie_1_mois = 1 - np.exp(-CH_1_month * exp_eta)
    survie_3_mois = 1 - np.exp(-CH_3_months * exp_eta)
    survie_6_mois = 1 - np.exp(-CH_6_months * exp_eta)

    # Ajouter les résultats à la liste
    results.append({
        'Product': variable,
        #'Buyers after 1 month': f"{survie_1_mois * 100:.0f}%",
        'Buyers after 3 months': f"{survie_3_mois * 100:.0f}%",
        #'Buyers after 6 months': f"{survie_6_mois * 100:.0f}%"
    })

# Créer un dataframe à partir des résultats
results_df = pd.DataFrame(results)

# Afficher les résultats
st.subheader("", divider = "red")
st.write("### Purchase likelihood for each Septodont product")
st.dataframe(results_df.set_index('Product'))
