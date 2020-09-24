#!/usr/bin/env python
# run with "python weather_stations.py"
# takes about 7 seconds per method being applied to the large csv.

import unittest
import csv
from typing import Iterable
from collections import defaultdict

STATION_ID_INDEX = 0
DATE_INDEX = 1
TEMPERATURE_INDEX = 2

# parse the csv rows and return them as a list
# not as memory efficient as a generator, but saves a lot of time if we need to iterate over this list more than once.
def get_csv_rows():
	with open('data.csv', 'r') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		next(r) # skip header row
		rows = []
		for row in r:
			rows.append((int(row[STATION_ID_INDEX]), float(row[DATE_INDEX]), float(row[TEMPERATURE_INDEX])))
		return rows


# create a generator to load the rows from the csv, and parse integers/decimals
# we use a generator because the dataset is massive and we don't want to keep it in memory.
def get_csv_rows_generator():
	with open('data.csv', 'r') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		next(r) # skip header row
		for row in r:
			yield (int(row[STATION_ID_INDEX]), float(row[DATE_INDEX]), float(row[TEMPERATURE_INDEX]))


# input of form [(1, 2000.001, 5), (2, 2000.001, 6), ...]
# output station that had the coldest temperature
def get_minimum_temperature_station(station_temperatures: Iterable) -> int:
	return min(station_temperatures, key = lambda s: s[TEMPERATURE_INDEX])[STATION_ID_INDEX]


# input of form [(1, 2000.001, 5), (2, 2000.001, 6), ...]
# creates a dict of {station_id: (last_temp, total_flux)}
# then take max(flux) to determine the station
# output station that had the coldest temperature
def get_max_fluctuation_station(station_temperatures: Iterable) -> int:

	# create a dict of station_id: (current_temp, total_flux) we'll use to accumulate the total change in temp
	flux_dict = {}
	# iterate through the station inputs and accumulate the total fluctuation in temp for each station
	for station_temperature in station_temperatures:
		station_id = station_temperature[STATION_ID_INDEX]
		new_temp = station_temperature[TEMPERATURE_INDEX]
		if station_id in flux_dict:
			old_temp, total_flux = flux_dict[station_id]
			flux_dict[station_id] = (new_temp, total_flux + abs(new_temp - old_temp))
		else:
			flux_dict[station_id] = (new_temp, 0.0)

	# now get the station with the highest flux by iterating the dict grabbing the max of total flux
	# reminder dictionary is in form {station_id: (last_temp, total_flux)}
	return max(flux_dict.items(), key = lambda kv: kv[1][1])[0]


# Same behavior as get_max_fluctuation_station(), except it only proccesses entries that fit the date range.
def get_max_fluctuation_dates_specified(station_temperatures: Iterable, start_date: float, end_date: float) -> int:

	# create a dict of station_id: (current_temp, total_flux) we'll use to accumulate the total change in temp
	flux_dict = {}
	# iterate through the station inputs and accumulate the total fluctuation in temp for each station
	for station_temperature in station_temperatures:
		if start_date <= station_temperature[DATE_INDEX] <= end_date:
			station_id = station_temperature[STATION_ID_INDEX]
			new_temp = station_temperature[TEMPERATURE_INDEX]
			if station_id in flux_dict:
				old_temp, total_flux = flux_dict[station_id]
				flux_dict[station_id] = (new_temp, total_flux + abs(new_temp - old_temp))
			else:
				flux_dict[station_id] = (new_temp, 0.0)

	return max(flux_dict.items(), key = lambda kv: kv[1][1])[0]



class TestWeatherStationMethods(unittest.TestCase):

	def test_basic(self):
		test_input = [(1, 2000.001, 5), (2, 2000.001, 20), (3, 2000.001, -1), \
			(1, 2000.002, -3), (2, 2000.002, -1), (1, 2000.003, 1), (2, 2000.003, -2)]
		expected_min_temp_station_id = 1
		expected_max_flux_station_id = 2

		self.assertEqual(get_minimum_temperature_station(test_input), expected_min_temp_station_id)
		self.assertEqual(get_max_fluctuation_station(test_input), expected_max_flux_station_id)

		start_date, end_date = 2000.002, 2000.004
		expected_max_flux_date_specified_station_id = 1
		self.assertEqual(get_max_fluctuation_dates_specified(test_input, start_date, end_date), \
			expected_max_flux_date_specified_station_id)


	def test_csv(self):
		expected_min_temp_station_id = 676223
		expected_max_flux_station_id = 735181

		# load the input into memory, as we use it more than once. can swap this out with the generator function
		# to save memory and increase time if desired.
		input_rows = get_csv_rows()
		self.assertEqual(get_minimum_temperature_station(input_rows), expected_min_temp_station_id)
		self.assertEqual(get_max_fluctuation_station(input_rows), expected_max_flux_station_id)

		start_date, end_date = 2001.0, 2002.0
		expected_max_flux_date_specified_station_id = 756020
		self.assertEqual(get_max_fluctuation_dates_specified(input_rows, start_date, end_date), \
			expected_max_flux_date_specified_station_id)
		


if __name__ == '__main__':
	unittest.main(verbosity=2)
