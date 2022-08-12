import streamlit as st
import pandas as pd
import numpy as np
import os
import openpyxl

layerlist = ['County', 'Tracts', 'Block Groups','Congressional Districts', \
             'Cities and Towns', 'Tribal Communities', 'School Districts']

variablelist = ['Deployment Indicators','Service Quality Indicators','Adoption Indicators']

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
    if v=='Deployment Indicators':
        cpucdata = pd.read_excel(f"Script Outputs/CPUC/{filemap[layer]}_Collapsed.xlsx", sheet_name=f"{sheetmap[layer]}_{year}")
        cpucdata = cpucdata.iloc[:,:-2]
        if final.empty:
            final = final.append(cpucdata)
        else:
            final = pd.concat([final,cpucdata], axis=1)

    if v =='Service Quality Indicators':
        if year == '2020':
            cpucdata = pd.read_excel(f"Script Outputs/CPUC/{filemap[layer]}_Collapsed.xlsx", sheet_name=f"{sheetmap[layer]}_{year}")
            cpucdata = cpucdata = pd.concat([cpucdata.iloc[:,0],cpucdata.iloc[:,-2:]],axis=1)
            ookladata = pd.read_excel("Script Outputs/ookla2020.xlsx", sheet_name=f"{filemap[layer]}_2020_ookla")
            ookladata = ookladata.merge(cpucdata, left_on=ookladata.columns[0], right_on=cpucdata.columns[0])
            ookladata = ookladata.rename(columns={'avg_d':'ookla down','avg_u':'ookla up','total_tests':'ookla tests',\
                                     'avg_max_up':"adv up",'avg_max_dn':"adv down"})
        elif year == '2019':
            cpucdata = pd.read_excel(f"Script Outputs/CPUC/{filemap[layer]}_Collapsed.xlsx", sheet_name=f"{sheetmap[layer]}_{year}")
            cpucdata = cpucdata = pd.concat([cpucdata.iloc[:,0],cpucdata.iloc[:,-2:]],axis=1)
            ookladata = pd.read_excel("Script Outputs/Ookla_Data.xlsx", sheet_name=f"{filemap[layer]}_2019_ookla")
            ookladata = ookladata.merge(cpucdata, left_on=ookladata.columns[0], right_on=cpucdata.columns[0])
            ookladata = ookladata.rename(columns={'avg_d':'ookla down','avg_u':'ookla up','total_tests':'ookla tests',\
                                     'avg_max_up':"adv up",'avg_max_dn':"adv down"})
            
        else:
            cpucdata = pd.read_excel(f"Script Outputs/CPUC/{filemap[layer]}_Collapsed.xlsx", sheet_name=f"{sheetmap[layer]}_{year}")
            cpucdata = pd.concat([cpucdata.iloc[:,0],cpucdata.iloc[:,-2:]],axis=1)
            ookladata = cpucdata.rename(columns={'avg_max_up':"adv up",'avg_max_dn':"adv down"})
        
        if final.empty:
            final = final.append(ookladata)
        else:
            final = pd.concat([final,ookladata], axis=1)

    if v=='Adoption Indicators':
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


final = final.round(1)
final = final.loc[:,~final.columns.duplicated()].copy()
final = final.T.drop_duplicates().T


if len(variables)>0:
    # final[final.columns[0]] = final[final.columns[0]].astype('str')
    st.dataframe(final.style.format(lambda x : '{:.1f}'.format(x)), 1200, 500)

    suffix = '_'.join(variables)

    st.download_button("Download CSV", data=final.to_csv(), file_name=f"{layer}_{year}_{suffix}.csv")


