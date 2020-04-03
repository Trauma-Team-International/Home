## Snapshot Method

First get the [code](https://github.com/autonomio/trauma-team-international/blob/master/icu_burden/icu_burden_snapshot.py) on to your machine, and then in :

```
from icu_burden_snapshot import simulate

# define the parameter ranges as start, stop, and step
params = {'capacity': [200, 1000, 50],
          'doubles_in_days': [3, 8, 1],
          'case_fatality_rate': [0.2, 0.6, 0.01]}

# store simulation result dataframe
results = simulate(params)
```

#### TODO

- [ ] add tiny randomness into inferred values
- [ ] add quantile visualization option
- [ ] refactor the code
- [ ] structure as self-contained module
- [ ] add starting value and number of days as input variables

## Robust Event-Based Simulator Method

Provides a simple interface with industrial event-based simulator based on the below logic.

- there is a certain number of patients at start day_total_cases
- each day there are more new patients based on doubles_in_days
- each day some patients will die based on case_fatality_rate
- each day some patients are released based on mean_duration
    - all patients that meet mean_duration and did not die are released
- some patients can be admitted based on current available capacity
    - such patients will be added to day_total_cases
- some patients may not be admittable due to lack of current capacity
    - such patients will die
    
First get the [code](https://github.com/autonomio/trauma-team-international/blob/master/icu_burden/icu_burden_simulator.py) on to your machine, and then run it.

