# Define Sustainable Occupations based on Wage Data
import pandas as pd

# Wage data for extended list of occupations 
occ_wage = pd.read_excel("data/feature/occ_earnings_data_all.xlsx", index_col=0)
# Wage and Employment Data from BLS 
data_clean = pd.read_csv("data/feature/bls_as_features.csv", index_col=0)

# Merge 
occ_wage.rename(columns={'ONET': 'O*NET-SOC Code'}, inplace=True)
occ_feat = pd.merge(data_clean.iloc[:,:-4], occ_wage, on='O*NET-SOC Code')

# Sustainable occupation := 1) occs with median hourly wage > living wage, 2) positive long-term growth 
# 1) Higher than MIT-living wage 
occ_feat['sustainable_wage'] = occ_feat.apply(lambda row: row['MEDIAN_HOURLY_EARNINGS'] - 25.02 if pd.notna(row['Employment change, numeric, 2022-32']) else np.nan, axis=1)
occ_feat['sustainable_wage_ind'] = occ_feat['sustainable_wage']>0
# 2) Stable Employment
occ_feat['stable_employment'] = occ_feat['Employment change, numeric, 2022-32']>0

# Define Sustainable Occupations 
occ_feat['sustainable'] = occ_feat.apply(lambda row: (row['sustainable_wage_ind']==True) & (row['stable_employment']==True) if pd.notna(row['Employment change, numeric, 2022-32']) else np.nan, axis=1)

#occ_feat.to_csv("data/feature/sustainability.csv")