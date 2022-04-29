#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt 


# In[2]:


date = pd.to_datetime("today").strftime('_%m_%d')
print('Latest update time is:',date)


# In[3]:

states = pd.read_csv("https://prsindia.org/covid-19/cases/download")
#states = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv")
#print(states)
states=states[states["Date"].str.contains("202")]
#print(states)
#states = pd.read_csv("https://prsindia.org/covid-19/cases/download")
# change column names to lowercase
states.columns= states.columns.str.lower()
#01/01/1970
# convert date column
#states['date'] = pd.to_datetime(states['date'], format= '%Y-%m-%d')
states['date'] = pd.to_datetime(states['date'], format= '%d/%m/%Y')
print(states['date'].unique())
#states0=states.copy()
#print(states[states["region"]=="Kerala"])
states[states["region"]=="Assam"]["confirmed cases"].diff().plot()
print(states[states["region"]=="Assam"]["confirmed cases"])
#plt.show()
# In[4]:
do_not_include = ['India','State assignment pending','World']


# In[5]:
states


# In[6]:


# NOTE: 
# The data set appears to add entries for the most recent date then fill in information as it comes in, 
# meaning a state will appear to have zero new cases for the most recent day until it gets updated.

# filter out most recent date to avoid potentially incomplete information
#states = states[~(states['date'] == states['date'].max())]

# dataset doesn't include every date before 2020-03-02 
# (1 new case in Kerala on 1/30, 2/2 & 2/3; all 3 recovered 2/14)
# filter out those dates
#states = states[states['date'] > '2020-03-01']


# In[7]:


states


# In[8]:


## Adding in missing dates for Kerala

# create an array of 2 dates starting at '2020-01-31', one per day
rng = pd.date_range('2020-01-31', periods=2, freq='D')
df1 = pd.DataFrame({ 'date': rng, 'state' : 'Kerala', 'confirmed' : 1, 'recovered' : 0, 'deceased' : 0, 'other': 0})

# create an array of 10 dates starting at '2020-02-04', one per day
rng = pd.date_range('2020-02-04', periods=10, freq='D')
df2 = pd.DataFrame({ 'date': rng, 'state' : 'Kerala', 'confirmed' : 3, 'recovered' : 0, 'deceased' : 0, 'other': 0})

# create an array of 16 dates starting at '2020-02-24', one per day
rng = pd.date_range('2020-02-15', periods=16, freq='D')
df3 = pd.DataFrame({ 'date': rng, 'state' : 'Kerala', 'confirmed' : 3, 'recovered' : 3, 'deceased' : 0, 'other': 0})


# In[9]:


df_Kerala = pd.concat([df1, df2, df3], ignore_index=True)


# In[10]:


df_Kerala


# In[11]:


# Kerala had 1st 3 cases in India
# duplicate dataframe of missing Kerala dates 
df_India = df_Kerala.copy()

# change 'Kerala' to 'India'
df_India['state'].replace({'Kerala':'India'}, inplace=True)


# In[12]:


df_India


# In[13]:


# new frame without missing dates
states_mod = states
#pd.concat([df_Kerala, df_India, states], ignore_index=True)
states_mod.sort_values(['date','region'], ascending=True, ignore_index=True, inplace=True)
states0=states_mod
#print(states0)
# In[14]:


states_mod


# In[15]:


# pivot data with states as columns
pivot_cases = pd.pivot_table(states_mod, index = "date", columns = "region", values= "confirmed cases")

# drop non-state columns
pivot_cases = pivot_cases.drop(columns=do_not_include).fillna(0)
#print(pivot_cases)
plt.figure(figsize=(15,10))
pivot_cases["Kerala"].plot()
#plt.show()
## replacing nan total cases with 0
#pivot_cases.replace(np.nan, 0, inplace=True)


# In[16]:


#pivot_cases


# In[17]:

