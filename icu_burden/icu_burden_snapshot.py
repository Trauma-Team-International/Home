import pandas as pd

def icu_burden_snapshot(days=30,
                        day_total_cases=50,
                        doubles_in_days=6,
                        case_fatality_rate=.4,
                        capacity=200,
                        summaries=True):

    '''Does the work for simulate() by taking as input
    parameters, and then returning either summaries with
    peak values, or a dataframe with raw data (daily).'''
    
    import numpy as np
    
    total_cases = []

    for day in range(days):
        
        # count how many new cases there will be today
        if day % doubles_in_days == 0:
            _temp_new_ = day_total_cases / doubles_in_days
        day_new_cases = _temp_new_
    
        day_total_cases = day_total_cases + day_new_cases
      
        total_cases.append(day_total_cases)
    
    df = pd.DataFrame()
    
    random_effect = np.round(np.random.normal(1, .1, days), 3)
    
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
        return df.max().tolist()
    
    else:
        return df
    
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
    

def simulate(params, days=20, cases=50, randomize=False):
    
    
    '''Accepts as input a set of parameters, and 
    returns a dataframe with peak values for each
    parameter combination. The only thing that is 
    simulated in an event-based manner, is total
    cases, and then everything else is inferred 
    from there onwards. 
    
    params | dict or list | either parameter ranges or
                            list of parameter combinations
    days | int | number of days to simulate
    cases | int | number of cases to start with
    randomize | bool | randomize order if True (for debugging)
    
    
    Example: 
    
    params = {'capacity': [250, 1000, 50],
              'doubles_in_days': [4, 8, 1],
              'case_fatality_rate': [0.30, 0.5, 0.01]}

    results = simulate(params)

    '''

    from tqdm import tqdm
    import numpy as np
    
    if isinstance(params, dict):
        combinations = create_combinations(params)
    else:
        combinations = params

    if randomize:
        np.random.shuffle(combinations)
    
    out = []
    
    for combination in tqdm(combinations):
        
        out.append(icu_burden_snapshot(capacity=combination[0],
                                       doubles_in_days=combination[1],
                                       case_fatality_rate=combination[2],
                                       days=days,
                                       day_total_cases=cases))

    df = pd.DataFrame(out)
    df.columns = ['cases', 'admissions', 'expired_cfr',
                  'recovered', 'expired_capacity',
                  'doubles_in_days', 'case_fatality_rate', 'capacity']

    _temp_ = df.case_fatality_rate.values
    df = df.astype(int)
    df['case_fatality_rate'] = _temp_
    
    return df
