import os
import pandas as pd
import matplotlib.pyplot as plt

from os.path import abspath, join
from pandas import DataFrame

basedir = abspath(os.path.dirname(__file__))
csv_files = join(basedir, 'csv_files')


def percentage(part: float, tot: float) -> float:
    return part * 100 / tot


if __name__ == "__main__":
    test_vs_confirmed_cases_csv = join(csv_files, 'tests-vs-confirmed-cases-covid-19.csv')
    data: DataFrame = pd.read_csv(test_vs_confirmed_cases_csv)
    data_testvscases = data[
        data['Year'].eq(56) &
        data['Total number of tests for COVID-19'].notnull() &
        data['Total confirmed cases of COVID-19'].notnull()
    ]

    population_csv = join(csv_files, 'population.csv')
    data: DataFrame = pd.read_csv(population_csv)
    data_population = data.loc[data['Year'].eq(2016), ['Country Code', 'Value']]

    md = pd.merge(data_testvscases, data_population, left_on='Code', right_on='Country Code')
    md['Test/Population'] = md.apply(
        lambda x: percentage(x['Total number of tests for COVID-19'], x['Value']),
        axis=1
    )
    md['Confirmed/Population'] = md.apply(
        lambda x: percentage(x['Total confirmed cases of COVID-19'], x['Value']),
        axis=1
    )
    res = md[['Entity', 'Test/Population', 'Confirmed/Population']].sort_values('Test/Population', ascending=False)

    print(res.to_string())

    x = res['Confirmed/Population'].to_numpy()
    y = res['Test/Population'].to_numpy()
    labels = res['Entity'].to_numpy()
    fig, ax = plt.subplots()
    ax.set_xlabel('Test/Population')
    ax.set_ylabel('Confirmed/Population')
    ax.scatter(x, y)
    for i, txt in enumerate(labels):
        ax.annotate(txt, xy=(x[i], y[i]))
    fig.show()
