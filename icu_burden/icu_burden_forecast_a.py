def create_combinations(params):
    
    '''Takes as input the input arguments from simulate() and 
    returns all the possible combinations'''
    
    import numpy as np
    import itertools
    
    capacity = params['capacity']
    capacity = range(capacity[0], capacity[1], capacity[2])
    
    doublers = params['doubles_in_days']
    doublers = range(doublers[0], doublers[1], doublers[2])
    
    mean_duration = params['mean_duration']
    durations = range(mean_duration[0], mean_duration[1], mean_duration[2])
    
    case_fatality_rate = params['case_fatality_rate']
    case_fatality_rates = np.arange(case_fatality_rate[0], case_fatality_rate[1], case_fatality_rate[2]).tolist()
    
    combinations = list(itertools.product(*[capacity, doublers, durations, case_fatality_rates]))

    return combinations


def compute_expired(day_total_cases, case_fatality_rate, mean_duration):
    
    import math
    
    day_expired_cases = day_total_cases * (case_fatality_rate / mean_duration)
    
    return int(math.ceil(day_expired_cases))


def compute_new(day, day_total_cases, doubles_in_days):
    
    day_new_cases = day_total_cases * (.8 / doubles_in_days)
        
    return int(day_new_cases)
    

def simulate(params, randomize=False, debug_limit=None):
    
    '''
    
    params | dict | parameter dictionary where each input is a list with start, stop and step values
    
    EXAMPLE:
    
    params = {'capacity': [150, 1000, 50],
              'doubles_in_days': [2, 6, 1],
              'mean_duration': [17, 23, 1],
              'case_fatality_rate': [0.4, 0.6, 0.01]}
    
    results = simulate(params)
    
    - each combination runs for 30 days
    - `capacity` is constant through days
    - `doubles_in_days` is constant through days
    - `mean_duration` is constant through days
    - daily cases grow based on `doubles_in_days`
    - each day death happens according to `case_fatality_rate`
    - if capacity is exceeded, more death results
    - every day `mean_duration` is used for deciding how many recover

    '''

    import uuid
    import math
    import random
    import pandas as pd
    import numpy as np
    from tqdm import tqdm
    
    # create all possible combinations from inputs
    combinations = create_combinations(params)

    if randomize:
        np.random.shuffle(combinations)
    
    # initiate output
    out = []
    
    # program loop
    
    for combination in tqdm(combinations[:debug_limit]):

        # combination starts
        
        days = 30
        day_total_cases = 41
        
        capacity = combination[0]
        doubles_in_days = combination[1]
        mean_duration = combination[2]
        case_fatality_rate = combination[3]

        # reset outputs
        demand_cases = []
        total_cases = []
        new_cases = []
        expired_cases = []
        
        for day in range(days):
            
            '''
            - [x] there is a certain number of patients at start `day_total_cases`
            - [x] each day there are more new patients based on `doubles_in_days`
            - [x] each day some patients will die based on `case_fatality_rate`
            - [x] each day some patients are released based on `mean_duration`
              [x]- all patients that meet `mean_duration` and did not die are released
            - some patients can be admitted based on current available capacity
              - such patients will be added to total patients
            - some patients may not be admittable due to lack of current capacity
              - such patients will die

            '''
            
            if day != 0:
                
                # use previous day's end number as base
                day_total_cases = total_cases[-1]
       
            # count how many new cases there are
            day_new_cases = compute_new(day, day_total_cases, doubles_in_days)

            # use previous day end total cases as base
            day_expired_cases = compute_expired(day_total_cases, case_fatality_rate, mean_duration)

            # end of day total cases before releasing patients
            day_total_cases = day_total_cases + day_new_cases - day_expired_cases
            
            # release patients
            if day > mean_duration:
                day_total_cases = day_total_cases - (new_cases[-mean_duration] - day_expired_cases)
            
            # end of day total demand
            day_demand_cases = day_total_cases + day_new_cases
            
            # add case data to combination outputs
            demand_cases.append(int(day_demand_cases))
            new_cases.append(int(day_new_cases))
            total_cases.append(int(day_total_cases))
            expired_cases.append(int(day_expired_cases))
            
            # day ends
        
        patient_id = random.randint(1000000000000, 9999999999999)
        
        out.append([patient_id,
                    max(demand_cases),   # get the peak demand
                    max(total_cases),    # get the peak actual cases (concurrent ICU stays)
                    sum(new_cases),      # get the total number of new cases
                    sum(expired_cases),  # get the total number of those expired
                    combination[0],
                    combination[1],
                    combination[2],
                    combination[3]])
                   
        # combination ends
        
    df = pd.DataFrame(out)
    df.columns = ['id',
                  'demand_cases',
                  'total_cases',
                  'new_cases',
                  'expired_cases',
                  'capacity',
                  'doubles_in_days',
                  'mean_duration',
                  'case_fatality_rate']
                   
    return df

# total_demand

params = {'capacity': [150, 500, 10],
          'doubles_in_days': [5, 8, 1],
          'mean_duration': [17, 23, 1],
          'case_fatality_rate': [0.4, 0.6, 0.01]}
#results = simulate(params, randomize=True, debug_limit=1)
results = simulate(params)
