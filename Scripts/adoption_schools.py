#!/usr/bin/env python
# coding: utf-8

# In[44]:


import geopandas as gp
import pandas as pd
import numpy as np
year=2020


# In[45]:


def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()


# In[46]:


bgdata = pd.read_excel('../Data Outputs/CPUC/BG_Collapsed.xlsx', sheet_name=f'bg_{year}')
sddata = pd.read_excel('../Data Outputs/CPUC/SD_Collapsed.xlsx', sheet_name=f'sd_{year}')


# In[47]:


if int(year) >= 2020:
    bg = gp.read_file('../Data Sources/Census/tl_2020_06_bg20.zip')
else:
    bg = gp.read_file('../Data Sources/Census/tl_2010_06_bg10.zip')

sd = gp.read_file('../Data Sources/Census/tl_2020_06_unsd.zip')

sd_bg = gp.sjoin(sd,bg, how = 'inner', op = 'intersects')

if int(year) >= 2020:
    sd_bg = sd_bg.rename(columns={'GEOID':'SD','GEOID20':'BlockGroup'})
else:
    sd_bg = sd_bg.rename(columns={'GEOID':'SD','GEOID10':'BlockGroup'})

sd_bg = sd_bg[['SD','BlockGroup']]
sd_bg = sd_bg.loc[:,~sd_bg.columns.duplicated()]
sd_bg = sd_bg.set_index('BlockGroup').squeeze()


# In[49]:


a = pd.read_csv('broadband_adoption_2020.csv')
a['bg'] = a['id'].str[9:]
a = a[['bg','broadband_any','broadband_fixed']]
a


# In[50]:


sdbgmap = sd_bg.to_dict()
a['sd'] = a['bg'].map(sdbgmap)
a['bgpop'] = bgdata['BGPop']


# In[51]:


a


# In[52]:


adop_sd = pd.DataFrame()
adop_sd['sd'] = '0' + sddata['SD'].astype('str')
adop_sd['sdpopadop'] = sddata['SDPop']


# In[53]:


adop_sd['broadband_any'] = adop_sd.sd.map(a.groupby('sd').apply(w_avg,'broadband_any','bgpop').to_dict())
adop_sd['broadband_fixed'] =  adop_sd.sd.map(a.groupby('sd').apply(w_avg,'broadband_fixed','bgpop').to_dict())


# In[54]:


adop_sd


# In[55]:


adop_sd.to_excel(f'sd_adop_{year}.xlsx', sheet_name=f'sd_adop_{year}', index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




