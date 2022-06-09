#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gp
import pandas as pd
import os


# In[2]:


#layers:
county = gp.read_file('../../Data Sources/Census/tl_2010_06_county10.zip').to_crs("EPSG:4326")
tract = gp.read_file('../../Data Sources/Census/tl_2010_06_tract10.zip').to_crs("EPSG:4326")
bg = gp.read_file('../../Data Sources/Census/tl_2010_06_bg10.zip').to_crs("EPSG:4326")
cd = gp.read_file('../../Data Sources/Census/tl_2010_06_cd111.zip').to_crs("EPSG:4326")
sd = gp.read_file('../../Data Sources/Census/tl_2020_06_unsd.zip').to_crs("EPSG:4326")
hs = gp.read_file('../../Data Sources/Schools/ca_schools_high.zip').to_crs("EPSG:4326")
ms = gp.read_file('../../Data Sources/Schools/ca_schools_middle.zip').to_crs("EPSG:4326")
os = gp.read_file('../../Data Sources/Schools/ca_schools_other.zip').to_crs("EPSG:4326")
ps = gp.read_file('../../Data Sources/Schools/ca_schools_primary.zip').to_crs("EPSG:4326")
ct = gp.read_file('../../Data Sources/city_boundaries.zip').to_crs("EPSG:4326")
trib = gp.read_file('../../Data Sources/tribal_boundaries.zip').to_crs("EPSG:4326")


# In[3]:


county_df = pd.DataFrame()
tract_df = pd.DataFrame()
bg_df = pd.DataFrame()
cd_df = pd.DataFrame()
sd_df = pd.DataFrame()
hs_df = pd.DataFrame()
ms_df = pd.DataFrame()
os_df = pd.DataFrame()
ps_df = pd.DataFrame()
ct_df = pd.DataFrame()
trib_df = pd.DataFrame()


# In[4]:


county_df['GEOID10'] = county['GEOID10'].sort_values().values
tract_df['GEOID10'] = tract['GEOID10'].sort_values().values
bg_df['GEOID10'] = bg['GEOID10'].sort_values().values
cd_df['GEOID10'] = cd['GEOID10'].sort_values().values
sd_df['GEOID'] = sd['GEOID'].sort_values().values
hs_df['ncessch'] = hs['ncessch'].sort_values().values
ms_df['ncessch'] = ms['ncessch'].sort_values().values
os_df['ncessch'] = os['ncessch'].sort_values().values
ps_df['ncessch'] = ps['ncessch'].sort_values().values
ct_df['GEOID10'] = ct['GEOID10'].sort_values().values
trib_df['LARID'] = trib['LARID'].sort_values().values


# In[5]:


get_ipython().run_line_magic('time', "q1 = gp.read_file('../../Data Sources/Ookla/2019/2019-01-01_performance_fixed_tiles.zip')")


# In[6]:


