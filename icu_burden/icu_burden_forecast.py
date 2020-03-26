def icu_burden_projection(incubation_period=5,
                          reproduction_rate=2.1,
                          infectious_period=7,
                          tested_daily=1000,
                          positive_rate=.13,
                          hospitalization_rate=.17,
                          icu_rate=.2,
                          ventilation_rate=.9,
                          population=5530000,
                          days=180):
    
    import numpy as np
    import pandas as pd
    
    # convert values for model
    incubation_period = (1 / incubation_period)
    infectious_period = (1 / infectious_period)
    
    avg_contact_rate = infectious_period * reproduction_rate
    
    timeline = range(days)
    
    # SEIR init values
    S, E, I, R = [1 - 1 / population], [1 / population], [0], [0]
    
    # NEW init values
    tested = [0]
    positive = [0]
    hospitalized = [0]
    icu = [0]
    ventilation = [0]
    
    for _ in timeline[1:]:
    
        next_S = S[-1] - (avg_contact_rate * S[-1] * I[-1])
        S.append(next_S)
        
        next_E = E[-1] + (avg_contact_rate * S[-1] * I[-1] - incubation_period * E[-1])
        E.append(next_E)
        
        next_I = I[-1] + (incubation_period * E[-1] - infectious_period * I[-1])
        I.append(next_I)
    
        '''
        if next_I > tested_daily:
            # full testing capacity is used
            round_tested_daily = tested_daily
        elif next_I <= tested_daily:
            # testing bandwidth remains
            round_tested_daily = next_I
        tested.append(round_tested_daily)
        '''
        
        round_tested_daily = tested_daily
        tested.append(round_tested_daily)
        
        round_positive = round_tested_daily * positive_rate
        positive.append(round_positive)
        
        round_hospitalized = round_positive * hospitalization_rate
        hospitalized.append(round_hospitalized)
        
        round_icu = round_hospitalized * icu_rate
        icu.append(round_icu)
        
        round_ventilation = round_icu * ventilation_rate
        ventilation.append(round_ventilation)
        
        next_R = R[-1] + (infectious_period*I[-1])
        R.append(next_R)
    
    # put together the dataset
    out = np.stack([I, tested, positive, hospitalized, icu, ventilation, R]).T     
    df = pd.DataFrame(out)
    df.columns = ['infected',
                  'tested',
                  'positive',
                  'hospitalized',
                  'icu',
                  'ventilation',
                  'removed']
                  
    df = df.astype(int)

    return df
