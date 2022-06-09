#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gp
import pandas as pd
import numpy as np


# In[2]:


import pickle as pkl


# In[97]:


def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()


# In[98]:


year = '2020'


# In[99]:


a = pd.read_stata(f'ACS_{year}.dta')
a['bg'] = a['id'].str[9:]
a= a[['bg','broadband_any','broadband_fixed']]
a


# In[100]:


a = pd.read_csv('broadband_adoption_2020.csv')
a['bg'] = a['id'].str[9:]
a = a[['bg','broadband_any','broadband_fixed']]
a


# In[101]:


citybgs = pkl.load(open('finalbglist20.p', 'rb'))


# In[102]:


ct = gp.read_file('zip://../Data Sources/Census/Combined/City Boundaries.zip!city_boundaries20.shp')
bg = gp.read_file('../Data Sources/Census/tl_2020_06_bg20.zip')
bgdata = pd.read_excel('../Data Outputs/CPUC/BG_Collapsed.xlsx', sheet_name=f'bg_{year}')


# In[103]:


bgdata['BlockGroup'] = '0' + bgdata['BlockGroup'].astype('str')


# In[104]:


bgpop = bgdata.set_index('BlockGroup').to_dict()['BGPop']


# In[105]:


bg = bg[bg['GEOID20'].isin(citybgs)]


# In[106]:


bg


# In[107]:


banymap = a.set_index('bg').to_dict()['broadband_any']
bfixmap = a.set_index('bg').to_dict()['broadband_fixed']


# In[108]:


bg['broadband_any'] = bg['GEOID20'].map(banymap)
bg['broadband_fixed'] = bg['GEOID20'].map(bfixmap)
bg['bgpop'] = bg['GEOID20'].map(bgpop)


# In[116]:


bg[bg['GEOID20'] == '060350404002']


# In[117]:


a[a['bg'] == '060350404002']


# In[110]:


ctjoin = gp.sjoin(ct,bg)


# In[111]:


ctjoin


# In[112]:


ctjoin = ctjoin.rename(columns={"GEOID20_left": "city", "GEOID20_right": "bg"})
ctjoin = ctjoin[['city', 'bg','broadband_any','broadband_fixed','bgpop']]
ctjoin


# In[113]:


ctjoin[ctjoin.broadband_any.isnull()]


# In[118]:


ctjoin.groupby('city').apply(w_avg,'broadband_any','bgpop')


# In[119]:


adop_ct = pd.DataFrame()
adop_ct['city'] = sorted(ctjoin['city'].unique().tolist())


# In[120]:


adop_ct['broadband_any'] = adop_ct.city.map(ctjoin.groupby('city').apply(w_avg,'broadband_any','bgpop').to_dict())
adop_ct['broadband_fixed'] = adop_ct.city.map(ctjoin.groupby('city').apply(w_avg,'broadband_fixed','bgpop').to_dict())
adop_ct['ctpopadop'] = adop_ct.city.map(ctjoin.groupby('city').bgpop.sum().to_dict())


# In[121]:


adop_ct


# In[122]:


writer = pd.ExcelWriter(f"ct_adop_{year}.xlsx", engine = 'xlsxwriter')
round(adop_ct,3).to_excel(writer, sheet_name=f'ct_adop_{year}', index=False)
writer.save()
writer.close()


# In[ ]:




