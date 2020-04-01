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
