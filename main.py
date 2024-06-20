import requests
import pandas
import matplotlib.pyplot as plt


def process_weather_data(raw_data, station):
    processed_data = []
    for day in raw_data[station]['days']:
        processed_day = {
            'date': day['dayDate'],
            'temperature_max_celsius': (day['temperatureMax'] / 10.0),
            'temperature_min_celsius': (day['temperatureMin'] / 10.0),
            'precipitation': day['precipitation'],
            'wind_speed': day['windSpeed'],
            'sunshine': day['sunshine']
        }
        processed_data.append(processed_day)
    return pandas.DataFrame(processed_data)


