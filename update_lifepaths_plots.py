
import json
import pandas as pd
import matplotlib.pyplot as plt 
date = pd.to_datetime("today").strftime('_%m_%d')
states = pd.read_csv("https://prsindia.org/covid-19/cases/download")
states=states[states["Date"].str.contains("202")]
states.columns= states.columns.str.lower()
states['date'] = pd.to_datetime(states['date'], format= '%d/%m/%Y')
#print(states['date'].unique())
#print(states[states["region"]=="Assam"]["confirmed cases"])
do_not_include = ['India','State assignment pending','World']
# create an array of 2 dates starting at '2020-01-31', one per day
rng = pd.date_range('2020-01-31', periods=2, freq='D')
df1 = pd.DataFrame({ 'date': rng, 'state' : 'Kerala', 'confirmed' : 1, 'recovered' : 0, 'deceased' : 0, 'other': 0})
# create an array of 10 dates starting at '2020-02-04', one per day
rng = pd.date_range('2020-02-04', periods=10, freq='D')
df2 = pd.DataFrame({ 'date': rng, 'state' : 'Kerala', 'confirmed' : 3, 'recovered' : 0, 'deceased' : 0, 'other': 0})
# create an array of 16 dates starting at '2020-02-24', one per day
rng = pd.date_range('2020-02-15', periods=16, freq='D')
df3 = pd.DataFrame({ 'date': rng, 'state' : 'Kerala', 'confirmed' : 3, 'recovered' : 3, 'deceased' : 0, 'other': 0})
df_Kerala = pd.concat([df1, df2, df3], ignore_index=True)
df_Kerala
# Kerala had 1st 3 cases in India
# duplicate dataframe of missing Kerala dates 
df_India = df_Kerala.copy()
# change 'Kerala' to 'India'
df_India['state'].replace({'Kerala':'India'}, inplace=True)
# In[12]:
# new frame without missing dates
states_mod = states
#pd.concat([df_Kerala, df_India, states], ignore_index=True)
states_mod.sort_values(['date','region'], ascending=True, ignore_index=True, inplace=True)
states0=states_mod
# pivot data with states as columns
pivot_cases = pd.pivot_table(states_mod, index = "date", columns = "region", values= "confirmed cases")
# drop non-state columns
pivot_cases = pivot_cases.drop(columns=do_not_include).fillna(0)
sts=pivot_cases.columns.to_list()
#import datetime
from datetime import datetime
#from time import time, sleep

from datetime import timezone
dt = datetime(2015, 10, 19)
timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

dts=[x.replace(tzinfo=timezone.utc).timestamp() for x in pivot_cases.index.to_list()]

all=[]#[["cases","deaths","recovered","Country","Time"]]
ind=0
for el in dts:
    arr=[]
    for item in sts:
        ll=pivot_cases[item].to_list()[dts.index(el)]
        #print(ll)
        first=[ll,ll,ll,item,el]
        arr.append(first)
        #if ind>60:
        all.append(first)
    ind+=1


kk={"countries": sts, "timeline":dts,"series":all}
import matplotlib.pyplot as plt
import numpy as np

ypoints = np.array([3, 8, 1, 10])

for item1 in sts:
    pop=199812341
    ll=[]
    ll0=[]
    ind1=0
    rr=[]
    for nn in pivot_cases[item1].diff().fillna(0).to_list():
        ll.append(nn/pop)
        rr.append(ind1)
        ind1+=1    

states3=[]
# new dataframe to store "daily new cases"
pivot_newcases = pivot_cases.copy()
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
    #print(states2["confirmed cases"].to_list())
    states3.append(states2)

# fill NaN in pivot_newcases (first row) with values from pivot_cases
pivot_newcases.fillna(pivot_cases, inplace=True)

pop={"Andaman and Nicobar Islands":434192, "Andhra Pradesh":90959737, "Arunachal Pradesh":1382611, "Assam":35607039, "Bihar":104099452, "Chandigarh":1169000, "Chhattisgarh":29436231, "Dadra and Nagar Haveli and Daman and Diu":585764, "Goa":1458545, "Gujarat":60439692,'Haryana':25351462, 'Himachal Pradesh':7451955, 'Jammu and Kashmir':13606320, 'Jharkhand':38471, 'Karnataka':67562686, 'Kerala':35699443, 'Ladakh':274289, 'Lakshadweep':64473, 'Madhya Pradesh':85047748, 'Maharashtra':
112374333, 'Manipur':2855794, 'Meghalaya':3366710, 'Mizoram':1239244, 'Nagaland':1980602, 'Odisha':47645822, 'Puducherry':877010, 'Punjab':30141373, 'Rajasthan':81032689, 'Sikkim':619000, 'Tamil Nadu':77841267, 'Telangana':38510982, 'Tripura':4071, 'Uttar Pradesh':237882725, 'Uttarakhand':11250858, 'West Bengal':100580953, "Delhi":31181000}

from scipy import optimize
def linear_fit(x, a, b):
    return  a*x+b

