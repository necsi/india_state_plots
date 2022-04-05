for item in list(pop.keys())[14:]:
    state = item # can choose any state from df.Region.unique()                                                                                                       
    threshold = 1 # x cases per million population                                                                                                                    
    offset_days = 60 # keep the most recent 60 days                                                                                                                   
    days = [(45,60)] # the time window to fit the decline curve, 45-60 usually works (60 is the most recent date)                                                     
    try:
        focus = df[df['Region'] == state].set_index('Date', drop=True)
        focus.index = pd.to_datetime(focus.index).strftime('%y/%m/%d')
        focus = focus['Confirmed Cases'].diff()[-offset_days:]
        title = state
        fig, ax = plt.subplots(nrows=1, ncols=1, sharey=True, figsize=(16,9))
        ax.plot(focus.index, focus.values, alpha=0.3)#, label=r'Daily cases in %s'%title)                                                                             
        ax.plot(focus.rolling(window=7, min_periods=1, center=True).mean(), c='green',alpha=0.3, ls='--')
        for i,(a,b) in enumerate(days):
            slope, intercept = optimize.curve_fit(linear_fit, np.arange(a,b), np.log(focus.values[a:b]+1))[0]
            #print(np.arange(a,b))                                                                                                                                    
            ax.plot(np.arange(a,b), np.exp(np.arange(a,b)*slope + intercept), c=('C'+str(i+1)))
            ax.annotate(np.round(np.exp(slope),3), xy=((a+b-2)/2, np.exp((a+b+2)/2*slope + intercept)), fontsize=24, c=('C'+str(i+1)))
        ax.set_yscale('log') #turn on/off this line to use log or linear scale                                                                                        

        b = np.array([focus.values[-1]])

        while b[-1] > pop[state] / 1e6 * threshold :
            b = np.append(b, b[-1]*(1+slope))
        numdays=len(b)+10
        base = datetime.date.today()
        #pd.to_datetime(focus.index).strftime('%y/%m/%d')                                                                                                             
        date_list = list(focus.index)+[(base + datetime.timedelta(days=x)).strftime('%y/%m/%d')  for x in range(0+numdays)]
        #print(date_list)                                                                                                                                             
        ax.plot(date_list,[pop[state]/1e6* threshold for x in range(0,len(date_list))],'--', label=str(threshold)+'/Mppl', linewidth=2)
        #threshold=1                                                                                                                                                  
        ax.legend(prop={'size': 30})
        ax.tick_params(labelsize=20)
        ax.xaxis.set_major_locator(plt.MaxNLocator(8))
        #ax.set_ylim(bottom=1, )                                                                                                                                      
        ax.plot(np.arange(len(focus),len(focus)+len(b)), b, ls='-.', c='C4')
        #print(b)                                                                                                                                                     
        #print(str(len(b))+' days until \ndaily cases\n<'+str(threshold)+' /Mppl')                                                                                    
  