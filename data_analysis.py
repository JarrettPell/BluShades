import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import re
import numpy as np
from scipy import stats
from statsmodels.formula.api import ols

def main():
    # read in the data from csv that I removed the unneccesarry non data columns from at the top
    df = pd.read_csv('BluShades_November 15, 2022_15.00.csv', sep=',')        
    
    # level of interest on a scale of 1-7
    df_interest = df[df['Q14_1']>=1]
    print('Level of interest statistics')
    print(df_interest['Q14_1'].describe())
    print('\n\n')
    # count    75.000000
    # mean      3.813333
    # std       1.950006
    # min       1.000000
    # 25%       2.000000
    # 50%       4.000000
    # 75%       5.000000
    # max       7.000000
    # Name: Q14_1, dtype: float64
    
    # Interest one sample t-test 
    print('Level of interest t-test')
    print(stats.ttest_1samp(df_interest['Q14_1'], 4))
    print('\n\n')
    
    # Create a df for struggling with headphones falling out
    df_fallout = df[df['Q17']>=1]
    # broken not fixing pie chart made one in excel instead
    # print(df_fallout["Q17"])
    # df_fallout['Q17'].plot.pie(y=['1','2','3'])
    # # plt.pie(df_fallout['Q17'])
    # plt.show()

    # Average interest by times headphones falls out
    df_interest_avg = df_fallout.groupby('Q17')['Q14_1'].mean().round(2)
    df_interest_avg = df_interest_avg.to_frame()
    df_interest_avg = df_interest_avg.rename(columns={'Q14_1': 'avg_interest(1-7)', 'Q17': 'headphone_fallout'})
    df_interest_avg.plot(kind='bar')
    plt.xticks(ticks=np.arange(0,3,1), labels=['yes', 'no', 'sometimes'])
    plt.xlabel('Do you struggle with headphones falling out of ears?')
    plt.show()
    corr, p_val = stats.pearsonr(df_interest['Q17'], df_interest['Q14_1'])
    print(f"correlation, p-value (Headphone fallout and Interest Level): {corr}, {p_val}")
    print('\n\n')
    # correlation, p-value (Headphone fallout and Interest Level): 0.031112139863730688, 0.7910266493184238
    
    # Average intrerest by times headphone fallsout merged yes and sometimes columns\
    df_fallout_sorted = df_fallout
    df_fallout_sorted['Q17'] = df_fallout_sorted['Q17'].apply(sometimes_to_yes)
    # print(df_fallout_sorted)
    
    df_interest_avg = df_fallout_sorted.groupby('Q17')['Q14_1'].mean().round(2)
    df_interest_avg = df_interest_avg.to_frame()
    df_interest_avg = df_interest_avg.rename(columns={'Q14_1': 'avg_interest(1-7)', 'Q17': 'headphone_fallout'})
    df_interest_avg.plot(kind='bar')
    plt.xticks(ticks=np.arange(0,2,1), labels=['yes', 'no'])
    plt.xlabel('Do you struggle with headphones falling out of ears?')
    plt.show()
    corr, p_val = stats.pearsonr(df_interest['Q17'], df_interest['Q14_1'])
    print(f"correlation, p-value (Headphone fallout and Interest Level): {corr}, {p_val}")
    print('\n\n')
    
    # Level of comfort wearing both one sample t-test
    df_comfort = df[df['Q19_1']>=1]
    print('Level of comfort Statistics')
    print(df_comfort['Q19_1'].describe())
    print('\n\n')
    # count    74.000000
    # mean      4.500000
    # std       1.859813
    # min       1.000000
    # 25%       3.000000
    # 50%       4.000000
    # 75%       6.000000
    # max       7.000000
    # Name: Q19_1, dtype: float64
    print('Level of comfort t-test')
    print(stats.ttest_1samp(df_comfort['Q19_1'], 4))
    print('\n\n')
    # df_comfort['Q19_1'].plot(kind='bar')
    # plt.show()
    
    # How often they wear headphones in days a week
    df_head_freq = df[df['Q6_1']>=1]
    print('Headphone Frequency Statistics')
    print(df_head_freq['Q6_1'].describe())
    print('\n\n')
    print('Headphone Frequency t-test')
    print(stats.ttest_1samp(df_head_freq['Q6_1'], 4))
    print('\n\n')
    

def sometimes_to_yes(num):
    if num != 2:
        num = 1
    return num
    
main()