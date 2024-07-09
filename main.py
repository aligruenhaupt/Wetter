import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tk.END)
        else:
            self.position = len(self.get())
        _hits = []
        for item in self._completion_list:
            if item.lower().startswith(self.get().lower()):
                _hits.append(item)
        self._hits = _hits
        if _hits:
            self._hit_index %= len(_hits)
            self.set_completion_text()

    def set_completion_text(self):
        self.position = len(self.get())
        self.delete(0, tk.END)
        self.insert(0, self._hits[self._hit_index])
        self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 'Shift', 'Control'):
            return
        if event.keysym == 'Return':
            self.set_completion_text()
        else:
            self.autocomplete()
            self.icursor(tk.END)

def fetch_weather_data(station_id):
    url = f"https://app-prod-ws.warnwetter.de/v30/stationOverviewExtended?stationIds={station_id}"
    try:
        print(f"Fetching data from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def process_weather_data(api_data, station_id):
    try:
        if station_id in api_data and 'days' in api_data[station_id]:
            days_data = api_data[station_id]['days']
            df = pd.DataFrame(days_data)
            df['dayDate'] = pd.to_datetime(df['dayDate'])  # Convert 'dayDate' to datetime format
            df['temperatureMax'] = df['temperatureMax'] / 10
            df['temperatureMin'] = df['temperatureMin'] / 10
            return df
        else:
            print(f"No valid data found for station ID {station_id}.")
            return None
    except KeyError as e:
        print(f"KeyError: {e}")
        return None

def plot_temperature_data(station_id, station_name, plot_canvas):
    if plot_canvas:
        plot_canvas.get_tk_widget().destroy()

    api_data = fetch_weather_data(station_id)
    if api_data:
        df = process_weather_data(api_data, station_id)
        if df is not None:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['dayDate'], df['temperatureMax'], marker='o', linestyle='-', color='r', label='Max Temperature')
            ax.plot(df['dayDate'], df['temperatureMin'], marker='o', linestyle='-', color='b', label='Min Temperature')
            ax.set_xlabel('Date')
            ax.set_ylabel('Temperature (°C)')
            ax.set_title(f'Max and Min Temperatures for Station {station_name} (ID: {station_id})')
            ax.legend()
            ax.grid(True)
            fig.autofmt_xdate(rotation=45)

            plot_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            plot_canvas.draw()
            plot_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            return plot_canvas  # Return the new plot_canvas
        else:
            print(f"Failed to process weather data for station ID {station_id}.")
    else:
        print(f"Failed to fetch API data for station ID {station_id}.")

def on_plot_button_click():
    global plot_canvas  # Use the global plot_canvas variable

    selected_station = station_id_var.get()
    if selected_station:
        station_name, station_id = selected_station.split(' - ')
        plot_canvas = plot_temperature_data(station_id, station_name, plot_canvas)
    else:
        messagebox.showwarning("Error", "Please select a station.")

def read_station_data(file_path):
    stations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    station_id, station_name = parts
                    stations.append(f"{station_name} - {station_id}")
    return stations

window = tk.Tk()
window.geometry("900x600")
window.title("Weather Data Plotter")

ttk.Label(window, text="Weather App by Muhammet Ali Yesilbas:", font=("Arial", 12)).pack(pady=10)
ttk.Label(window, text="Select City:", font=("Arial", 18)).pack(pady=10)
station_id_var = tk.StringVar()

station_data = read_station_data('cleaned_stations.txt')

station_id_dropdown = AutocompleteCombobox(window, textvariable=station_id_var, width=60)
station_id_dropdown.set_completion_list(station_data)
station_id_dropdown.pack()

plot_frame = tk.Frame(window)
plot_frame.pack(pady=20)

plot_button = ttk.Button(window, text="Plot Weather Data", command=on_plot_button_click)
plot_button.pack(pady=10)

plot_canvas = None

window.mainloop()
