import pandas as pd 

formula_df = pd.read_csv('./score_formula.csv',index_col=False)
plane_df = pd.read_csv('./master_scored.csv')

y_int = formula_df['Y-intercept'][0]
m = formula_df['Weight Coefficients'][0]

plane_df['Score'] = (plane_df['CO2 per mi per seat'] - y_int)/m

plane_df.to_csv('master_scored_ML.csv',index=False)