states3=[]
# new dataframe to store "daily new cases"
pivot_newcases = pivot_cases.copy()
#print(states0)
# calculate "daily new cases"
for column in pivot_newcases.columns[0:]:
    DailyNewCases = column
    states2=states0[states0["region"]==DailyNewCases].reset_index()
    ind=[str(x) for x in states2["date"].to_list()].index('2021-11-19 00:00:00')
    ll0=states2["confirmed cases"].to_list()
    ll0[ind]=ll0[ind-1]
    states2["confirmed cases"]=ll0
    ll=states2["confirmed cases"].diff().to_frame().fillna(0)
    pivot_newcases[DailyNewCases] = [0 for x in range(0,len(pivot_cases)-len(ll))]+ll['confirmed cases'].to_list()
    print(states2["confirmed cases"].to_list())
    states3.append(states2)
    #'2021-11-19'
    #print([str(x) for x in states2["date"].to_list()].index('2021-11-19 00:00:00'))
    #print(ll['confirmed cases'].to_list(),pivot_newcases[DailyNewCases])
    #states[states['region']==column]['confirmed cases']#.fillna(0).diff()#.apply(lambda x: [0 if y < 0 else y for y in x])
    #df1['A'] = df1['A'].apply(lambda x: [y if y <= 9 else 11 for y in x])
    #print(pivot_newcases[DailyNewCases])
pivot_newcases["Kerala"].plot()
#plt.title("Kerala")
#plt.show()
pivot_newcases["Ladakh"].plot()
plt.title("Ladakh")
#plt.show()
pivot_newcases["Mizoram"].plot()
plt.title("Mizoram")
#plt.show()

#print(pivot_newcases)
# In[18]:


# fill NaN in pivot_newcases (first row) with values from pivot_cases
pivot_newcases.fillna(pivot_cases, inplace=True)


# In[19]:


pivot_newcases


# In[20]:


# replace negative daily values by setting 0 as the lowest value
pivot_newcases = pivot_newcases.clip(lower=0)


# In[21]:


# new dataframe to store "avg new cases"
pivot_avgnewcases = pivot_newcases.copy()

# calculate 7-day averages of new cases
for column in pivot_avgnewcases.columns[0:]:
    DaySeven = column
    pivot_avgnewcases[DaySeven] = pivot_newcases[column].rolling(window=7, center=False).mean()

pivot_avgnewcases["Kerala"].plot()
#plt.show()
# In[22]:


# fill NaN in pivot_avgnewcases (first 6 rows) with values from pivot_newcases
pivot_recentnew = pivot_avgnewcases.fillna(pivot_newcases)


# In[23]:


pivot_recentnew


# In[24]:


# new dataframe to store "avg new cases" with centered average
pivot_avgnewcases_center = pivot_newcases.copy()

# calculate 7-day averages of new cases with centered average
for column in pivot_avgnewcases_center.columns[0:]:
    DaySeven = column
    pivot_avgnewcases_center[DaySeven] = pivot_avgnewcases_center[column].rolling(window=7, min_periods=4, center=True).mean()


# In[25]:


pivot_avgnewcases_center


# In[26]:


# reset indexes of "pivoted" data
pivot_cases = pivot_cases.reset_index()
pivot_newcases = pivot_newcases.reset_index()
pivot_recentnew = pivot_recentnew.reset_index()
pivot_avgnewcases_center = pivot_avgnewcases_center.reset_index()


# In[27]:


# convert "pivot" of total cases to "long form"
state_cases = pd.melt(pivot_cases, id_vars=['date'], var_name='state', value_name='cases')


# In[28]:


#print(state_cases)


# In[29]:


# convert "pivot" of daily new cases to "long form"
state_newcases = pd.melt(pivot_newcases, id_vars=['date'], var_name='state', value_name='new_cases')


# In[30]:


state_newcases


# In[31]:


