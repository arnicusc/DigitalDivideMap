import geopandas as gp      #GIS data
import pandas as pd         #Dataframes
import argparse
from os import path
from openpyxl import load_workbook
import os
import numpy as np

parser = argparse.ArgumentParser(description='Options')
parser.add_argument('--year', default='2019',help="Year for which script should run")
parser.add_argument('--layer', default='County', help="Layer for which script should run")
args = parser.parse_known_args()[0]
year = args.year
layer = args.layer

# Year options = [2018,2019,2020]
# Layer options = [county, tracts, bg, cd, city, trib, sd]

def year_fil(y):
    if int(y)<2020:
        return '2010'
    else:
        return '2020'

def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()

if path.exists(f"../Script Outputs/CPUC/BC_Collapsed_{year}.xlsx"):
    continue
else:
    print(f"Base file missing, creating BC_Collapsed_{year}.xlsx")
    os.system(f"python BC_Collapse.py --year {year}")

if layer == 'county':
    bc_collapsed = f"../Data Outputs/CPUC/BC_Collapsed_{year}.csv" #Block Code Collapsed Data
    print('Reading Data...')
    bc_collapsed = pd.read_csv(bc_collapsed)

    bc_collapsed['County'] = bc_collapsed['BlockCode'].astype('str').str[:4] #County
    bc_collapsed['CountyPop'] = bc_collapsed['County'].map(bc_collapsed.groupby('County')['POP10'].sum().to_dict())
    bc_collapsed['County_shrpop10'] = bc_collapsed['POP10'] / bc_collapsed['CountyPop']

    #Temprory Columns for Population Weight
    bc_collapsed['spop'] = bc_collapsed['served']*bc_collapsed['County_shrpop10']
    bc_collapsed['spop25'] = bc_collapsed['served25']*bc_collapsed['County_shrpop10']
    bc_collapsed['spop100'] = bc_collapsed['served100']*bc_collapsed['County_shrpop10']
    bc_collapsed['spopfib'] = bc_collapsed['served_fib']*bc_collapsed['County_shrpop10']
    bc_collapsed['cpop'] = bc_collapsed['comp']*bc_collapsed['County_shrpop10']
    bc_collapsed['cpop25'] = bc_collapsed['comp25']*bc_collapsed['County_shrpop10']
    bc_collapsed['cpop100'] = bc_collapsed['comp100']*bc_collapsed['County_shrpop10']
    bc_collapsed['cpopfib'] = bc_collapsed['comp_fib']*bc_collapsed['County_shrpop10']

    bc_collapsed['avgup'] = bc_collapsed['max_up']*bc_collapsed['County_shrpop10']
    bc_collapsed['avgdn'] = bc_collapsed['max_dn']*bc_collapsed['County_shrpop10']

    #Dataframe collapsed by Block Group
    cn_collapsed = pd.DataFrame()
    cn_collapsed['County'] = sorted(bc_collapsed['BlockCode'].astype('str').str[:4].unique()) #County
    cn_collapsed['County'] = '0' + cn_collapsed['County'].astype('str')
    cn_collapsed['CountyPop'] = bc_collapsed.groupby('County').CountyPop.mean().values
    cn_collapsed['LACounty'] = bc_collapsed.groupby('County').LACounty.mean().values #LACounty or not

    print("Calculating CPUC Variables")
    #Served and not served weighed by population
    cn_collapsed['served'] = bc_collapsed.groupby('County').spop.sum().values*100
    cn_collapsed['served25'] = bc_collapsed.groupby('County').spop25.sum().values*100
    cn_collapsed['served100'] = bc_collapsed.groupby('County').spop100.sum().values*100
    cn_collapsed['served_fib'] = bc_collapsed.groupby('County').spopfib.sum().values*100

    #Comp and no comp weighed by population
    cn_collapsed['comp'] = bc_collapsed.groupby('County').cpop.sum().values*100
    cn_collapsed['comp25'] = bc_collapsed.groupby('County').cpop25.sum().values*100
    cn_collapsed['comp100'] = bc_collapsed.groupby('County').cpop100.sum().values*100
    cn_collapsed['comp_fib'] = bc_collapsed.groupby('County').cpopfib.sum().values*100

    #Average max upload and download weighed by population 
    cn_collapsed['avg_max_up'] = bc_collapsed.groupby('County').avgup.sum().values
    cn_collapsed['avg_max_dn'] = bc_collapsed.groupby('County').avgdn.sum().values

    cn_collapsed = cn_collapsed.round(1)


    print("Calculating Adoption Variables")
    a = pd.read_stata(f'ACS_{year}.dta')
    a['bg'] = a['id'].str[9:]
    a= a[['bg','broadband_any','broadband_fixed']]
    a['county'] = a['bg'].str[:5]
    countydata = cn_collapsed.copy()

    adop_county = pd.DataFrame()
    adop_county['county'] = '0' + countydata['County'].astype('str')
    adop_county['countypopadop'] = countydata['CountyPop']

    adop_county['broadband_any'] = adop_county.county.map(a.groupby('county').apply(w_avg,'broadband_any','bgpop').to_dict())
    adop_county['broadband_fixed'] =  adop_county.county.map(a.groupby('county').apply(w_avg,'broadband_fixed','bgpop').to_dict())

    cn_collapsed['broadband_any'] = adop_county['broadband_any']
    cn_collapsed['broadband_fixed'] = adop_county['broadband_fixed']


    
    print("Calculating Ookla Variables")
    county = gp.read_file(f'../../Data Sources/Census/tl_{year_fil(year)}_06_county10.zip').to_crs("EPSG:4326")
    county_df = pd.DataFrame()
    county_df['GEOID10'] = county['GEOID10'].sort_values().values
    q1 = gp.read_file('../../Data Sources/Ookla/2019/2019-01-01_performance_fixed_tiles.zip')





