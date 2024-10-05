"""
This code is used to pull data from AQS and create csv files of the data
"""

import pyaqsapi as aqs
from datetime import date
import time
import pandas as pd
import numpy as np

def compute_mean(df):
    # remove rows whre sample_duration_code is not 3 hours (B)
    df = df[df['sample_duration_code'] == 'B']

    # only keep rows where start time was 6:00
    df = df[df['time_local'] == '06:00']

    # compute the mean for that compound
    avg = round(df['sample_measurement'].mean(), 3)

    return df, avg

def compute_quarters(df):
    """
    Takes in data that has already been cleaned by compute_mean function
    """

    # convert 'date_local' to a datetime
    df['date_local'] = pd.to_datetime(df['date_local'], format='%Y-%m-%d')

    df = df[['date_local', 'sample_measurement']]

    # group data by quarters of the year
    df_quarters = df.groupby(df['date_local'].dt.to_period('Q')).mean()

    # drop column names 'date_local'
    df_quarters.drop(columns=['date_local'], inplace=True)

    return df_quarters

def save_samples(df, year, site, name):
    """
    Saves to G-drive
    """
    df.to_csv(f"X:\My Drive\coops_data\{site}_{year}_{name}.csv")


aqs.aqs_credentials(username='leah.gibson@state.co.us', key='amberram57')


compound_codes = {
    'Benzene': ['45201'],
    'Toluene': ['45202'],
    'Xylene': ['45109', '45204'],
    'Ethylbenzene': ['45203']
}


compound_codes = {
    "43280": "1-Butene",
    "43330": "1-Dodecene",
    "43328": "1-Heptene",
    "43245": "1-Hexene",
    "43279": "1-Nonene",
    "43145": "1-Octene",
    "43224": "1-Pentene",
    "43142": "1-Tridecene",
    "43299": "1-Undecene",
    "45225": "1,2,3-Trimethylbenzene",
    "45208": "1,2,4-Trimethylbenzene",
    "43218": "1,3-Butadiene",
    "45207": "1,3,5-Trimethylbenzene",
    "43552": "2-Butanone",
    "43236": "2-Ethyl-1-butene",
    "43225": "2-Methyl-1-butene",
    "43246": "2-Methyl-1-pentene",
    "43228": "2-Methyl-2-butene",
    "43960": "2-Methylheptane",
    "43263": "2-Methylhexane",
    "43285": "2-Methylpentane",
    "43244": "2,2-Dimethylbutane",
    "43292": "2,2,3-Trimethylpentane",
    "43250": "2,2,4-Trimethylpentane",
    "43284": "2,3-Dimethylbutane",
    "43291": "2,3-Dimethylpentane",
    "43252": "2,3,4-Trimethylpentane",
    "43247": "2,4-Dimethylpentane",
    "43282": "3-Methyl-1-butene",
    "43253": "3-Methylheptane",
    "43249": "3-Methylhexane",
    "43230": "3-Methylpentane",
    "43234": "4-Methyl-1-pentene",
    "43503": "Acetaldehyde",
    "43551": "Acetone",
    "43206": "Acetylene",
    "43505": "Acrolein",
    "45501": "Benzaldehyde",
    "45201": "Benzene",
    "43510": "Butyraldehyde",
    "43217": "cis-2-Butene",
    "43290": "cis-2-Hexene",
    "43227": "cis-2-Pentene",
    "43528": "Crotonaldehyde",
    "43248": "Cyclohexane",
    "43242": "Cyclopentane",
    "43283": "Cyclopentene",
    "43202": "Ethane",
    "45203": "Ethylbenzene",
    "43203": "Ethylene",
    "43502": "Formaldehyde",
    "43517": "Hexaldehyde",
    "43214": "Isobutane",
    "43270": "Isobutylene",
    "43221": "Isopentane",
    "43243": "Isoprene",
    "45210": "Isopropylbenzene",
    "45218": "m-Diethylbenzene",
    "45212": "m-Ethyltoluene",
    "45508": "m-Tolualdehyde",
    "45109": "m/p-Xylenes",
    "43552": "MEK",
    "43515": "Methacrolein",
    "43201": "Methane",
    "43261": "Methylcyclohexane",
    "43262": "Methylcyclopentane",
    "43212": "n-Butane",
    "43238": "n-Decane",
    "43141": "n-Dodecane",
    "43232": "n-Heptane",
    "43231": "n-Hexane",
    "43235": "n-Nonane",
    "43233": "n-Octane",
    "43220": "n-Pentane",
    "45209": "n-Propylbenzene",
    "43143": "n-Tridecane",
    "43954": "n-Undecane",
    "45211": "o-Ethyltoluene",
    "45204": "o-Xylene",
    "45219": "p-Diethylbenzene",
    "45213": "p-Ethyltoluene",
    "43204": "Propane",
    "43504": "Propionaldehyde",
    "43205": "Propylene",
    "43144": "Propyne",
    "45220": "Styrene",
    "45202": "Toluene",
    "43216": "trans-2-Butene",
    "43289": "trans-2-Hexene",
    "43226": "trans-2-Pentene",
    "43518": "Valeraldehyde",
    "43256": "alpha-pinene",
    "43257": "beta-pinene",
    "43510": "Butyraldehyde"
}

