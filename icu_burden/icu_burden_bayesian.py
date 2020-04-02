# https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

data = pd.read_csv('COVID-19-geographic-disbtribution-worldwide.csv')
data.dateRep = pd.DatetimeIndex(data.dateRep)
temp = data[data.countriesAndTerritories == 'Finland'].sort_values('dateRep')['cases']
temp = temp[temp > 0]

x = temp.shift(3)[3:].astype(int).values
y = temp[3:].values

import pymc3 as pm
import matplotlib.pyplot as plt

with pm.Model() as linear_model:
    
    # Intercept
    intercept = pm.Normal('Intercept', mu=0, sd=10)
    
    # Slope 
    slope = pm.Normal('slope', mu=0, sd=10)
    
    # Standard deviation
    sigma = pm.HalfNormal('sigma', sd=10)
    
    # Estimate of mean
    mean = intercept + slope * x
    
    # Observed values
    Y_obs = pm.Normal('Y_obs', mu = mean, sd = sigma, observed = y)
    
    # Sampler
    step = pm.NUTS()

    # Posterior distribution
    linear_trace = pm.sample(5000, step, tune=5000, cores=20)
    
plt.figure(figsize=(7, 7))
pm.traceplot(linear_trace[100:])
plt.tight_layout(); 