# convert "pivot" of recent new cases to "long form" (7-day avg w first 6 days from "new cases")
state_recentnew = pd.melt(pivot_recentnew, id_vars=['date'], var_name='state', value_name='recent_new')


# In[32]:


state_recentnew


# In[33]:


# convert "pivot" of centered average new cases to "long form"
state_avgnewcases_center = pd.melt(pivot_avgnewcases_center, id_vars=['date'], var_name='state', value_name='avg_cases')


# In[34]:


state_avgnewcases_center


# In[35]:


# merge the 4 "long form" dataframes based on index
state_merge = pd.concat([state_cases, state_newcases, state_avgnewcases_center, state_recentnew], axis=1)


# In[36]:


state_merge


# In[37]:


# remove duplicate columns
state_merge = state_merge.loc[:,~state_merge.columns.duplicated()]


# In[38]:


# dataframe with only the most recent date for each state
# https://stackoverflow.com/questions/23767883/pandas-create-new-dataframe-choosing-max-value-from-multiple-observations
state_latest = state_merge.loc[state_merge.groupby('state').date.idxmax().values]


# In[39]:


state_latest


# In[40]:


# dataframe with peak average cases for each state
peak_avg_cases = state_merge.groupby('state')['recent_new'].agg(['max']).reset_index()
peak_avg_cases = peak_avg_cases.rename(columns = {'max':'peak_recent_new'})


# In[41]:


# merging total cases onto the merged dataframe
state_color_test = state_latest.merge(peak_avg_cases, on='state', how='left')


# In[42]:


# NOTE:
# original code uses integer from latest 7-day average in country color logic

# take integer from "recent_new"
state_color_test['recent_new_int'] = state_color_test['recent_new'].astype(int)


# In[43]:


state_color_test


# In[44]:


## UPDATE 9/25/20 - modified green logic due to quirk caused by original logic on countries page
## original logic caused Uruguay with avg ~16 cases to appear red because 16 > 50% of its low peak of 24

## Orignial green logic:
## if state_color_test['recent_new_int'] <= n_0*f_0 or state_color_test['recent_new_int'] <= n_0 and state_color_test['recent_new_int'] <= f_0*state_color_test['peak_recent_new']:

#choosing colors
n_0 = 20
f_0 = 0.5
f_1 = 0.2

# https://stackoverflow.com/questions/49586471/add-new-column-to-python-pandas-dataframe-based-on-multiple-conditions/49586787
def conditions(state_color_test):
    if state_color_test['recent_new_int'] <= n_0:
        return 'green'
    elif state_color_test['recent_new_int'] <= 1.5*n_0 and state_color_test['recent_new_int'] <= f_0*state_color_test['peak_recent_new'] or state_color_test['recent_new_int'] <= state_color_test['peak_recent_new']*f_1:
        return 'orange'
    else:
        return 'red'

state_color_test['color'] = state_color_test.apply(conditions, axis=1)


# In[45]:


state_color_test


# In[46]:


# dataframe with just state, total cases, and color
state_total_color = state_color_test[['state','cases','color']]

# rename cases to total_cases for the purpose of merging
state_total_color = state_total_color.rename(columns = {'cases':'total_cases'})


# In[47]:


# merging total cases onto the merged dataframe
state_final = state_merge.merge(state_total_color, on='state', how='left')


# In[48]:


state_final = state_final[['state','date','cases','new_cases','avg_cases','total_cases','recent_new','color']]


# In[49]:


state_final


# In[50]:


# rename states
staterename = {'Andaman and Nicobar Islands' : 'Andaman & Nicobar Islands',
              'Dadra and Nagar Haveli and Daman and Diu' : 'Dadra, Nagar Haveli, Daman & Diu',
              'Jammu and Kashmir' : 'Jammu & Kashmir'}

state_final['state'] = state_final['state'].replace(staterename)


# In[51]:


# drop rows where cumulative cases is NaN (dates before reported cases)
state_final = state_final.dropna(subset=['cases']) 


