import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
import datetime
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter
'''
numdays=100
base = datetime.date.today()
date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
print(base)
print(date_list)
'''
def linear_fit(x, a, b):
    return  a*x+b

pop= {"Andaman and Nicobar Islands":434192, "Andhra Pradesh":90959737, "Arunachal Pradesh":1382611, 
      "Assam":35607039, "Bihar":104099452, "Chandigarh":1169000, "Chhattisgarh":29436231, 
      "Dadra and Nagar Haveli and Daman and Diu":585764, "Goa":1458545, "Gujarat":60439692,
      'Haryana':25351462, 'Himachal Pradesh':7451955, 'Jammu and Kashmir':13606320, 
      'Jharkhand':38471, 'Karnataka':67562686, 'Kerala':35699443, 'Ladakh':274289, 
      'Lakshadweep':64473, 'Madhya Pradesh':85047748, 'Maharashtra':
112374333, 'Manipur':2855794, 'Meghalaya':3366710, 'Mizoram':1239244, 'Nagaland':1980602, 
      'Odisha':47645822, 'Puducherry':877010, 'Punjab':30141373, 'Rajasthan':81032689, 
      'Sikkim':619000, 'Tamil Nadu':77841267, 'Telangana':38510982, 'Tripura':4071, 
      'Uttar Pradesh':237882725, 'Uttarakhand':11250858, 'West Bengal':100580953, "Delhi":31181000}
df = pd.read_csv('https://raw.githubusercontent.com/coder-amey/COVID-19-India_Data/master/time-series/India_aggregated.csv')
df['Year'] = df['Date'].apply(lambda x : int(x.split('-')[2]))
df = df[df['Year'] > 2019] # filter out rows with year = 1970,...etc
df['Date'] = pd.to_datetime(df.Date, dayfirst=True)


