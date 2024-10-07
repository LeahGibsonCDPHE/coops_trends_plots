from data_plots import *
from data_conversions import *
import pandas as pd

sites = ['DECO', 'PVCO', 'BFCO', 'MPCO']

# load datafiles
data_dict = {}
summed_dict = {}
for site in sites:
    print(site)
    df = pd.read_csv(f'data/{site}_annual_data.csv')
    data_dict[site] = df

    # get summed compounds
    df_summed = convert_to_ppb(df)
    summed_dict[site] = df_summed


# plot the data
#bar_charts(data_dict=data_dict, parameter='Xylene', units='ppbC')

line_plot(data_dict=summed_dict, parameter='summed', units='ppbV')

line_subplots(summed_dict)

#stacked_line(data_dict)

# quarterly plot