# In[52]:


state_final


# In[53]:


## Remove the 'cases' column to match format of Era's state result file 
state_final = state_final[['state','date','new_cases','avg_cases','total_cases','recent_new','color']]

#state_final.to_csv('state_final.csv', index=False)


# In[54]:


# dataframe with just state and color
state_color = state_color_test[['state','color']]

## creates csv similar to USStateColors.csv
#state_color.to_csv('stateColors.csv', index=False)


# In[55]:


# state_list = states['state'].unique()


# In[56]:




# In[57]:


# merging total cases onto the merged dataframe
# state_final_trans = state_final.merge(state_list, on='state', how='left')


# In[58]:


# adding Hindi names of states
#state_final['state_hindi'] = state_final['state']

#state_final['state_hindi'] = state_final['state_hindi'].replace(translation)

#state_final_trans.to_csv('result.csv', index=False)


# In[59]:

print(states0)
states4=pd.concat(states3)
# filter to start at Mar 1, 2020 #states0['date'] >= '2020-03-01' '2021-11-19'
state_final_trans_mar1 = state_final#[states4['date'] <= '2021-11-18']
#print(state_final_trans_mar1)
print(state_final_trans_mar1)
# In[60]:
state_final_trans_mar2=state_final_trans_mar1[state_final_trans_mar1['state']=="Assam"]
plt.figure(figsize=(15,10))
state_final_trans_mar2["total_cases"].plot()
#print(state_final_trans_mar2)
plt.title("Assam")
#plt.show()
state_final_trans_mar2=state_final_trans_mar1[state_final_trans_mar1['state']=="Ladakh"]
state_final_trans_mar2["total_cases"].plot()
#print(state_final_trans_mar2)
plt.title("Ladakh")
#plt.show()
state_final_trans_mar2=state_final_trans_mar1[state_final_trans_mar1['state']=="Mizoram"]
state_final_trans_mar2["total_cases"].plot()
#print(state_final_trans_mar2)
plt.title("Mizoram")
#plt.show()
#print(state_final_trans_mar2)
state_final_trans_mar1.to_csv('result.csv', index=False)
import matplotlib.pyplot as plt

#plt.plot(range(10))

#plt.title('Center Title')
#plt.title('Left Title', loc='left')
#plt.title('Right Title', loc='right')

#plt.show()
from datetime import datetime
#pro = datetime.strptime(date_n,'%Y-%m-%d').date()
#state,date,new_cases,avg_cases,total_cases,recent_new,color
lk=list(state_final_trans_mar1["state"].unique())
state_final_trans_mar1["date1"]=pd.to_datetime(state_final_trans_mar1["date"]).dt.strftime('%m/%d/%y')
#[datetime.strptime(x,'%Y-%m-%d').date() for x in state_final_trans_mar1["date"].to_list()]
#pd.to_datetime(lk["date"])#,format='%Y-%m-%d,%H:%M:%S', errors='coerce')
for item in lk:
    da=state_final_trans_mar1[state_final_trans_mar1["state"]==item]
    tt=[20 for x in range(0,len(da))]
    fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True, figsize=(16,9))
    ax.plot(da["date1"],tt, label = '20 cases')
    ax.legend(prop={'size': 20}, loc='upper left')
    ax.plot(da["date1"],da["avg_cases"],c='C4', linewidth = 2)
    ax.tick_params(labelsize=30)
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    item = item.replace("&","and")
    item = item.replace(","," and")
    plt.title(item, fontsize=30)
    if da['avg_cases'].iloc[-1]<=20:
      plt.title("\u25CF", loc='right',fontsize=50, color='green')
    else:
      plt.title("\u25CF", loc='right',fontsize=50, color='red')
    plt.tight_layout()
    plt.savefig('images/'+item+"_3.png",bbox_inches='tight')
    plt.close()
    #plt.show()
