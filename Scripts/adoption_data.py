#!/usr/bin/env python
# coding: utf-8

# In[2]:


import geopandas as gp
import pandas as pd
import numpy as np


# In[3]:


def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()


# In[25]:


year = '2019'


# In[26]:


a = pd.read_stata(f'ACS_{year}.dta')
a['bg'] = a['id'].str[9:]
a= a[['bg','broadband_any','broadband_fixed']]
a


# In[27]:


bgdata = pd.read_excel('../Data Outputs/CPUC/BG_Collapsed.xlsx', sheet_name=f'bg_{year}')
trdata = pd.read_excel('../Data Outputs/CPUC/Tract_Collapsed.xlsx', sheet_name=f'tr_{year}')
countydata = pd.read_excel('../Data Outputs/CPUC/County_Collapsed.xlsx', sheet_name=f'county_{year}')
cddata = pd.read_excel('../Data Outputs/CPUC/CD_Collapsed.xlsx', sheet_name=f'cd_{year}')


# In[28]:


a['bgpop'] = bgdata['BGPop']
a['tract'] = a['bg'].str[:-1]
a['county'] = a['bg'].str[:5]
a


# In[29]:


countydata


# In[30]:


adop_tr = pd.DataFrame()
adop_tr['tract'] = '0' + trdata['Tract'].astype('str')
adop_tr['trpopadop'] = trdata['TractPop']
adop_county = pd.DataFrame()
adop_county['county'] = '0' + countydata['County'].astype('str')
adop_county['countypopadop'] = countydata['CountyPop']
adop_bg = pd.DataFrame()
adop_bg['bg'] = a['bg']
adop_bg['bgpopadop'] = a['bgpop']


# In[31]:


adop_tr['broadband_any'] = adop_tr.tract.map(a.groupby('tract').apply(w_avg,'broadband_any','bgpop').to_dict())
adop_tr['broadband_fixed'] =  adop_tr.tract.map(a.groupby('tract').apply(w_avg,'broadband_fixed','bgpop').to_dict())

adop_county['broadband_any'] = adop_county.county.map(a.groupby('county').apply(w_avg,'broadband_any','bgpop').to_dict())
adop_county['broadband_fixed'] =  adop_county.county.map(a.groupby('county').apply(w_avg,'broadband_fixed','bgpop').to_dict())

adop_bg['broadband_any'] = a.broadband_any
adop_bg['broadband_fixed'] = a.broadband_fixed


# In[32]:


adop_tr


# In[33]:


adop_county


# In[34]:


adop_bg


# In[ ]:





# In[ ]:





# In[ ]:





# In[35]:


cd10 = gp.read_file('../Data Sources/Census/tl_2010_06_cd111.zip')
bg10 = gp.read_file('../Data Sources/Census/tl_2010_06_bg10.zip')


# In[36]:


cdbgmap = gp.sjoin(bg10,cd10)[['GEOID10_left','GEOID10_right',]].rename(columns={'GEOID10_left':'bg','GEOID10_right':'cd'})


# In[37]:


cdbgmap = cdbgmap.set_index('bg').to_dict()['cd']


# In[38]:


a['cd'] = a['bg'].map(cdbgmap)


# In[39]:


adop_cd = pd.DataFrame()
adop_cd['cd'] = '0' + cddata['CD'].astype('str')
adop_cd['cdpopadop'] = cddata['CDPop']


# In[40]:


adop_cd['broadband_any'] = adop_cd.cd.map(a.groupby('cd').apply(w_avg,'broadband_any','bgpop').to_dict())
adop_cd['broadband_fixed'] =  adop_cd.cd.map(a.groupby('cd').apply(w_avg,'broadband_fixed','bgpop').to_dict())


# In[41]:


adop_cd


# In[42]:


writer = pd.ExcelWriter(f"adoption_data_{year}.xlsx", engine = 'xlsxwriter')


# In[43]:


round(adop_bg,3).to_excel(writer, sheet_name=f'bg_adop_{year}', index=False)
round(adop_tr,3).to_excel(writer, sheet_name=f'tr_adop_{year}', index=False)
round(adop_county,3).to_excel(writer, sheet_name=f'county_adop_{year}', index=False)
round(adop_cd,3).to_excel(writer, sheet_name=f'cd_adop_{year}', index=False)


# In[44]:


writer.save()
writer.close()


# In[ ]:




