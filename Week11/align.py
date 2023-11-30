def align(X1, X2):   
    data = X1.join(X2, how = 'outer', sort = True)
    #Interpolate missing values (will interpolate labels but also X1)
    data = data.interpolate('index', limit_area ='inside')

    #Get only the data interpolated (remove NaN)
    data = data.loc[data.iloc[:,0].dropna().index.intersection(data.iloc[:,-1].dropna().index)]

    #Remove original labels index (X1 was interpolated at these rows, we don't want it)
    data = data[~data.index.isin(X2.index.intersection(data.index))]

    #X back but cut with labels
    X1 = data[X1.columns]
    
    #Labels and columns of subject and condition
    X2 = data[X2.columns]

    #Resolve some align issues
    X2 = X2.round(decimals=0)
    X2[(X2['Right_Hand_channel1'] == 0) & (X2['Right_Hand_channel2'] == 1) &  
       (X2['Right_Hand_channel3'] == 2) & (X2['Right_Hand_channel4'] == 2) &  
       (X2['Right_Hand_channel5'] == 2) & (X2['Right_Hand_channel6'] == 2)] = [0,0,2,2,2,2]

    return X1,X2

