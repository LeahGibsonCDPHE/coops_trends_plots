"""
Code for making various plots of data
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 10,             # font fize for general text
    'axes.titlesize': 11,       # font size for plot titles
    'axes.labelsize': 10,        # font size for axis labels
    'xtick.labelsize': 9,       # font size for x-axis ticks
    'ytick.labelsize': 9,       # font size for y-axis ticks
    'legend.fontsize': 10,       # font size for legend
    'lines.linewidth': 2.5,     # set linewidth
    'lines.markersize': 8.5,    # set markersize
    'markers.fillstyle': 'none'
})

site_names = {
    'DECO': 'Denver-CAMP',
    'PVCO': 'Platteville',
    'BFCO': 'Brighton Fire',
    'MPCO': 'Missile Park'
}

header_names = {
    'TVOC': 'Combined Ozone Precursors',
    'summed': 'Summed Ozone Precursors',
    'BTEX': 'BTEX Compounds',
    'Benzene': 'Benzene',
    'Toluene': 'Toluene',
    'Ethylbenzene': 'Ethylbenzene',
    'Xylene': 'Xylene'
}

site_colors = {
    'DECO': 'blue',
    'PVCO': 'orange',
    'BFCO': 'green',
    'MPCO': 'pink'
}

site_markers = {
    'DECO': 'o',
    'PVCO': '^',
    'BFCO': 's',
    'MPCO': 'D'
}

# number of carbons for conversions from ppbC -> ppbV
ppb_conversions = {
    'Benzene': 6,
    'Toluene': 7,
    'Ethylbenzene': 8,
    'Xylene': 8
}

valid_years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

complete_years = {
    'DECO': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023],
    'PVCO': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'BFCO': [2020, 2021, 2022, 2023],
    'MPCO': [2022, 2023]
}

def bar_charts(data_dict, parameter, units):
    """
    Plots barcharts side by size with same scale y-axis
    
    Inputs:
    - data_dict: dict of data where key is site name and key if df of annual data
    - parameter: the column header to plot
    - units: ppbV or ppbC
    """

    n_sites = len(data_dict)

    fig, axes = plt.subplots(1, n_sites, figsize=(5*n_sites, 6), sharey=True)

    # case for if there is only one site
    if n_sites == 1:
        axes = [axes]
    
    valid_years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023] ### add in 2011 later
    max_years = len(valid_years)
    
    # create a color map
    cmap = plt.cm.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, max_years))
    colors_mapping = {}
    for i, year in enumerate(valid_years):
        colors_mapping[year] = colors[i]
    

    for ax, (site, df) in zip(axes, data_dict.items()):
        print(site)
        years = df['Year']
        values = df[parameter]

        # positions for the bars
        positions = np.linspace(0, 1, max_years + 1)[:-1]
        positions = positions[:len(years)] # only use as many positions as years we have

        # plot bar
        bars = ax.bar(positions, values, width=1/max_years, color=[colors_mapping[year] for year in years])


        # label x axis with site name
        ax.set_title(site)

        # remove x ticks
        ax.set_xticks([])
    
    # set y-labels
    fig.text(0.01, 0.5, f'{parameter} ({units})', va='center', rotation='vertical')

    # add legend
    year_names = [str(year) for year in valid_years]
    handles = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(valid_years))]
    plt.legend(handles, year_names, title='Year', loc='best', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()
    plt.show()
    

def line_plot(data_dict, parameter, units):
    """
    Plots all data on same line chart

    Inputs:
    - data_dict: dict of data where key is site name and key if df of annual data
    - parameter: the column header to plot
    - units: ppbV or ppbC
    """

    fig, ax = plt.subplots(figsize=(7,4.25))
    for site, df in data_dict.items():
        df = df.copy()
        # replace all 0's with nans
        df[parameter] = df[parameter].replace(0, np.nan)

        # get subset based on years with 75% complete data
        complete_df = df[df['Year'].isin(complete_years[site])]

        # get df of data not in that list
        incomplete_df = df[~df['Year'].isin(complete_years[site])]

        # plot complete data
        ax.plot(complete_df['Year'], complete_df[parameter], marker=site_markers[site], color=site_colors[site], label=site_names[site])

        # plot incomplete as scatter points (uncomment if desired)
        # ax.scatter(incomplete_df['Year'], incomplete_df[parameter], color=site_colors[site], marker=site_markers[site], alpha=0.6)
        
    ax.set_ylabel(f'{header_names[parameter]} ({units})')

    ax.set_ylim(bottom=0)

    ax.set_xticks(valid_years)
    ax.set_xticklabels(valid_years, rotation=45, ha='right')

    plt.tight_layout()
    plt.legend()
    plt.show()

def line_subplots(data_dict):
    """
    Plots BTEX with individual compounds as subplots

    Inputs
    - data_dict: dict of data where key is site name and key if df of annual data
    - units: ppbV or ppbC
    """

    compounds = ['BTEX', 'Benzene', 'Toluene', 'Ethylbenzene', 'Xylene']

    fig, axes = plt.subplots(nrows=5, figsize=(7, 10), sharex=True)

    for i, compound in enumerate(compounds):
        for site, df in data_dict.items():
            df = df.copy()
            # replace all 0's with nans
            df[compound] = df[compound].replace(0, np.nan)

            # get subset based on years with 75% complete data
            df = df[df['Year'].isin(complete_years[site])]


            # plot site data 
            axes[i].plot(df['Year'], df[compound], marker=site_markers[site], color=site_colors[site], label=site_names[site])

            # title the subplot
            axes[i].set_title(header_names[compound])

            # label yaxis
            axes[i].set_ylabel('(ppbV)')
    
            # set xticks
            axes[i].set_xticks(valid_years)
            axes[i].set_xticklabels(valid_years, rotation=45, ha='right')
    
    for ax in axes:
        ax.set_ylim(bottom=0) # set at end so top scates automatically

    plt.tight_layout()
    plt.legend(ncols=2)
    plt.show()


def stacked_line(data_dict):
    """
    Plots a stacked line chart for the BTEX compounds

    Inputs
    - data_dict: dict of data where key is site name and key if df of annual data
    - units: ppbV or ppbC
    """

    fig, axes = plt.subplots(nrows=len(data_dict.keys()), figsize=(7,8), sharex=True, sharey=True)

    compounds = ['Benzene', 'Toluene', 'Ethylbenzene', 'Xylene']
    colors=['#FF7F7F', '#9EDAE5', '#FFBB78', '#C5B0D5']

    for ax, (site, df) in zip(axes, data_dict.items()):
        stacked = [df[compound] for compound in compounds]

        ax.stackplot(valid_years, stacked, labels=compounds, colors=colors)
        ax.set_title(site_names[site])

        ax.set_ylabel('ppbC')

        # set xticks
        ax.set_xticks(valid_years)
        ax.set_xticklabels(valid_years, rotation=45, ha='right')

    fig.suptitle('Summed BTEX Compounds')
    plt.legend(ncols=2, loc='upper left')
    plt.tight_layout()
    plt.show()





