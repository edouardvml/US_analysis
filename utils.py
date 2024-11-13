def get_account_type_dummies(account_type):
    account_type_lead_digital = 0
    account_type_DSO = 0
    account_type_government = 0
    account_type_mid_market = 0
    if account_type == "Lead Digital":
        account_type_lead_digital = 1
    elif account_type == 'Group DSO':
        account_type_DSO = 1
    elif account_type == 'Governement':
        account_type_government = 1
    elif account_type == 'Mid Market':
        account_type_mid_market = 1
    # Si 'solo_practice', toutes les variables indicatrices restent à 0
    return account_type_lead_digital, account_type_DSO, account_type_government, account_type_mid_market

def get_interaction_type_dummies(interaction_type):
    interaction_type_cold_call = 0
    interaction_type_co_travel = 0
    interaction_type_appointment = 0
    
    if interaction_type == 'Cold call':
        interaction_type_cold_call = 1
    elif interaction_type == 'Co-Travel':
        interaction_type_co_travel = 1
    elif interaction_type == 'Appointment':
        interaction_type_appointment = 1
    # Si 'solo_practice', toutes les variables indicatrices restent à 0
    return interaction_type_cold_call, interaction_type_co_travel, interaction_type_appointment
