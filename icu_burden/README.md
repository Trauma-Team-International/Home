# Forecasting ICU Burden and Fatalities Caused by Capacity Issues

Below, several methods are provided for answering the question `how much ICU burden will there be` and `how much fatalities will be caused by excess demand for ICU beds`. These methods are provided to test and challenge outputs provided by opaque models that are based on undisclosed complexity and caveats. Each method provided below have been provided with auditability and absence of complexity in mind. The [Robust Event-Based Simulator](#robust-event-based-method) can be used as a single pipeline with one of the [provided SEIR methods](https://github.com/autonomio/trauma-team-international/tree/master/SEIR) as an input for number of infections.

## Snapshot Method

DATA SOURCE: generated based on input parameters
FOCUS: to evaluate outcomes of every possible parameter combination
PARAMETERS: `capacity`, `doubles_in_days`, and `case_fatality_rate`

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

## Robust Event-Based Method

A high resolution event-based ICU burden simulator. Number of infections can be used as an input from SEIR or other similar infectious disease focused model.

- **DATA SOURCE:** generated based on input parameters
- **FOCUS:** to evaluate outcomes of every possible parameter combination
- **PARAMETERS:** see below

parameter | type | description
--- | --- | ---
days_to_simulate | int | total days to be simulated
doubles_in_days | int | number of days it takes to double incoming ICU cases
starting_standard_icu_count | int | the number of initial ICU patients (on day 0 of stay)
starting_ventilated_icu_count | int | the number of initial ventilated patients (on day 0 of stay)
standard_icu_capacity | int | total number of available standard ICU beds
ventilated_icu_capacity | int | total number of available ventilated ICU beds
standard_icu_fatality_rate | float | percentage (e.g. 0.1 means 10%) of ICU cases that die 
ventilated_icu_fatality_rate | float | percentage (e.g. 0.1 means 10%) of ventilated cases that die
standard_icu_stay_duration | float | mean duration of ICU stay in days
ventilated_icu_stay_duration | float | mean duration of ICU ventilation in days

The logic is based on the following rules:

- there is a certain number of patients at start day_total_cases
- each day there are more new patients based on doubles_in_days
- each day some patients will die based on case_fatality_rate
- each day some patients are released based on mean_duration
    - all patients that meet mean_duration and did not die are released
- some patients can be admitted based on current available capacity
    - such patients will be added to day_total_cases
- some patients may not be admittable due to lack of current capacity
    - such patients will die
    
Capacity specific logic:

- if capacity not full:
  - patient is admitted
  - patient will have some change to die
  - every hour it is decided if the person is going to die or not*

- if needs ventilation:
  - patient chance to die will change
  - every hour it is decided if the person is going to die or not*
 
- if capacity is full:
  - patient will immediately die

*The way in which death (and release) are computed, results in normally distributed duration of stay, with separate means for recovered, standard ICU and ventilated ICU.

First get the [code](https://github.com/autonomio/trauma-team-international/blob/master/icu_burden/icu_burden_simulator.py) on to your machine, and then run it.

## Bayesian Method

**DATA SOURCE:** daily country-level case or death numbers
**FOCUS:** to evaluate the strength of historical trend as a proxy for forecasting the future
**PARAMETERS:** NA

GLM pipeline for using Bayesian method for linear regression, where the historical trend is used to predict future events.

Get the [code](https://github.com/autonomio/trauma-team-international/blob/master/icu_burden/icu_burden_bayesian.py) on to your machine, and run it.

## Moving Average Method

**DATA SOURCE:** daily country-level case or death numbers
**FOCUS:** to evaluate how precise the most simplistic available method is in forecasting the future
**PARAMETERS:** NA

A moving average based baseline method, where historical trend is used to predict future events across all countries with COVID-19 cases. Provides as output mean-average-error and relative-median-error for each country.

First get the [code](https://github.com/autonomio/trauma-team-international/blob/master/icu_burden/icu_burden_average.py) on to your machine, and then run it.
