import streamlit as st
import pandas as pd
import numpy as np
import os
import openpyxl

layerlist = ['County', 'Tracts', 'Block Groups','Congressional Districts', \
             'Cities and Towns', 'Tribal Communities', 'School Districts']

variablelist = ['CPUC Variables', 'Ookla','Adoption']

filemap = {
    "County": "County",
    "Tracts": "Tract",
    "Block Groups": "BG",
    "Congressional Districts": "CD",
    "Cities and Towns": "CT",
    "Tribal Communities": "Tri",
    "School Districts" : "SD"
}
sheetmap = {
    "County": "county",
    "Tracts": "tr",
    "Block Groups": "bg",
    "Congressional Districts": "cd",
    "Cities and Towns": "ct",
    "Tribal Communities": "tri",
    "School Districts" : "sd"
}

year = st.sidebar.selectbox("Select Year:", ['2020','2019','2018'])
layer = st.sidebar.selectbox("Select Layer:", layerlist)

if year == '2018':
    variablelist = [x for x in variablelist if x!="Ookla"]
if layer == 'Tribal Communities':
    variablelist = [x for x in variablelist if x!="Adoption"]

container = st.sidebar.container()
alllayer = st.sidebar.checkbox("Select All")

if alllayer:
    variables = container.multiselect("Select Variable:",variablelist, variablelist)
else:
    variables = container.multiselect("Select Variable:",variablelist)

final = pd.DataFrame()

for v in variables:
    if v=='CPUC Variables':
        cpucdata = pd.read_excel(f"Script Outputs/CPUC/{filemap[layer]}_Collapsed.xlsx", sheet_name=f"{sheetmap[layer]}_{year}")
        
        if final.empty:
            final = final.append(cpucdata)
        else:
            final = pd.concat([final,cpucdata], axis=1)
    if v =='Ookla':
        if year == '2020':
            ookladata = pd.read_excel("Script Outputs/ookla2020.xlsx", sheet_name=f"{filemap[layer]}_2020_ookla")
        else:
            ookladata = pd.read_excel("Script Outputs/Ookla_Data.xlsx", sheet_name=f"{filemap[layer]}_2019_ookla")
        
        if final.empty:
            final = final.append(ookladata)
        else:
            final = pd.concat([final,ookladata], axis=1)

    if v=='Adoption':
        if layer == 'School Districts':
            adopdata = pd.read_excel("Script Outputs/sd_adop.xlsx", sheet_name=f"{sheetmap[layer]}_adop_{year}")
        elif layer == 'Cities and Towns':
            adopdata = pd.read_excel("Script Outputs/Adoption_City.xlsx", sheet_name=f"{sheetmap[layer]}_adop_{year}")
        else:
            adopdata = pd.read_excel(f"Script Outputs/adoption_data_{year}.xlsx", sheet_name=f"{sheetmap[layer]}_adop_{year}")

        adopdata = adopdata.sort_values(by = adopdata.columns[0])

        if final.empty:
            final = final.append(adopdata)
        else:
            final = pd.concat([final, adopdata], axis=1)

final = final.loc[:,~final.columns.duplicated()].copy()
final = final.T.drop_duplicates().T

if len(variables)>0:
    st.dataframe(final, 1200, 500)

    suffix = '_'.join(variables)

    st.download_button("Download CSV", data=final.to_csv(), file_name=f"{layer}_{year}_{suffix}.csv")


