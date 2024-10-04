from data_plots import *
import pandas as pd

sites = ['DECO', 'PVCO', 'BFCO', 'MPCO']

# load datafiles
data_dict = {}
for site in sites:
    df = pd.read_csv(f'data/{site}_data.csv')
    data_dict[site] = df

# plot the data
#bar_charts(data_dict=data_dict, parameter='Xylene', units='ppbC')

line_plot(data_dict=data_dict, parameter='TVOC', units='ppbC')

line_subplots(data_dict)

#stacked_line(data_dict, units='ppbC')