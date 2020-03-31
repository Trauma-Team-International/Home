## Snapshot Method

First get the [code](https://github.com/autonomio/trauma-team-international/blob/master/icu_burden/icu_burden_snapshot.py) on to your machine, and then in the same folder:

```
params = {'capacity': [100, 1000, 1],
          'doubles_in_days': [2, 20, 1],
          'case_fatality_rate': [0.2, 0.6, 0.01]}

results = simulate(params)
```