get_ipython().run_line_magic('time', "county_q1 =  gp.sjoin(county,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "tract_q1 =  gp.sjoin(tract,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "bg_q1 =  gp.sjoin(bg,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "cd_q1 =  gp.sjoin(cd,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "sd_q1 =  gp.sjoin(sd,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "hs_q1 =  gp.sjoin(hs,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ms_q1 =  gp.sjoin(ms,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "os_q1 =  gp.sjoin(os,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ps_q1 =  gp.sjoin(ps,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ct_q1 =  gp.sjoin(ct,q1,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "trib_q1 =  gp.sjoin(trib,q1,how = 'inner', op = 'intersects')")


# In[7]:


def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()


# In[8]:


get_ipython().run_line_magic('time', 'county_df[\'d_q1\'] = county_df[\'GEOID10\'].map(round(county_q1.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'county_df[\'u_q1\'] = county_df[\'GEOID10\'].map(round(county_q1.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'tract_df[\'d_q1\'] = tract_df[\'GEOID10\'].map(round(tract_q1.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'tract_df[\'u_q1\'] = tract_df[\'GEOID10\'].map(round(tract_q1.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'bg_df[\'d_q1\'] = bg_df[\'GEOID10\'].map(round(bg_q1.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'bg_df[\'u_q1\'] = bg_df[\'GEOID10\'].map(round(bg_q1.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'cd_df[\'d_q1\'] = cd_df[\'GEOID10\'].map(round(cd_q1.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'cd_df[\'u_q1\'] = cd_df[\'GEOID10\'].map(round(cd_q1.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'sd_df[\'d_q1\'] = sd_df[\'GEOID\'].map(round(sd_q1.groupby(\'GEOID\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'sd_df[\'u_q1\'] = sd_df[\'GEOID\'].map(round(sd_q1.groupby(\'GEOID\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'hs_df[\'d_q1\'] = hs_df[\'ncessch\'].map(round(hs_q1.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'hs_df[\'u_q1\'] = hs_df[\'ncessch\'].map(round(hs_q1.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ms_df[\'d_q1\'] = ms_df[\'ncessch\'].map(round(ms_q1.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ms_df[\'u_q1\'] = ms_df[\'ncessch\'].map(round(ms_q1.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'os_df[\'d_q1\'] = os_df[\'ncessch\'].map(round(os_q1.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'os_df[\'u_q1\'] = os_df[\'ncessch\'].map(round(os_q1.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ps_df[\'d_q1\'] = ps_df[\'ncessch\'].map(round(ps_q1.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ps_df[\'u_q1\'] = ps_df[\'ncessch\'].map(round(ps_q1.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ct_df[\'d_q1\'] = ct_df[\'GEOID10\'].map(round(ct_q1.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ct_df[\'u_q1\'] = ct_df[\'GEOID10\'].map(round(ct_q1.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'trib_df[\'d_q1\'] = trib_df[\'LARID\'].map(round(trib_q1.groupby(\'LARID\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'trib_df[\'u_q1\'] = trib_df[\'LARID\'].map(round(trib_q1.groupby(\'LARID\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')

county_df['tests_q1'] = county_df['GEOID10'].map(county_q1.groupby('GEOID10').tests.sum().to_dict())
tract_df['tests_q1'] = tract_df['GEOID10'].map(tract_q1.groupby('GEOID10').tests.sum().to_dict())
bg_df['tests_q1'] = bg_df['GEOID10'].map(bg_q1.groupby('GEOID10').tests.sum().to_dict())
cd_df['tests_q1'] = cd_df['GEOID10'].map(cd_q1.groupby('GEOID10').tests.sum().to_dict())
sd_df['tests_q1'] = sd_df['GEOID'].map(sd_q1.groupby('GEOID').tests.sum().to_dict())
hs_df['tests_q1'] = hs_df['ncessch'].map(hs_q1.groupby('ncessch').tests.sum().to_dict())
ms_df['tests_q1'] = ms_df['ncessch'].map(ms_q1.groupby('ncessch').tests.sum().to_dict())
os_df['tests_q1'] = os_df['ncessch'].map(os_q1.groupby('ncessch').tests.sum().to_dict())
ps_df['tests_q1'] = ps_df['ncessch'].map(ps_q1.groupby('ncessch').tests.sum().to_dict())
ct_df['tests_q1'] = ct_df['GEOID10'].map(ct_q1.groupby('GEOID10').tests.sum().to_dict())
trib_df['tests_q1'] = trib_df['LARID'].map(trib_q1.groupby('LARID').tests.sum().to_dict())


# In[9]:


county_df


# In[10]:


county_df


# In[11]:


# county_df = county_df.fillna(0)
# tract_df = tract_df.fillna(0)
# bg_df = bg_df.fillna(0)
# cd_df = cd_df.fillna(0)
# sd_df = sd_df.fillna(0)
# hs_df = hs_df.fillna(0)
# ms_df = ms_df.fillna(0)
# os_df = os_df.fillna(0)
# ps_df = ps_df.fillna(0)
# ct_df = ct_df.fillna(0)
# trib_df = trib_df.fillna(0)


# In[12]:


del q1


# In[13]:


del county_q1
del tract_q1
del bg_q1
del cd_q1
del sd_q1
del hs_q1
del ms_q1
del os_q1
del ps_q1
del ct_q1
del trib_q1


# In[14]:


get_ipython().run_line_magic('time', "q2 = gp.read_file('../../Data Sources/Ookla/2019/2019-04-01_performance_fixed_tiles.zip')")


# In[15]:


get_ipython().run_line_magic('time', "county_q2 =  gp.sjoin(county,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "tract_q2 =  gp.sjoin(tract,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "bg_q2 =  gp.sjoin(bg,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "cd_q2 =  gp.sjoin(cd,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "sd_q2 =  gp.sjoin(sd,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "hs_q2 =  gp.sjoin(hs,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ms_q2 =  gp.sjoin(ms,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "os_q2 =  gp.sjoin(os,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ps_q2 =  gp.sjoin(ps,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ct_q2 =  gp.sjoin(ct,q2,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "trib_q2 =  gp.sjoin(trib,q2,how = 'inner', op = 'intersects')")


# In[16]:


get_ipython().run_line_magic('time', 'county_df[\'d_q2\'] = county_df[\'GEOID10\'].map(round(county_q2.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'county_df[\'u_q2\'] = county_df[\'GEOID10\'].map(round(county_q2.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'tract_df[\'d_q2\'] = tract_df[\'GEOID10\'].map(round(tract_q2.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'tract_df[\'u_q2\'] = tract_df[\'GEOID10\'].map(round(tract_q2.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'bg_df[\'d_q2\'] = bg_df[\'GEOID10\'].map(round(bg_q2.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'bg_df[\'u_q2\'] = bg_df[\'GEOID10\'].map(round(bg_q2.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'cd_df[\'d_q2\'] = cd_df[\'GEOID10\'].map(round(cd_q2.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'cd_df[\'u_q2\'] = cd_df[\'GEOID10\'].map(round(cd_q2.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'sd_df[\'d_q2\'] = sd_df[\'GEOID\'].map(round(sd_q2.groupby(\'GEOID\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'sd_df[\'u_q2\'] = sd_df[\'GEOID\'].map(round(sd_q2.groupby(\'GEOID\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'hs_df[\'d_q2\'] = hs_df[\'ncessch\'].map(round(hs_q2.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'hs_df[\'u_q2\'] = hs_df[\'ncessch\'].map(round(hs_q2.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ms_df[\'d_q2\'] = ms_df[\'ncessch\'].map(round(ms_q2.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ms_df[\'u_q2\'] = ms_df[\'ncessch\'].map(round(ms_q2.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'os_df[\'d_q2\'] = os_df[\'ncessch\'].map(round(os_q2.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'os_df[\'u_q2\'] = os_df[\'ncessch\'].map(round(os_q2.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ps_df[\'d_q2\'] = ps_df[\'ncessch\'].map(round(ps_q2.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ps_df[\'u_q2\'] = ps_df[\'ncessch\'].map(round(ps_q2.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ct_df[\'d_q2\'] = ct_df[\'GEOID10\'].map(round(ct_q2.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ct_df[\'u_q2\'] = ct_df[\'GEOID10\'].map(round(ct_q2.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'trib_df[\'d_q2\'] = trib_df[\'LARID\'].map(round(trib_q2.groupby(\'LARID\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'trib_df[\'u_q2\'] = trib_df[\'LARID\'].map(round(trib_q2.groupby(\'LARID\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')

county_df['tests_q2'] = county_df['GEOID10'].map(county_q2.groupby('GEOID10').tests.sum().to_dict())
tract_df['tests_q2'] = tract_df['GEOID10'].map(tract_q2.groupby('GEOID10').tests.sum().to_dict())
bg_df['tests_q2'] = bg_df['GEOID10'].map(bg_q2.groupby('GEOID10').tests.sum().to_dict())
cd_df['tests_q2'] = cd_df['GEOID10'].map(cd_q2.groupby('GEOID10').tests.sum().to_dict())
sd_df['tests_q2'] = sd_df['GEOID'].map(sd_q2.groupby('GEOID').tests.sum().to_dict())
hs_df['tests_q2'] = hs_df['ncessch'].map(hs_q2.groupby('ncessch').tests.sum().to_dict())
ms_df['tests_q2'] = ms_df['ncessch'].map(ms_q2.groupby('ncessch').tests.sum().to_dict())
os_df['tests_q2'] = os_df['ncessch'].map(os_q2.groupby('ncessch').tests.sum().to_dict())
ps_df['tests_q2'] = ps_df['ncessch'].map(ps_q2.groupby('ncessch').tests.sum().to_dict())
ct_df['tests_q2'] = ct_df['GEOID10'].map(ct_q2.groupby('GEOID10').tests.sum().to_dict())
trib_df['tests_q2'] = trib_df['LARID'].map(trib_q2.groupby('LARID').tests.sum().to_dict())


# In[17]:


# county_df = county_df.fillna(0)
# tract_df = tract_df.fillna(0)
# bg_df = bg_df.fillna(0)
# cd_df = cd_df.fillna(0)
# sd_df = sd_df.fillna(0)
# hs_df = hs_df.fillna(0)
# ms_df = ms_df.fillna(0)
# os_df = os_df.fillna(0)
# ps_df = ps_df.fillna(0)
# ct_df = ct_df.fillna(0)
# trib_df = trib_df.fillna(0)


# In[18]:


del q2
del county_q2
del tract_q2
del bg_q2
del cd_q2
del sd_q2
del hs_q2
del ms_q2
del os_q2
del ps_q2
del ct_q2
del trib_q2


# In[19]:


get_ipython().run_line_magic('time', "q3 = gp.read_file('../../Data Sources/Ookla/2019/2019-07-01_performance_fixed_tiles.zip')")


# In[20]:


get_ipython().run_line_magic('time', "county_q3 =  gp.sjoin(county,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "tract_q3 =  gp.sjoin(tract,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "bg_q3 =  gp.sjoin(bg,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "cd_q3 =  gp.sjoin(cd,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "sd_q3 =  gp.sjoin(sd,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "hs_q3 =  gp.sjoin(hs,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ms_q3 =  gp.sjoin(ms,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "os_q3 =  gp.sjoin(os,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ps_q3 =  gp.sjoin(ps,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ct_q3 =  gp.sjoin(ct,q3,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "trib_q3 =  gp.sjoin(trib,q3,how = 'inner', op = 'intersects')")


# In[21]:


get_ipython().run_line_magic('time', 'county_df[\'d_q3\'] = county_df[\'GEOID10\'].map(round(county_q3.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'county_df[\'u_q3\'] = county_df[\'GEOID10\'].map(round(county_q3.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'tract_df[\'d_q3\'] = tract_df[\'GEOID10\'].map(round(tract_q3.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'tract_df[\'u_q3\'] = tract_df[\'GEOID10\'].map(round(tract_q3.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'bg_df[\'d_q3\'] = bg_df[\'GEOID10\'].map(round(bg_q3.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'bg_df[\'u_q3\'] = bg_df[\'GEOID10\'].map(round(bg_q3.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'cd_df[\'d_q3\'] = cd_df[\'GEOID10\'].map(round(cd_q3.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'cd_df[\'u_q3\'] = cd_df[\'GEOID10\'].map(round(cd_q3.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'sd_df[\'d_q3\'] = sd_df[\'GEOID\'].map(round(sd_q3.groupby(\'GEOID\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'sd_df[\'u_q3\'] = sd_df[\'GEOID\'].map(round(sd_q3.groupby(\'GEOID\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'hs_df[\'d_q3\'] = hs_df[\'ncessch\'].map(round(hs_q3.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'hs_df[\'u_q3\'] = hs_df[\'ncessch\'].map(round(hs_q3.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ms_df[\'d_q3\'] = ms_df[\'ncessch\'].map(round(ms_q3.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ms_df[\'u_q3\'] = ms_df[\'ncessch\'].map(round(ms_q3.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'os_df[\'d_q3\'] = os_df[\'ncessch\'].map(round(os_q3.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'os_df[\'u_q3\'] = os_df[\'ncessch\'].map(round(os_q3.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ps_df[\'d_q3\'] = ps_df[\'ncessch\'].map(round(ps_q3.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ps_df[\'u_q3\'] = ps_df[\'ncessch\'].map(round(ps_q3.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ct_df[\'d_q3\'] = ct_df[\'GEOID10\'].map(round(ct_q3.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ct_df[\'u_q3\'] = ct_df[\'GEOID10\'].map(round(ct_q3.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'trib_df[\'d_q3\'] = trib_df[\'LARID\'].map(round(trib_q3.groupby(\'LARID\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'trib_df[\'u_q3\'] = trib_df[\'LARID\'].map(round(trib_q3.groupby(\'LARID\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')

county_df['tests_q3'] = county_df['GEOID10'].map(county_q3.groupby('GEOID10').tests.sum().to_dict())
tract_df['tests_q3'] = tract_df['GEOID10'].map(tract_q3.groupby('GEOID10').tests.sum().to_dict())
bg_df['tests_q3'] = bg_df['GEOID10'].map(bg_q3.groupby('GEOID10').tests.sum().to_dict())
cd_df['tests_q3'] = cd_df['GEOID10'].map(cd_q3.groupby('GEOID10').tests.sum().to_dict())
sd_df['tests_q3'] = sd_df['GEOID'].map(sd_q3.groupby('GEOID').tests.sum().to_dict())
hs_df['tests_q3'] = hs_df['ncessch'].map(hs_q3.groupby('ncessch').tests.sum().to_dict())
ms_df['tests_q3'] = ms_df['ncessch'].map(ms_q3.groupby('ncessch').tests.sum().to_dict())
os_df['tests_q3'] = os_df['ncessch'].map(os_q3.groupby('ncessch').tests.sum().to_dict())
ps_df['tests_q3'] = ps_df['ncessch'].map(ps_q3.groupby('ncessch').tests.sum().to_dict())
ct_df['tests_q3'] = ct_df['GEOID10'].map(ct_q3.groupby('GEOID10').tests.sum().to_dict())
trib_df['tests_q3'] = trib_df['LARID'].map(trib_q3.groupby('LARID').tests.sum().to_dict())


# In[22]:


# county_df = county_df.fillna(0)
# tract_df = tract_df.fillna(0)
# bg_df = bg_df.fillna(0)
# cd_df = cd_df.fillna(0)
# sd_df = sd_df.fillna(0)
# hs_df = hs_df.fillna(0)
# ms_df = ms_df.fillna(0)
# os_df = os_df.fillna(0)
# ps_df = ps_df.fillna(0)
# ct_df = ct_df.fillna(0)
# trib_df = trib_df.fillna(0)


# In[23]:


del q3
del county_q3
del tract_q3
del bg_q3
del cd_q3
del sd_q3
del hs_q3
del ms_q3
del os_q3
del ps_q3
del ct_q3
del trib_q3


# In[24]:


get_ipython().run_line_magic('time', "q4 = gp.read_file('../../Data Sources/Ookla/2019/2019-10-01_performance_fixed_tiles.zip')")


# In[25]:


get_ipython().run_line_magic('time', "county_q4 =  gp.sjoin(county,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "tract_q4 =  gp.sjoin(tract,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "bg_q4 =  gp.sjoin(bg,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "cd_q4 =  gp.sjoin(cd,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "sd_q4 =  gp.sjoin(sd,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "hs_q4 =  gp.sjoin(hs,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ms_q4 =  gp.sjoin(ms,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "os_q4 =  gp.sjoin(os,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ps_q4 =  gp.sjoin(ps,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "ct_q4 =  gp.sjoin(ct,q4,how = 'inner', op = 'intersects')")
get_ipython().run_line_magic('time', "trib_q4 =  gp.sjoin(trib,q4,how = 'inner', op = 'intersects')")


# In[26]:


get_ipython().run_line_magic('time', 'county_df[\'d_q4\'] = county_df[\'GEOID10\'].map(round(county_q4.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'county_df[\'u_q4\'] = county_df[\'GEOID10\'].map(round(county_q4.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'tract_df[\'d_q4\'] = tract_df[\'GEOID10\'].map(round(tract_q4.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'tract_df[\'u_q4\'] = tract_df[\'GEOID10\'].map(round(tract_q4.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'bg_df[\'d_q4\'] = bg_df[\'GEOID10\'].map(round(bg_q4.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'bg_df[\'u_q4\'] = bg_df[\'GEOID10\'].map(round(bg_q4.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'cd_df[\'d_q4\'] = cd_df[\'GEOID10\'].map(round(cd_q4.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'cd_df[\'u_q4\'] = cd_df[\'GEOID10\'].map(round(cd_q4.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'sd_df[\'d_q4\'] = sd_df[\'GEOID\'].map(round(sd_q4.groupby(\'GEOID\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'sd_df[\'u_q4\'] = sd_df[\'GEOID\'].map(round(sd_q4.groupby(\'GEOID\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'hs_df[\'d_q4\'] = hs_df[\'ncessch\'].map(round(hs_q4.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'hs_df[\'u_q4\'] = hs_df[\'ncessch\'].map(round(hs_q4.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ms_df[\'d_q4\'] = ms_df[\'ncessch\'].map(round(ms_q4.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ms_df[\'u_q4\'] = ms_df[\'ncessch\'].map(round(ms_q4.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'os_df[\'d_q4\'] = os_df[\'ncessch\'].map(round(os_q4.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'os_df[\'u_q4\'] = os_df[\'ncessch\'].map(round(os_q4.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ps_df[\'d_q4\'] = ps_df[\'ncessch\'].map(round(ps_q4.groupby(\'ncessch\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ps_df[\'u_q4\'] = ps_df[\'ncessch\'].map(round(ps_q4.groupby(\'ncessch\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ct_df[\'d_q4\'] = ct_df[\'GEOID10\'].map(round(ct_q4.groupby(\'GEOID10\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'ct_df[\'u_q4\'] = ct_df[\'GEOID10\'].map(round(ct_q4.groupby(\'GEOID10\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'trib_df[\'d_q4\'] = trib_df[\'LARID\'].map(round(trib_q4.groupby(\'LARID\').apply(w_avg, "avg_d_kbps", "tests")/1024,3).to_dict())')
get_ipython().run_line_magic('time', 'trib_df[\'u_q4\'] = trib_df[\'LARID\'].map(round(trib_q4.groupby(\'LARID\').apply(w_avg, "avg_u_kbps", "tests")/1024,3).to_dict())')

county_df['tests_q4'] = county_df['GEOID10'].map(county_q4.groupby('GEOID10').tests.sum().to_dict())
tract_df['tests_q4'] = tract_df['GEOID10'].map(tract_q4.groupby('GEOID10').tests.sum().to_dict())
bg_df['tests_q4'] = bg_df['GEOID10'].map(bg_q4.groupby('GEOID10').tests.sum().to_dict())
cd_df['tests_q4'] = cd_df['GEOID10'].map(cd_q4.groupby('GEOID10').tests.sum().to_dict())
sd_df['tests_q4'] = sd_df['GEOID'].map(sd_q4.groupby('GEOID').tests.sum().to_dict())
hs_df['tests_q4'] = hs_df['ncessch'].map(hs_q4.groupby('ncessch').tests.sum().to_dict())
ms_df['tests_q4'] = ms_df['ncessch'].map(ms_q4.groupby('ncessch').tests.sum().to_dict())
os_df['tests_q4'] = os_df['ncessch'].map(os_q4.groupby('ncessch').tests.sum().to_dict())
ps_df['tests_q4'] = ps_df['ncessch'].map(ps_q4.groupby('ncessch').tests.sum().to_dict())
ct_df['tests_q4'] = ct_df['GEOID10'].map(ct_q4.groupby('GEOID10').tests.sum().to_dict())
trib_df['tests_q4'] = trib_df['LARID'].map(trib_q4.groupby('LARID').tests.sum().to_dict())


# In[27]:


# county_df = county_df.fillna(0)
# tract_df = tract_df.fillna(0)
# bg_df = bg_df.fillna(0)
# cd_df = cd_df.fillna(0)
# sd_df = sd_df.fillna(0)
# hs_df = hs_df.fillna(0)
# ms_df = ms_df.fillna(0)
# os_df = os_df.fillna(0)
# ps_df = ps_df.fillna(0)
# ct_df = ct_df.fillna(0)
# trib_df = trib_df.fillna(0)


# In[28]:


county_df


# In[29]:


county_df


# In[ ]:





# In[30]:


county_df['avg_d'] = county_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
county_df['avg_u'] = county_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
tract_df['avg_d'] = tract_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
tract_df['avg_u'] = tract_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
bg_df['avg_d'] = bg_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
bg_df['avg_u'] = bg_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
cd_df['avg_d'] = cd_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
cd_df['avg_u'] = cd_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
sd_df['avg_d'] = sd_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
sd_df['avg_u'] = sd_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
hs_df['avg_d'] = hs_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
hs_df['avg_u'] = hs_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
ms_df['avg_d'] = ms_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
ms_df['avg_u'] = ms_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
os_df['avg_d'] = os_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
os_df['avg_u'] = os_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
ps_df['avg_d'] = ps_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
ps_df['avg_u'] = ps_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
ct_df['avg_d'] = ct_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
ct_df['avg_u'] = ct_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)
trib_df['avg_d'] = trib_df[['d_q1','d_q2','d_q3','d_q4']].mean(axis=1)
trib_df['avg_u'] = trib_df[['u_q1','u_q2','u_q3','u_q4']].mean(axis=1)


county_df['total_tests'] = county_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
tract_df['total_tests'] = tract_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
bg_df['total_tests'] = bg_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
cd_df['total_tests'] = cd_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
sd_df['total_tests'] = sd_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
hs_df['total_tests'] = hs_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
ms_df['total_tests'] = ms_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
os_df['total_tests'] = os_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
ps_df['total_tests'] = ps_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
ct_df['total_tests'] = ct_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)
trib_df['total_tests'] = trib_df[['tests_q1','tests_q2','tests_q3','tests_q4']].sum(axis=1)


# In[31]:


import pickle


# In[32]:


pickle.dump(county_df, open("ookla_files/county_df.p","wb"))
pickle.dump(tract_df, open("ookla_files/tract_df.p","wb"))
pickle.dump(bg_df, open("ookla_files/bg_df.p","wb"))
pickle.dump(cd_df, open("ookla_files/cd_df.p","wb"))
pickle.dump(sd_df, open("ookla_files/sd_df.p","wb"))
pickle.dump(hs_df, open("ookla_files/hs_df.p","wb"))
pickle.dump(ms_df, open("ookla_files/ms_df.p","wb"))
pickle.dump(os_df, open("ookla_files/os_df.p","wb"))
pickle.dump(ps_df, open("ookla_files/ps_df.p","wb"))
pickle.dump(ct_df, open("ookla_files/ct_df.p","wb"))
pickle.dump(trib_df, open("ookla_files/trib_df.p","wb"))


# In[31]:


county_df_final = county_df[['GEOID10','avg_d','avg_u','total_tests']]
tract_df_final = tract_df[['GEOID10','avg_d','avg_u','total_tests']]
bg_df_final = bg_df[['GEOID10','avg_d','avg_u','total_tests']]
cd_df_final = cd_df[['GEOID10','avg_d','avg_u','total_tests']]
sd_df_final = sd_df[['GEOID','avg_d','avg_u','total_tests']]
hs_df_final = hs_df[['ncessch','avg_d','avg_u','total_tests']]
ms_df_final = ms_df[['ncessch','avg_d','avg_u','total_tests']]
os_df_final = os_df[['ncessch','avg_d','avg_u','total_tests']]
ps_df_final = ps_df[['ncessch','avg_d','avg_u','total_tests']]
ct_df_final = ct_df[['GEOID10','avg_d','avg_u','total_tests']]
trib_df_final = trib_df[['LARID','avg_d','avg_u','total_tests']]


# In[44]:


tract_df_final[tract_df_final['total_tests'] < 100].count()


# In[52]:


bg_df_final[bg_df_final['total_tests'] < 100].count()


# In[47]:


hs_df_final[hs_df_final['total_tests'] < 100].count()


# In[48]:


ps_df_final[ps_df_final['total_tests'] < 100].count()


# In[49]:


ct_df_final[ct_df_final['total_tests'] < 100].count()


# In[50]:


cd_df_final[cd_df_final['total_tests'] < 100].count()


# In[ ]:





# In[ ]:





# In[ ]:





# In[32]:


pd.DataFrame().to_excel("Ookla_Data.xlsx")


# In[33]:


writer = pd.ExcelWriter("Ookla_Data.xlsx", engine = 'xlsxwriter')


# In[34]:


county_df_final.to_excel(writer, sheet_name='County_2019_ookla', index=False)
tract_df_final.to_excel(writer, sheet_name='Tract_2019_ookla', index=False)
bg_df_final.to_excel(writer, sheet_name='BG_2019_ookla', index=False)
cd_df_final.to_excel(writer, sheet_name='CD_2019_ookla', index=False)
sd_df_final.to_excel(writer, sheet_name='SD_2019_ookla', index=False)
hs_df_final.to_excel(writer, sheet_name='HS_2019_ookla', index=False)
ms_df_final.to_excel(writer, sheet_name='MS_2019_ookla', index=False)
os_df_final.to_excel(writer, sheet_name='OS_2019_ookla', index=False)
ps_df_final.to_excel(writer, sheet_name='PS_2019_ookla', index=False)
ct_df_final.to_excel(writer, sheet_name='CT_2019_ookla', index=False)
trib_df_final.to_excel(writer, sheet_name='Trib_2019_ookla', index=False)


# In[35]:


writer.save()
writer.close()


# In[109]:


bg_df_final


# In[110]:


county_df


# In[111]:


q4


# In[112]:


q4['tests'].hist()


# In[1]:


from os import path


# In[13]:


path.exists("../../Data Outputs/CPUC/BC_Collapsed.xlsx")


# In[ ]:




