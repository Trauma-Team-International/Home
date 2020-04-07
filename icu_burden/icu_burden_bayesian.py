# https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863

#! /usr/bin/env python

import pandas as pd
import numpy as np
import pymc3 as pm
import matplotlib.pyplot as plt
import matplotlib.dates as pld  # from .. import (YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange)
import matplotlib.ticker as ticker


# https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863
data = pd.read_csv('COVID-19__2020_4_6.csv')  # geographic-distribution-worldwide.csv')
# DatetimeIndex(data.dateRep)   # probably takes month as day or something
data['dates'] = pd.to_datetime(data.dateRep, dayfirst=True)
countries = data.countriesAndTerritories.unique()
countries = sorted(countries)
# data.dateRep.describe()
# data.dateRep


def plot_country(country, log='lin', end=None, start=None):
    """
    plot the cases of given country
    :param country: Country name
    :param log: 'log' if logarithmic plot
    :param end:  end datetime to plot x-range
    :param start: start datetime
    :return:
    """
    if country=='all' or country=='World':
        temp = data.sort_values('dates')
    else:
        temp = data[data.countriesAndTerritories == country].sort_values('dates')
    if temp.shape[0]==0:  # check that country exists in data
        print('Country %s not found in data'%country)
        # countries = temp.countriesAndTerritories.unique()
        print(countries)
        return

    # check that there are none zero values in cases or deaths
    if start == None:
        first_date2 = next((ti['dates'] for ind, ti in temp.iterrows() if ti['deaths'] > 0 or ti['cases'] > 1), None)
        first_date = next((ti['dates'] for ind, ti in temp.iterrows() if ti['deaths'] > 0 or ti['cases'] > 0), None)
        if first_date == None:
            print('no cases or deaths for country ', country)
            return
    else:
        first_date2 = None
        first_date = start
    # country = 'Finland'  # Italy
    # print(temp.cases.cumsum())
    # print(temp.dateRep)
    temp = temp[temp.dates>= first_date]
    if end is None:
        end = temp.dates.max()
        print('date range with non-zero data: \n', first_date, '-', end)  # pld.num2date(xlim[1])
    #         ax.set_xlim(pld.date2num(first_date), xlim[1])
    else:
        print('date range with non-zero data: \n', first_date, '-', end)
        temp = temp[temp.date <= end]
    #         ax.set_xlim(pld.date2num([first_date, end]))

    fig, ax = plt.subplots()
    # temp.plot(x='dateRep', y='cases')
    # temp.plot(x='dateRep', y='deaths')
    plt.plot_date(temp.dates, temp.cases.cumsum().values, 'o-', label='cases')
    plt.plot_date(temp.dates, temp.deaths.cumsum().values, 'o-', label='deaths')
    if log == "log":
        ax.set_yscale('log')

    fig.autofmt_xdate()
#     xlim = plt.xlim()

    # formatter = DateFormatter('%d.%m.%y')
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    # ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.title(country+' Cases and Deaths')
    plt.legend()

    return first_date2 if first_date2 is not None else None


def exp_model(x, y, expo=[0.7, 2], slope=[5, 10], intercept=[0, 30], sigma0=20):
    """
    likelihood function is y = intercept + slope * exp( x * exponent)
    :param x: datapoints
    :param y:  data
    :param expo:  exponent [mu and sigma]
    :param slope:
    :param intercept:
    :param sigma0: the variation of the result
    :return:  returns the model to fit_mc()
    """
    print('Exponential fit \n')
    with pm.Model() as exp_m:  # or exp_model = pm.Model()
        # model y ~ theta_1* exp(theta_2*x) + theta_3

        # Intercept  - theta_3
        intercept = pm.Normal('Intercept', mu=intercept[0], sd=intercept[1])
        # Slope   - theta_2
        slope = pm.Normal('slope', mu=slope[0], sd=slope[1])
        # Exponent  - theta_1
        expo = pm.Normal('expo', mu=expo[0], sd=expo[1])
        # Estimate of mean
        mean = slope * np.exp(expo * x) + intercept

        # Standard deviation
        sigma = pm.HalfNormal('sigma', sd=sigma0)
        # Observed values
        Y_obs = pm.Normal('Y_obs', mu=mean, sd=sigma, observed=y)
    return exp_m


