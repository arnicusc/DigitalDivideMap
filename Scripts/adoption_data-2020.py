#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gp
import pandas as pd
import numpy as np


# In[2]:


def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()


# In[3]:


year = '2020'


# In[4]:


a = pd.read_csv('broadband_adoption_2020.csv')
a['bg'] = a['id'].str[9:]
a = a[['bg','broadband_any','broadband_fixed']]
a


# In[6]:


a[a['bg'] == '060350404002']


# In[7]:


bgdata = pd.read_excel('../Data Outputs/CPUC/BG_Collapsed.xlsx', sheet_name=f'bg_{year}')
trdata = pd.read_excel('../Data Outputs/CPUC/Tract_Collapsed.xlsx', sheet_name=f'tr_{year}')
countydata = pd.read_excel('../Data Outputs/CPUC/County_Collapsed.xlsx', sheet_name=f'county_{year}')
cddata = pd.read_excel('../Data Outputs/CPUC/CD_Collapsed.xlsx', sheet_name=f'cd_{year}')


# In[8]:


a['bgpop'] = bgdata['BGPop']
a['tract'] = a['bg'].str[:-1]
a['county'] = a['bg'].str[:5]
a


# In[9]:


adop_tr = pd.DataFrame()
adop_tr['tract'] = '0' + trdata['Tract'].astype('str')
adop_tr['trpopadop'] = trdata['TractPop']
adop_county = pd.DataFrame()
adop_county['county'] = '0' + countydata['County'].astype('str')
adop_county['countypopadop'] = countydata['CountyPop']
adop_bg = pd.DataFrame()
adop_bg['bg'] = a['bg']
adop_bg['bgpopadop'] = a['bgpop']


# In[10]:


adop_tr['broadband_any'] = adop_tr.tract.map(a.groupby('tract').apply(w_avg,'broadband_any','bgpop').to_dict())
adop_tr['broadband_fixed'] =  adop_tr.tract.map(a.groupby('tract').apply(w_avg,'broadband_fixed','bgpop').to_dict())

adop_county['broadband_any'] = adop_county.county.map(a.groupby('county').apply(w_avg,'broadband_any','bgpop').to_dict())
adop_county['broadband_fixed'] =  adop_county.county.map(a.groupby('county').apply(w_avg,'broadband_fixed','bgpop').to_dict())

adop_bg['broadband_any'] = a.broadband_any
adop_bg['broadband_fixed'] = a.broadband_fixed


# In[11]:


adop_tr


# In[12]:


adop_county


# In[13]:


adop_bg


# In[ ]:





# In[ ]:





# In[ ]:





# In[14]:


cd20 = gp.read_file('../Data Sources/Census/tl_2020_06_cd113.zip')
bg20 = gp.read_file('../Data Sources/Census/tl_2020_06_bg20.zip')


# In[15]:


cdbgmap = gp.sjoin(bg20,cd20)[['GEOID20','GEOID10',]].rename(columns={'GEOID20':'bg','GEOID10':'cd'})


# In[16]:


cdbgmap = cdbgmap.set_index('bg').to_dict()['cd']


# In[17]:


a['cd'] = a['bg'].map(cdbgmap)


# In[18]:


adop_cd = pd.DataFrame()
adop_cd['cd'] = '0' + cddata['CD'].astype('str')
adop_cd['cdpopadop'] = cddata['CDPop']


# In[19]:


adop_cd['broadband_any'] = adop_cd.cd.map(a.groupby('cd').apply(w_avg,'broadband_any','bgpop').to_dict())
adop_cd['broadband_fixed'] =  adop_cd.cd.map(a.groupby('cd').apply(w_avg,'broadband_fixed','bgpop').to_dict())


# In[20]:


adop_cd


# In[21]:


writer = pd.ExcelWriter(f"adoption_data_{year}.xlsx", engine = 'xlsxwriter')


# In[22]:


round(adop_bg,3).to_excel(writer, sheet_name=f'bg_adop_{year}', index=False)
round(adop_tr,3).to_excel(writer, sheet_name=f'tr_adop_{year}', index=False)
round(adop_county,3).to_excel(writer, sheet_name=f'county_adop_{year}', index=False)
round(adop_cd,3).to_excel(writer, sheet_name=f'cd_adop_{year}', index=False)


# In[23]:


writer.save()
writer.close()


# In[ ]:




