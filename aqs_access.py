"""
This code is used to pull data from AQS and create csv files of the data
"""

import pyaqsapi as aqs
from datetime import date
import time
import pandas as pd

def compute_mean(df):
    # remove rows whre sample_duration_code is not 3 hours (B)
    df = df[df['sample_duration_code'] == 'B']

    # remove repreats of date_local
    df = df.drop_duplicates(subset='date_local')

    # compute the mean
    try:
        avg = round(df['arithmetic_mean'].mean(), 3)
    except:
        avg = round(df['sample_measurement'].mean(), 3)

    return df, avg


aqs.aqs_credentials(username='leah.gibson@state.co.us', key='amberram57')


compound_codes = {
    'Benzene': ['45201'],
    'Toluene': ['45202'],
    'Xylene': ['45109', '45204'],
    'Ethylbenzene': ['45203']
}

num_carbons = {
    'Benzene': 6,
    'Toluene': 7,
    'Xylene': 8,
    'Ethylbenzene': 8,
}


tvoc_codes = [
    "43280", "43330", "43328", "43245", "43279", "43145", "43224", "43142", "43299",
    "45225", "45208", "43218", "45207", "43552", "43236", "43225", "43246", "43228",
    "43960", "43263", "43285", "43244", "43292", "43250", "43284", "43291", "43252",
    "43247", "43282", "43253", "43249", "43230", "43234", "43503", "43551", "43206",
    "43510", "45501", "45201", "43510", "43217", "43290", "43227", "43528", "43248",
    "43242", "43283", "43202", "45203", "43203", "43502", "43517", "43214", "43270",
    "43221", "43243", "45210", "45218", "45212", "45508", "45109", "43552", "43515",
    "43201", "43261", "43262", "43212", "43238", "43141", "43232", "43231", "43235",
    "43233", "43220", "45209", "43143", "43954", "45211", "45204", "45219", "45213",
    "43204", "43504", "43205", "43144", "45220", "45202", "43216", "43289", "43226",
    "43518", "43256", "43257"
]

site_codes = {
    'DECO': ['031', '0002'],
    'PVCO': ['123', '0008'], 
    'BFCO': ['001', '0009'], # started in 2020
    'MPCO': ['123', '0014'] # started in 2021
}

site_years = {
    'DECO': [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'PVCO': [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'BFCO': [2020, 2021, 2022, 2023],
    'MPCO': [2021, 2022, 2023]
}

df_columns = ['Year', 'TVOC', 'BTEX', 'Benzene', 'Toluene', 'Ethylbenzene', 'Xylene']


### for all years prior to 2024 ###
for site, codes in site_codes.items():
    county_code = codes[0]
    site_code = codes[1]

    # make df for site with columns years, TVOC, BTEX, Benzene, Toluene, Ethylbenzene, Xylene
    df = pd.DataFrame(columns=df_columns)

    for year in site_years[site]:    
        bdate=date(year, 1, 1)
        edate=date(year, 12, 31)


        voc_sum = 0
        btex_sum = 0
        row = {
            'Year': year,
            'Xylene': 0
        }
        for parameter in tvoc_codes:
            try:
                data = aqs.bysite.dailysummary(parameter=parameter, bdate=bdate, edate=edate, stateFIPS='08', countycode=county_code, sitenum=site_code)

                # clean the data  and compute the yearly average concentration
                cleaned_df, concentration = compute_mean(data)
                voc_sum += concentration

                # catch BTEX compounds
                if parameter == '45201':
                    print('found Benzene')
                    btex_sum += concentration
                    row['Benzene'] = concentration

                    # # save list of sample dates
                    # sample_dates = pd.DataFrame()
                    # sample_dates['Date'] = cleaned_df['date_local']
                    # sample_dates.to_csv(f'data/{site}_sample_dates_{year}.csv')

                if parameter == '45202':
                    print('found Toluene')
                    btex_sum += concentration
                    row['Toluene'] = concentration
                if parameter == '45203':
                    print('found Ethylbenzene')
                    btex_sum += concentration
                    row['Ethylbenzene'] = concentration
                if parameter == '45109':
                    print('found a Xylene')
                    btex_sum += concentration
                    row['Xylene'] += concentration
                if parameter == '45204':
                    print('found the other Xylene')
                    btex_sum += concentration
                    row['Xylene'] += concentration
                
                
                print(f'{site} {year} {parameter} sucessful')

            except:
                print(f"Error for {site} {year} {parameter}")

            # pause 6 seconds
            time.sleep(1)
    
        # add to a df for the site
        row['TVOC'] = voc_sum
        row['BTEX'] = btex_sum

        # append to a new row of the df by column name
        df.loc[len(df.index)] = row

    # export completex csv to a df
    df.to_csv(f'data/{site}_data.csv')


### for 2024 data ###

# values computed and manually added to speadsheets 
bdate = date(2024, 1, 1)
edate = date(2024, 9, 30)

for site, codes in site_codes.items():

    # skip DECO - no 2024 data available as of 10/3/2024
    if site == 'DECO': # no data from DECO
        continue

    county_code = codes[0]
    site_code = codes[1]

    # make df for site with columns years, TVOC, BTEX, Benzene, Toluene, Ethylbenzene, Xylene
    df = pd.DataFrame(columns=df_columns)

    voc_sum = 0
    btex_sum = 0
    row = {
        'Year': 2024,
        'Xylene': 0
    }
    for parameter in tvoc_codes:
        try:
            data = aqs.bysite.sampledata(parameter=parameter, bdate=bdate, edate=edate, stateFIPS='08', countycode=county_code, sitenum=site_code)

            # clean the data  and compute the yearly average concentration
            cleaned_df, concentration = compute_mean(data)
            voc_sum += concentration

            # catch BTEX compounds
            if parameter == '45201':
                print('found Benzene')
                btex_sum += concentration
                row['Benzene'] = concentration

                # save list of sample dates
                sample_dates = pd.DataFrame()
                sample_dates['Date'] = cleaned_df['date_local']
                sample_dates.to_csv(f'data/{site}_sample_dates_{2024}.csv')

            if parameter == '45202':
                print('found Toluene')
                btex_sum += concentration
                row['Toluene'] = concentration
            if parameter == '45203':
                print('found Ethylbenzene')
                btex_sum += concentration
                row['Ethylbenzene'] = concentration
            if parameter == '45109':
                print('found a Xylene')
                btex_sum += concentration
                row['Xylene'] += concentration
            if parameter == '45204':
                print('found the other Xylene')
                btex_sum += concentration
                row['Xylene'] += concentration
            
            
            print(f'{site} {2024} {parameter} sucessful')

        except:
            print(f"Error for {site} {2024} {parameter}")

        # pause 
        time.sleep(1)

    # add to a df for the site
    row['TVOC'] = voc_sum
    row['BTEX'] = btex_sum

    # append to a new row of the df by column name
    df.loc[len(df.index)] = row

    # export completex csv to a df
    df.to_csv(f'data/2024_{site}_data.csv')