site_codes = {
    'DECO': ['031', '0002'],
    'PVCO': ['123', '0008'], 
    'BFCO': ['001', '0009'], # started in 2019
    'MPCO': ['123', '0014'] # started in 2021
}

site_years = {
    'DECO': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'PVCO': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'BFCO': [2020, 2021, 2022, 2023, 2024],
    'MPCO': [2021, 2022, 2023, 2024]
}

compound_names = list(compound_codes.values())
df_columns = ['Year', 'summed_COOPS', 'BTEX', 'Xylene'] + compound_names


### for all years prior to 2024 ###
for site, codes in site_codes.items():
    county_code = codes[0]
    site_code = codes[1]

    # make df for site with columns years, summed_COOPS, BTEX, Benzene, Toluene, Ethylbenzene, Xylene
    df = pd.DataFrame(columns=df_columns)

    # make df for quarters
    quarterly_averages_df = pd.DataFrame(columns=['Quarter'] + compound_names)

    for year in site_years[site]:    
        bdate=date(year, 1, 1)
        edate=date(year, 12, 31)

        # initializing things
        voc_sum = 0
        btex_sum = 0
        row = {
            'Year': year,
        }
        sample_dates = []
        quarterly_row = {}

        for parameter, name in compound_codes.items():
            try:
                data = aqs.bysite.sampledata(parameter=parameter, bdate=bdate, edate=edate, stateFIPS='08', countycode=county_code, sitenum=site_code)

                # save as csv in case we need it
                save_samples(df=data, year=year, site=site, name=name)

                # clean the data  and compute the yearly average concentration
                cleaned_df, concentration = compute_mean(data)
                voc_sum += concentration

                # add the compound data to row
                row[name] = concentration

                # document sample dates
                valid_dates = cleaned_df['date_local'].tolist()
                sample_dates.extend(valid_dates)


                # save list of sample dates (using Benzene to catch)
                if parameter == '45201':
                    print('found Benzene')
                    btex_sum += concentration

                if parameter == '45202':
                    print('found Toluene')
                    btex_sum += concentration
             
                if parameter == '45203':
                    print('found Ethylbenzene')
                    btex_sum += concentration
                 
                if parameter == '45109':
                    print('found a Xylene')
                    btex_sum += concentration
                    row['Xylene'] += concentration
                if parameter == '45204':
                    print('found the other Xylene')
                    btex_sum += concentration
                    row['Xylene'] += concentration
                
                # compute mean of quarters
                quarter_df = compute_quarters(cleaned_df)

                quarterly_row['Quarter'] = quarter_df.index.astype(str).tolist()
                quarterly_row[name] = quarter_df['sample_measurement'].tolist()
                
                print(f'{site} {year} {parameter} sucessful')

            except:
                print(f"Error for {site} {year} {parameter}")

            # pause 1 seconds
            time.sleep(1)
    
        # add to a df for the site
        row['summed_COOPS'] = voc_sum
        row['BTEX'] = btex_sum

        # append to a new row of the df by column name
        df.loc[len(df.index)] = row

        # append quarterly data to df
        new_df = pd.DataFrame(quarterly_row)
        quarterly_averages_df = pd.concat([quarterly_averages_df, new_df], ignore_index=True)

        # remove duplicates of the list 'sample_dates'
        sample_dates = list(set(sample_dates))

        # save data as df
        sample_dates_df = pd.DataFrame()
        sample_dates_df['sample_dates'] = sample_dates
        # convert to datetimes and sort
        sample_dates_df['sample_dates'] = pd.to_datetime(sample_dates_df['sample_dates'])
        sample_dates_df = sample_dates_df.sort_values(by='sample_dates')
        sample_dates_df.to_csv(f'data/{site}_sample_dates_{year}.csv')

    # export annual data to csv 
    df.to_csv(f'data/{site}_annual_data.csv')

    # export quarterly data to a csv
    quarterly_averages_df.to_csv(f'data/{site}_quarterly_data.csv')


