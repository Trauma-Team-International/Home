# requires the file from https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863 to be converted into csv.

def rolling_average(window=5):

    data = pd.read_csv('COVID-19-geographic-disbtribution-worldwide.csv')
    
    out = [] 

    for country in data.countriesAndTerritories.unique():

        cases = data[data.countriesAndTerritories == country].sort_values('dateRep').cases
        cases = cases[cases > 0]
        rolling = cases.rolling(window).mean()

        mae = abs(cases - rolling).mean()
        rame = (abs(cases - rolling) / cases).median()

        out.append([country, mae, rame, sum(cases)])

    df = pd.DataFrame(out)
    df.columns = ['country', 'mae', 'rame', 'total_cases']
    
    return df