data = {'Confirmed':[], 'Death':[], 'Recovered':[]}  
def country_dynamics(category, country, cut, days):
    #print(category, country, cut, days)
    fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True, figsize=(16,9))
    ax.set_yscale('log')
    cum = data[category]
    #print(cum.index)
    kk0=pivot_newcases.index.values#.astype('<M8[M]')#.astype(str)
    cum['time'] = kk0#.dt.strftime('%m/%d') 
    cum.index = cum.time#.dt.strftime('%Y-%m-%d')
    #print(cut)
    cum.drop('time', axis=1, inplace=True)
    focus = (cum - cum.shift(1)).iloc[cut:,:]
    #print(cum)
    #print(cum.iloc[cut:,:])
    print(focus)
    ax.plot(cum.iloc[cut:,:], alpha=0.8, lw=2, label='Daily Cases in ' + country )
    ax.scatter(focus.index, focus[country], c='gray', s=5, label='Daily cases in %s'%country)
    ax.plot(focus[country].rolling(window=7, min_periods=1, center=True).mean(), c='green',alpha=0.3)    
    for i,(a,b) in enumerate(days):
        slope, intercept = optimize.curve_fit(linear_fit, np.arange(a,b), np.log(focus[country].values[a:b]+1))[0]
        ax.plot(np.arange(a,b), np.exp(np.arange(a,b)*slope + intercept), c=('C'+str(i+1)))
        ax.annotate(np.round(np.exp(slope),3), 
                    xy=((a+b-2)/2, np.exp((a+b+2)/2*slope + intercept)*1.2), fontsize=24, c=('C'+str(i+1)))                    
            
    ax.legend(prop={'size': 30})
    ax.tick_params(labelsize=20)
    ax.xaxis.set_major_locator(plt.MaxNLocator(12))
    ax.format_xdata = mdates.DateFormatter('%m-%d')
    plt.tight_layout()
    plt.savefig(country+'.png')
    plt.close()    

def country_dynamics_all(country, cut, days):
    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(12,12))
    fig.subplots_adjust(wspace=0, hspace=0)
    
    for i,category in enumerate(data.keys()):
        ax[i].set_yscale('log')
        cum = data[category].copy().T[[country]]
        focus = (cum - cum.shift(1)).iloc[cut:,:]

        ax[i].plot(cum.iloc[cut:,:], alpha=0.5, lw=2, label=category + ' cases in ' + country )
        ax[i].scatter(focus.index, focus[country], c='gray', s=5)

        for j,(a,b) in enumerate(days[i]):
            slope, intercept = optimize.curve_fit(linear_fit, np.arange(a,b), np.log(focus[country].values[a:b]+1))[0]
            ax[i].plot(np.arange(a,b), np.exp(np.arange(a,b)*slope + intercept), c=('C'+str(j+1)))
            ax[i].annotate(np.round(np.exp(slope),2), 
                    xy=((a+b-2)/2, np.exp((a+b)/2*slope + intercept)), fontsize=14, c=('C'+str(j+1)))  

        ax[i].legend(prop={'size': 12})
        ax[i].tick_params(labelrotation=90, labelsize=14)
        # ax.xaxis.set_major_locator(plt.MaxNLocator(15))
        #plt.savefig(item2+'.png')
        plt.tight_layout()

        
def country_dynamics_all_in_one(country, cut, days):
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(12,10))
    fig.subplots_adjust(wspace=0, hspace=0)
    
    for i,category in enumerate(data.keys()):
        ax.set_yscale('log')
        focus = (cum - cum.shift(1)).iloc[cut:,:]

#         ax.plot(cum.iloc[cut:,:], alpha=0.5, lw=2, label=category + ' cases in ' + country )
        ax.scatter(focus.index, focus[country], c='gray', s=5)

        for j,(a,b) in enumerate(days[i]):
            slope, intercept = optimize.curve_fit(linear_fit, np.arange(a,b), np.log(focus[country].values[a:b]+1))[0]
            ax[i].plot(np.arange(a,b), np.exp(np.arange(a,b)*slope + intercept), c=('C'+str(j+1)))
            ax[i].annotate(np.round(np.exp(slope),2), 
                    xy=((a+b-2)/2, np.exp((a+b)/2*slope + intercept)), fontsize=14, c=('C'+str(j+1)))  

        ax[i].legend(prop={'size': 12})
        ax[i].tick_params(labelrotation=90, labelsize=14)
        # ax.xaxis.set_major_locator(plt.MaxNLocator(15))
        plt.tight_layout()

for item2 in sts:
    pivot_newcases[item2]=[x/pop[item2]*1000000 for x in pivot_newcases[item2].to_list()]
    lk=list(pivot_newcases.index)
    data['Confirmed']=pivot_newcases[item2]
    data['Death']=lk
    data['Recovered']=lk
    try:
        country_dynamics('Confirmed', item2,40, [(7,40),(40,65),(65,85),(95,140),(140,190),(190,218),(218,232)])
    except:
        continue