for item in list(pop.keys()):
    state = item # can choose any state from df.Region.unique()
    threshold = 1 # x cases per million population
    offset_days = 60 # keep the most recent 60 days
    days = [(45,60)] # the time window to fit the decline curve, 45-60 usually works (60 is the most recent date)
    try:
        focus = df[df['Region'] == state].set_index('Date', drop=True)
        focus.index = pd.to_datetime(focus.index).strftime('%m/%d/%y')
        focus = focus['Confirmed'].diff()[-offset_days:] 
        title = state
        fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True, figsize=(16,9))
        ax.plot(focus.index, focus.values, alpha=0.5, linewidth=2)#, label=r'Daily cases in %s'%title)
        ax.plot(focus.rolling(window=7, min_periods=1, center=True).mean(), c='green',alpha=0.4, ls='--', linewidth=2)    
        for i,(a,b) in enumerate(days):
            slope, intercept = optimize.curve_fit(linear_fit, np.arange(a,b), np.log(focus.values[a:b]+1))[0]
            #print(np.arange(a,b))
            if focus.values[a:b].mean() > 10:
              ax.plot(np.arange(a,b), np.exp(np.arange(a,b)*slope + intercept), c=('C'+str(i+1)))
              ax.annotate(np.round(np.exp(slope),3), xy=((a+b-2)/2, np.exp((a+b+2)/2*slope + intercept)), fontsize=24, c=('C'+str(i+1)))
        if focus.values[a:b].mean() > 10:
            ax.set_yscale('log') #turn on/off this line to use log or linear scale

            b = np.array([focus.values[-1]])

            while b[-1] > pop[state] / 1e6 * threshold and slope <-0.001 :
                b = np.append(b, b[-1]*(1+slope))
            numdays=len(b)+10
            base = datetime.date.today()
            #pd.to_datetime(focus.index).strftime('%m/%d/%y')                                                                                    
            date_list = list(focus.index)+[(base + datetime.timedelta(days=x)).strftime('%m/%d/%y')  for x in range(0+numdays)]
            #print(date_list)                                                                                                                    
            ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label=str(threshold)+'/Mppl', linewidth=2)
            #threshold=1
            ax.legend(prop={'size': 20}, loc = 'lower right')
            ax.tick_params(labelsize=30)
            
            # user controls
            #####################################################
            sub_ticks = [10,20,50] # fill these midpoints
            sub_range = [-2,8] # from 100000000 to 0.000000001
            #format = "%.0f" # standard float string formatting

            # set scalar and string format floats
            #####################################################
            ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
            #ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter(format))
            #ax.yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())
            #ax.yaxis.set_minor_formatter(matplotlib.ticker.FormatStrFormatter(format))

            #force 'autoscale'
            #####################################################
            yd = [] #matrix of y values from all lines on plot
            for n in range(len(plt.gca().get_lines())):
                    line = plt.gca().get_lines()[n]
                    yd.append((line.get_ydata()).tolist())
            yd = [item for sublist in yd for item in sublist]
            ymin, ymax = np.min(yd), np.max(yd)
            ax.set_ylim([0.9*ymin, 1.1*ymax])

            # add sub ticks
            #####################################################
            set_sub_formatter=[]
            for i in sub_ticks:
                for j in range(sub_range[0],sub_range[1]):
                    set_sub_formatter.append(i*10**j)
            k = []
            for l in set_sub_formatter:
                if ymin<l<ymax:
                    k.append(l)
            ax.set_yticks(k)
            ax.set_yticklabels(['{:7.1f}'.format(x*1) if x < 1 else '{:7.0f}'.format(x*1) for x in k])
            #####################################################
            
            ax.xaxis.set_major_locator(plt.MaxNLocator(6))
            #formatter = ax.get_major_formatter()
            #ax.set_minor_formatter(formatter)
            #ax.yaxis.set_major_locator(plt.MinNLocator(2))
            #ax.set_ylim(bottom=1, )    
            ax.plot(np.arange(len(focus),len(focus)+len(b)), b, ls='-.', c='C4')
            #print(b)
            #print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')
            try:
                if len(b)==2:
                  dy = b[-1] - b[0]
                  dx = len(focus)+len(b) - len(focus)
                  angle = np.rad2deg(np.arctan2(dy, dx))
                  #angle = np.rad2deg(slope)
                  plt.text(len(focus), b[0], str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', ha='left', va='bottom', rotation=angle, rotation_mode='anchor',c='C4', size = 20,transform_rotates_text=True)
                  #ax.annotate(s=str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(len(focus)+len(b)-19, b[0]), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9
                  #ax.annotate(s=str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(0.9, b[0]), xycoords = ax.get_yaxis_transform(), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9
                elif len(b) >2:
                  dy = b[-1] - b[0]
                  dx = len(focus)+len(b) - len(focus)
                  angle = np.rad2deg(np.arctan2(dy, dx))
                  #angle = np.rad2deg(slope)
                  plt.text(len(focus)+ int(len(b)/4), b[int(len(b)/4)], str(len(b)-1)+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', ha='left', va='bottom', rotation=angle, rotation_mode='anchor',c='C4', size = 20,transform_rotates_text=True)
                  #ax.annotate(s=str(len(b)-1)+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(0.9, b[0]), xycoords = ax.get_yaxis_transform(), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9

            except:
                #ax.annotate(s=str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(len(focus)+len(b)-9, 10), fontsize=20, ha='center', c='C4')
                print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')  
            #ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label='1/Mppl', linewidth=2)
            plt.title(state, fontsize=30)
            plt.tight_layout()
            plt.savefig('images/'+state+'_1.png',bbox_inches='tight')
            plt.savefig('images/'+state+'_log_1.png',bbox_inches='tight')

            fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True, figsize=(16,9))
            ax.plot(focus.index, focus.values, alpha=0.5, linewidth=2)#, label=r'Daily cases in %s'%title)
            ax.plot(focus.rolling(window=7, min_periods=1, center=True).mean(), c='green',alpha=0.4, ls='--', linewidth=2)    
            for i,(a,b) in enumerate(days):
                slope, intercept = optimize.curve_fit(linear_fit, np.arange(a,b), np.log(focus.values[a:b]+1))[0]
                #print(np.arange(a,b))
                if focus.values[a:b].mean() > 10:
                  ax.plot(np.arange(a,b), np.exp(np.arange(a,b)*slope + intercept), c=('C'+str(i+1)))
                  ax.annotate(np.round(np.exp(slope),3), xy=((a+b-2)/2, np.exp((a+b+2)/2*slope + intercept)), fontsize=24, c=('C'+str(i+1)))
                

            b = np.array([focus.values[-1]])

            while b[-1] > pop[state] / 1e6 * threshold and slope <-0.001 :
                b = np.append(b, b[-1]*(1+slope))
            numdays=len(b)+10
            base = datetime.date.today()
            #pd.to_datetime(focus.index).strftime('%m/%d/%y')                                                                                    
            date_list = list(focus.index)+[(base + datetime.timedelta(days=x)).strftime('%m/%d/%y')  for x in range(0+numdays)]
            #print(date_list)                                                                                                                    
            ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label=str(threshold)+'/Mppl', linewidth=2)
            #threshold=1
            ax.legend(prop={'size': 20}, loc = 'lower right')
            ax.tick_params(labelsize=30)
            ax.xaxis.set_major_locator(plt.MaxNLocator(6))
            #ax.yaxis.set_major_locator(plt.MinNLocator(2))
            #ax.set_ylim(bottom=1, )    
            ax.plot(np.arange(len(focus),len(focus)+len(b)), b, ls='-.', c='C4')
            #print(b)
            #print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')
            try:
                if len(b)==2:
                  dy = b[-1] - b[0]
                  dx = len(focus)+len(b) - len(focus)
                  angle = np.rad2deg(np.arctan2(dy, dx))
                  #angle = np.rad2deg(slope)
                  plt.text(len(focus), b[0], str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', ha='left', va='bottom', rotation=angle, rotation_mode='anchor',c='C4', size = 20,transform_rotates_text=True)
                  #ax.annotate(s=str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(len(focus)+len(b)-19, b[0]), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9
                  #ax.annotate(s=str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(0.9, b[0]), xycoords = ax.get_yaxis_transform(), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9
                elif len(b) >2:
                  dy = b[-1] - b[0]
                  dx = len(focus)+len(b) - len(focus)
                  angle = np.rad2deg(np.arctan2(dy, dx))
                  #angle = np.rad2deg(slope)
                  plt.text(len(focus)+ int(len(b)/4), b[int(len(b)/4)], str(len(b)-1)+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', ha='left', va='bottom', rotation=angle, rotation_mode='anchor',c='C4', size = 20,transform_rotates_text=True)
                  #ax.annotate(s=str(len(b)-1)+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(0.9, b[0]), xycoords = ax.get_yaxis_transform(), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9

            except:
                #ax.annotate(s=str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(len(focus)+len(b)-9, 10), fontsize=20, ha='center', c='C4')
                print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')  
            #ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label='1/Mppl', linewidth=2)
            plt.title(state, fontsize=30)
            plt.tight_layout()
            plt.savefig('images/'+state+'_lin_1.png',bbox_inches='tight')
            
        else:
            b = np.array([focus.values[-1]])

            while b[-1] > pop[state] / 1e6 * threshold and slope <-0.001 :
                b = np.append(b, b[-1]*(1+slope))
            numdays=len(b)+10
            base = datetime.date.today()
            #pd.to_datetime(focus.index).strftime('%m/%d/%y')                                                                                    
            date_list = list(focus.index)+[(base + datetime.timedelta(days=x)).strftime('%m/%d/%y')  for x in range(0+numdays)]
            #print(date_list)                                                                                                                    
            ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label=str(threshold)+'/Mppl', linewidth=2)
            #threshold=1
            ax.legend(prop={'size': 20}, loc = 'lower right')
            ax.tick_params(labelsize=30)
            ax.xaxis.set_major_locator(plt.MaxNLocator(6))
            #ax.yaxis.set_major_locator(plt.MinNLocator(2))
            #ax.set_ylim(bottom=1, )    
            ax.plot(np.arange(len(focus),len(focus)+len(b)), b, ls='-.', c='C4')
            #print(b)
            #print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')
            try:
                if len(b)==2:
                  dy = b[-1] - b[0]
                  dx = len(focus)+len(b) - len(focus)
                  angle = np.rad2deg(np.arctan2(dy, dx))
                  #angle = np.rad2deg(slope)
                  plt.text(len(focus), b[0], str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', ha='left', va='bottom', rotation=angle, rotation_mode='anchor',c='C4', size = 20,transform_rotates_text=True)
                  #ax.annotate(s=str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(len(focus)+len(b)-19, b[0]), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9
                  #ax.annotate(s=str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(0.9, b[0]), xycoords = ax.get_yaxis_transform(), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9
                elif len(b) >2:
                  dy = b[-1] - b[0]
                  dx = len(focus)+len(b) - len(focus)
                  angle = np.rad2deg(np.arctan2(dy, dx))
                  #angle = np.rad2deg(slope)
                  plt.text(len(focus)+ int(len(b)/4), b[int(len(b)/4)], str(len(b)-1)+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', ha='left', va='bottom', rotation=angle, rotation_mode='anchor',c='C4', size = 20,transform_rotates_text=True)
                  #ax.annotate(s=str(len(b)-1)+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(0.9, b[0]), xycoords = ax.get_yaxis_transform(), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9

            except:
                #ax.annotate(s=str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(len(focus)+len(b)-9, 10), fontsize=20, ha='center', c='C4')
                print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')  
            #ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label='1/Mppl', linewidth=2)
            plt.title(state, fontsize=30)
            plt.tight_layout()
            plt.savefig('images/'+state+'_1.png',bbox_inches='tight')
            plt.savefig('images/'+state+'_lin_1.png',bbox_inches='tight')

            fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True, figsize=(16,9))
            ax.plot(focus.index, focus.values, alpha=0.5, linewidth=2)#, label=r'Daily cases in %s'%title)
            ax.plot(focus.rolling(window=7, min_periods=1, center=True).mean(), c='green',alpha=0.4, ls='--', linewidth=2)    
            for i,(a,b) in enumerate(days):
                slope, intercept = optimize.curve_fit(linear_fit, np.arange(a,b), np.log(focus.values[a:b]+1))[0]
                #print(np.arange(a,b))
                if focus.values[a:b].mean() > 10:
                  ax.plot(np.arange(a,b), np.exp(np.arange(a,b)*slope + intercept), c=('C'+str(i+1)))
                  ax.annotate(np.round(np.exp(slope),3), xy=((a+b-2)/2, np.exp((a+b+2)/2*slope + intercept)), fontsize=24, c=('C'+str(i+1)))
                

            ax.set_yscale('log')
            b = np.array([focus.values[-1]])

            while b[-1] > pop[state] / 1e6 * threshold and slope <-0.001 :
                b = np.append(b, b[-1]*(1+slope))
            numdays=len(b)+10
            base = datetime.date.today()
            #pd.to_datetime(focus.index).strftime('%m/%d/%y')                                                                                    
            date_list = list(focus.index)+[(base + datetime.timedelta(days=x)).strftime('%m/%d/%y')  for x in range(0+numdays)]
            #print(date_list)                                                                                                                    
            ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label=str(threshold)+'/Mppl', linewidth=2)
            #threshold=1
            ax.legend(prop={'size': 20}, loc = 'lower right')
            ax.tick_params(labelsize=30)
            
            # user controls
            #####################################################
            sub_ticks = [10,20,50] # fill these midpoints
            sub_range = [-2,8] # from 100000000 to 0.000000001
            #format = "%.0f" # standard float string formatting

            # set scalar and string format floats
            #####################################################
            ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
            #ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter(format))
            #ax.yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())
            #ax.yaxis.set_minor_formatter(matplotlib.ticker.FormatStrFormatter(format))

            #force 'autoscale'
            #####################################################
            yd = [] #matrix of y values from all lines on plot
            for n in range(len(plt.gca().get_lines())):
                    line = plt.gca().get_lines()[n]
                    yd.append((line.get_ydata()).tolist())
            yd = [item for sublist in yd for item in sublist]
            ymin, ymax = np.min(yd), np.max(yd)
            ax.set_ylim([0.9*ymin, 1.1*ymax])

            # add sub ticks
            #####################################################
            set_sub_formatter=[]
            for i in sub_ticks:
                for j in range(sub_range[0],sub_range[1]):
                    set_sub_formatter.append(i*10**j)
            k = []
            for l in set_sub_formatter:
                if ymin<l<ymax:
                    k.append(l)
            ax.set_yticks(k)
            ax.set_yticklabels(['{:7.1f}'.format(x*1) if x < 1 else '{:7.0f}'.format(x*1) for x in k])
            #####################################################
            
            ax.xaxis.set_major_locator(plt.MaxNLocator(6))
            #formatter = ax.get_major_formatter()
            #ax.set_minor_formatter(formatter)
            #ax.yaxis.set_major_locator(plt.MinNLocator(2))
            #ax.set_ylim(bottom=1, )    
            ax.plot(np.arange(len(focus),len(focus)+len(b)), b, ls='-.', c='C4')
            #print(b)
            #print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')
            try:
                if len(b)==2:
                  dy = b[-1] - b[0]
                  dx = len(focus)+len(b) - len(focus)
                  angle = np.rad2deg(np.arctan2(dy, dx))
                  #angle = np.rad2deg(slope)
                  plt.text(len(focus), b[0], str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', ha='left', va='bottom', rotation=angle, rotation_mode='anchor',c='C4', size = 20,transform_rotates_text=True)
                  #ax.annotate(s=str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(len(focus)+len(b)-19, b[0]), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9
                  #ax.annotate(s=str(len(b)-1)+' day until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(0.9, b[0]), xycoords = ax.get_yaxis_transform(), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9
                elif len(b) >2:
                  dy = b[-1] - b[0]
                  dx = len(focus)+len(b) - len(focus)
                  angle = np.rad2deg(np.arctan2(dy, dx))
                  #angle = np.rad2deg(slope)
                  plt.text(len(focus)+ int(len(b)/4), b[int(len(b)/4)], str(len(b)-1)+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', ha='left', va='bottom', rotation=angle, rotation_mode='anchor',c='C4', size = 20,transform_rotates_text=True)
                  #ax.annotate(s=str(len(b)-1)+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(0.9, b[0]), xycoords = ax.get_yaxis_transform(), fontsize=20, ha='center', c='C4')#len(focus)+len(b)-9

            except:
                #ax.annotate(s=str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl', xy=(len(focus)+len(b)-9, 10), fontsize=20, ha='center', c='C4')
                print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')  
            #ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label='1/Mppl', linewidth=2)
            plt.title(state, fontsize=30)
            plt.tight_layout()
            plt.savefig('images/'+state+'_log_1.png',bbox_inches='tight')
            
    except:
        print(item)
        continue
