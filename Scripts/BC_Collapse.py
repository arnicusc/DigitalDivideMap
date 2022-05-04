import geopandas as gp      #GIS data
import pandas as pd         #Dataframes
import argparse
from os import path
from openpyxl import load_workbook

from utils import download_from_drive #Download file from Drive

filepath = "../Data Outputs/CPUC/BC_Collapsed.xlsx"


parser = argparse.ArgumentParser(description='Year')
parser.add_argument('--year', default='2019',help="Year for which script should run")
args = parser.parse_known_args()[0]
year = args.year

#Download Retail Blacklist https://drive.google.com/file/d/1yvKFaXDvpjDRbYgibP_9QvSghDn2lM03/view?usp=sharing
download_from_drive('1yvKFaXDvpjDRbYgibP_9QvSghDn2lM03', "../Data Sources/CPUC/retail_check_new.xlsx")

cpuc_zipfile    = "zip://../Data Sources/CPUC/CPUC_"+year+".zip!Wireline_BB_Consumer.shp" #CPUC Broadband Data

census=''
if int(year) >= 2020:
    census = "../Data Sources/Census/Census_2020.xlsx"
else:
    census = "../Data Sources/Census/Census_Blocks_2010.xlsx"

retail_check = "../retail_check.xlsx" #Retail Check

print('Reading Data...')
cpuc = gp.read_file(cpuc_zipfile) #Read CPUC file
census = pd.read_excel(census) #Read Census file
retail_check = pd.read_excel(retail_check) #Read Retail Check file

#Rename columns for Census Data
if int(year) < 2020:
    census = census.rename(columns = {"SE_T002_001":"Population", "SE_T002_002":"Population Density","SE_T002_006":"Area (sq mi)", "SE_T058_001":"Households"})

print("Performing Transformations...")
#Define Tech Codes used in CPUC data
techcodes = {
    10: 'dsl', 11: 'dsl', 12: 'dsl', 20: 'dsl',
    40: 'cable', 41: 'cable', 42: 'cable', 43: 'cable',
    50: 'fiber',
    70: 'fixed wireless'
}

#Blacklist where retail exists
blacklist = retail_check[retail_check['Retail']==0]['Name'].tolist()

#Remove Blacklisted IPA
cpuc = cpuc[~cpuc['DBA'].isin(blacklist)]

#Add a column for Technology
cpuc['tech'] = cpuc['TechCode'].map(techcodes)

#Dataframe that contains collapsed information by Block Code
collapsed = pd.DataFrame(index = cpuc.groupby('BlockCode')['DBA'].count().index)

#Number of unique ISPs, with speeds greater than 25Mbps and 100Mbps respectively
collapsed['n_isp'] = cpuc.groupby('BlockCode')['DBA'].nunique() 
collapsed['n_bb_25'] = cpuc[(cpuc['MaxAdDn']>=25.0) & (cpuc['MaxAdUp']>=3.0)].groupby(['BlockCode'])['DBA'].nunique()
collapsed['n_bb_100'] = cpuc[(cpuc['MaxAdDn']>=100.0) & (cpuc['MaxAdUp']>=20.0)].groupby(['BlockCode'])['DBA'].nunique()

#Number of unique ISP's providing respective technologies
collapsed['n_fib'] = cpuc[cpuc['tech'] == 'fiber'].groupby(['BlockCode'])['DBA'].nunique()
collapsed['n_cab'] = cpuc[cpuc['tech'] == 'cable'].groupby(['BlockCode'])['DBA'].nunique()
collapsed['n_dsl'] = cpuc[cpuc['tech'] == 'dsl'].groupby(['BlockCode'])['DBA'].nunique()
collapsed['n_fixed_wireless'] = cpuc[cpuc['tech'] == 'fixed wireless'].groupby(['BlockCode'])['DBA'].nunique()

#Convert everything to integer
collapsed = collapsed.fillna(0)
collapsed = collapsed.astype('int64')

