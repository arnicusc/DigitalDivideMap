import geopandas as gp      #GIS data
import pandas as pd         #Dataframes
import argparse
import zipfile
import os

parser = argparse.ArgumentParser(description='Year')
parser.add_argument('--year', default='2019',help="Year for which script should run")
args = parser.parse_known_args()[0]
year = args.year

try:
    print('Reading Data...')
    cpuc_zipfile = "zip://../Data Sources/CPUC/CPUC_"+year+".zip!Fixed_Consumer_Deployment_2021.shp" #CPUC Broadband Data
    cpuc = gp.read_file(cpuc_zipfile) #Read CPUC file
except:
    raise Exception("File is already split or not valid!")

fixed_wireless = cpuc[cpuc['TechCode']==70]
wireline = cpuc[cpuc['TechCode']!=70]

directory = "../Data Sources/CPUC/"
print("Saving Fixed Wireless Data...")
fixed_wireless.to_file(directory + 'Fixed_Wireless_BB_Consumer.shp', driver='ESRI Shapefile')
print("Saving Wireline Data...")
wireline.to_file(directory + 'Wireline_BB_Consumer.shp', driver='ESRI Shapefile')

os.remove(directory + 'Fixed_Wireless_BB_Consumer.cpg')
os.remove(directory + 'Wireline_BB_Consumer.cpg')

exts = ['.dbf','.shp','.shx','.prj']
fixed_wireless_files = []
wireline_files = []

for e in exts:
    fixed_wireless_files.append('Fixed_Wireless_BB_Consumer' + e)
    wireline_files.append('Wireline_BB_Consumer' + e)

os.remove(directory + f'CPUC_{year}.zip')

os.chdir(directory)

print("Creating Zip File...")
with zipfile.ZipFile(f'CPUC_{year}.zip','w') as z:
    for f in fixed_wireless_files:
        z.write(f, compress_type=zipfile.ZIP_DEFLATED)
    for f in wireline_files:
        z.write(f, compress_type=zipfile.ZIP_DEFLATED)

print("Cleaning...")
for f in fixed_wireless_files:
    os.remove(f)
for f in wireline_files:
    os.remove(f)

print("Finished!")



    