def icu_burden_snapshot(days=30,
                        day_total_cases=50,
                        doubles_in_days=6,
                        case_fatality_rate=.4,
                        capacity=200,
                        summaries=True):
  
    import numpy as np
    import pandas as pd
    
    total_cases = []

    for day in range(days):
        
        # count how many new cases there will be today
        if day % doubles_in_days == 0:
            _temp_new_ = day_total_cases / doubles_in_days
        day_new_cases = _temp_new_
    
        day_total_cases = day_total_cases + day_new_cases
    
        if day_total_cases > capacity:
            day_total_admitted = capacity
        else:
            day_total_admitted = day_total_cases
    
        total_cases.append(day_total_cases)
    
    df = pd.DataFrame()
    
    random_effect = np.round(np.random.normal(0, .2, days), 2)
    
    df['cases'] = np.array(total_cases) * random_effect
    
    admissions = lambda x: x if capacity >= x else capacity
    df['admissions'] = df['cases'].apply(admissions).astype(int)
    
    expired_cfr = lambda x: x * case_fatality_rate
    df['expired_cfr'] = df['admissions'].apply(expired_cfr)
    
    df['recovered'] = df['admissions'] - df['expired_cfr']
    df['expired_capacity'] = abs(df['cases'] - df['admissions'])
    
    df['doubles_in_days'] = doubles_in_days
    df['case_fatality_rate'] = case_fatality_rate
    df['capacity'] = capacity
    
    if summaries:
        return df.astype(int).max().tolist()
    
    else:
        return df.astype(int)

 
def create_combinations(params):
    
    '''Takes as input the input arguments from simulate() and 
    returns all the possible combinations'''
    
    import numpy as np
    import itertools
    
    capacity = params['capacity']
    doublers = params['doubles_in_days']
    case_fatality_rate = params['case_fatality_rate']
    
    capacity = range(capacity[0], capacity[1], capacity[2])
    doublers = range(doublers[0], doublers[1], doublers[2])
    case_fatality_rates = np.arange(case_fatality_rate[0], case_fatality_rate[1], case_fatality_rate[2]).tolist()
    
    combinations = list(itertools.product(*[capacity, doublers, case_fatality_rates]))

    return combinations
    

def simulate(params, randomize=False, limit=None):
    

    from tqdm import tqdm
    
    combinations = create_combinations(params)

    if randomize:
        np.random.shuffle(combinations)
    
    out = []
    
    for combination in tqdm(combinations[:None]):
        
        out.append(icu_burden_snapshot(capacity=combination[0],
                                       doubles_in_days=combination[1],
                                       case_fatality_rate=combination[2]))
        
    df = pd.DataFrame(out)
    df.columns = ['cases', 'admissions', 'expired_cfr',
                   'recovered', 'expired_capacity',
                   'doubles_in_days', 'case_fatality_rate', 'capacity']
    
    return df