#Maximum Upload and Download Speed
collapsed['max_up'] = cpuc.groupby(['BlockCode'])['MaxAdUp'].max()
collapsed['max_dn'] = cpuc.groupby(['BlockCode'])['MaxAdDn'].max()

#See if specific technology exists or not
collapsed['served'] = (collapsed['n_isp'] > 0).astype('int64')
collapsed['served25'] = (collapsed['n_bb_25'] > 0).astype('int64')
collapsed['served100'] = (collapsed['n_bb_100'] > 0).astype('int64')
collapsed['served_fib'] = (collapsed['n_fib'] > 0).astype('int64')

#See if competition exists
collapsed['comp'] = (collapsed['n_isp'] > 1).astype('int64')
collapsed['comp25'] = (collapsed['n_bb_25'] > 1).astype('int64')
collapsed['comp100'] = (collapsed['n_bb_100'] > 1).astype('int64')
collapsed['comp_fib'] = (collapsed['n_fib'] > 1).astype('int64')

collapsed = collapsed.reset_index()

# #Convert Block Code to integer
# collapsed['BlockCode'] = collapsed['BlockCode'].astype('int64')

#Census Data
census = census[['BlockCode','Population']].copy()

census['BlockCode'] = '0' + census['BlockCode'].astype('str') 
census['BlockGroup'] = census['BlockCode'].str[:-3] #Define Groups for every block
census['LACounty'] = (census['BlockCode'].str[2:5] == '037').astype('int64') #If the block is in LA County or not
census['n_blocks'] = census['BlockGroup'].map(census['BlockGroup'].value_counts().to_dict()) #Number of blocks in group
census['BGPop'] = census['BlockGroup'].map(census.groupby(['BlockGroup'])['Population'].sum().to_dict()) #Block Group Population
census['shrpop10'] = census['Population']/census['BGPop'] #Population of block / Population of group

#Rename Columns
census = census.rename(columns={'Population':'POP10'})

print("Merging Datasets...")
#Merge Census and Collapsed Dataframes
collapsed = census.merge(collapsed, on='BlockCode', how='left')

#Fill NaN with 0
collapsed['n_isp'] = collapsed['n_isp'].fillna(0).astype('int64')
collapsed['n_bb_25'] = collapsed['n_bb_25'].fillna(0).astype('int64')
collapsed['n_bb_100'] = collapsed['n_bb_100'].fillna(0).astype('int64')
collapsed['n_fib'] = collapsed['n_fib'].fillna(0).astype('int64')
collapsed['n_cab'] = collapsed['n_cab'].fillna(0).astype('int64')
collapsed['n_dsl'] = collapsed['n_dsl'].fillna(0).astype('int64')
collapsed['n_fixed_wireless'] = collapsed['n_fixed_wireless'].fillna(0).astype('int64')
collapsed['served'] = collapsed['served'].fillna(0).astype('int64')
collapsed['served25'] = collapsed['served25'].fillna(0).astype('int64')
collapsed['served100'] = collapsed['served100'].fillna(0).astype('int64')
collapsed['served_fib'] = collapsed['served_fib'].fillna(0).astype('int64')
collapsed['shrpop10'] = collapsed['shrpop10'].fillna(0)

#Fill NaN with ""
collapsed['max_up'] = collapsed['max_up'].fillna("")
collapsed['max_dn'] = collapsed['max_dn'].fillna("")
collapsed['comp'] = collapsed['comp'].fillna("")
collapsed['comp25'] = collapsed['comp25'].fillna("")
collapsed['comp100'] = collapsed['comp100'].fillna("")
collapsed['comp_fib'] = collapsed['comp_fib'].fillna("")


print("Saving File...")

collapsed.to_csv(f"../Data Outputs/CPUC/BC_Collapsed_{year}.csv",index=False)

# if "Sheet1" in writer.book.sheetnames:
#     std=writer.book['Sheet1']
#     writer.book.remove(std)

# writer.save()
print(f"Finished! File saved to ../Data Outputs/CPUC/BC_Collapsed_{year}.xlsx")