# noinspection PyIncorrectDocstring
def poly_model(x, y, order, sigma0=30, **kwargs):
    """
    models any polynomial
    **kwargs allows any number of key word arguments
    The polynomial function is intercept + a1*x + a2*x**2 + a3*x**3 + ...
    Order N of the polynomial gives the last aN multiplier
    :param x: datapoints
    :param y: data
    :param order: order of the polynomial  0, 1, 2, ...
    :param intercept:  the constant [mu, sigma] - mu is center point, sigma is deviation in normal distribution
    :param a1: first order multiplier [mu, sigma]
    :param a2: second order multiplier [mu, sigma]
    ...
    :param aN: Nth order multiplier [mu, sigma]
    :return: returns the model to fit_mc()
    """
    args = []
    argvals = []
    intercept = [0, 20]
    for oi in range(1, order + 1):
        aN = 'a' + str(oi)
        args.append(aN)
        argvals.append([0, 10/oi])
#        if oi == 1:
#            argdict = dict([(aN, argvals[-1])])
#        else:
#            argdict[aN] = argvals[-1]

    print('%d-order polynomial fit \n args: intercept, '%order, args)
    for key, value in kwargs.items():
        if key == 'intercept':
            intercept = value  # [mu, sigma]
        elif key[0] == 'a' and int(key[1:])<=order:
            argvals[int(key[1:])-1] = value  # [mu, sigma]
            exec('key = value')
        else:
            print('argument %s not used'%key)

    with pm.Model() as poly_m:  # or exp_model = pm.Model()
        # model y ~ a1*x + a2*x**2 + a3*x**3 +.. + intercept

        # Intercept  - theta_3
        intercept = pm.Normal('Intercept', mu=intercept[0], sd=intercept[1])
        mean = intercept
        for ari, ar in enumerate(args):
            print('args[ari] = pm.Normal(args[ari], mu=%f, sd=%f)'
                  %(float(argvals[ari][0]), float(argvals[ari][1])), flush=True)
            exec('args[ari] = pm.Normal(args[ari], mu=%f, sd=%f)'
                 %(float(argvals[ari][0]), float(argvals[ari][1])))
            # Estimate of mean
            exec('mean += args[ari]*x**(ari+1)')  # aN*x**N

        # Standard deviation
        sigma = pm.HalfNormal('sigma', sd=sigma0)
        # Observed values
        Y_obs = pm.Normal('Y_obs', mu=mean, sd=sigma, observed=y)

    return poly_m


def fit_mc(country, ftype='poly1', samples=10000, startdate=None, enddate=None, **kwargs):
    """
    do monte carlo fit of posterior (gives also the point max estimate)

    :param country:
    :param samples: number of samples to use
    :param startdate: start date number
    :param enddate: end date number
    :return: fitresults
    """
    if country=="World" or country=="all":
        temp = data[data.countriesAndTerritories == country].sort_values('dates')
    else:
        temp = data[data.countriesAndTerritories == country].sort_values('dates')
    # temp = temp[temp > 0]

    # x = temp.shift(shift)[shift:].astype(int).values
    if startdate == None:
        startdate = temp[temp.cases > 1].dates.dt.date.min()  # timestamp
    if enddate == None:
        enddate = temp[temp.cases > 0].dates.dt.date.max()
    print('date range: ', startdate, enddate, flush=True)
    temp_new = temp[(temp.dates.dt.date>=startdate) & (temp.dates.dt.date<=enddate)]
    x0 = temp_new.dates.dt.date - startdate
    # print(x0.dt.days)
    x = x0.dt.days
    y = temp_new.cases.values
    # print(x, y)
    print('Number of data points: ', x.shape[0])  # , y.shape[0])

    if ftype=='exp':
        model = exp_model(x, y, **kwargs)
    elif 'poly' in ftype:
        order = int(ftype[4:])
        model = poly_model(x, y, order, **kwargs)
    else:
        print('undefined model - %s'%type)
        return None
    # find Maximum a posteriori  - a point estimate
    map_estimate = pm.find_MAP(model=model)
    print(map_estimate)

    # plot fit difference  - new function needed in AnalysisPlots.py
    # AnalysisPlots.fitEval(strings, x, data, fit)
    #  where strings = (function_str, title_str, x_label, y_label)
    #  and calculates mean difference, MSE, max-min deviation

    with model:
        # Sampler
        # step = pm.NUTS()
        # Posterior distribution
        step = pm.Slice()
        exp_trace = pm.sample(samples, step=step)  #, step, tune=2500, cores=10)
        # print(exp_trace)

    plt.figure(figsize=(7, 7))
    pm.traceplot(exp_trace[100:])
    plt.tight_layout()

    # pm.summary(exp_trace)  # some issue

    return exp_trace
