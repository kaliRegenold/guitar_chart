#!/usr/bin/env python3

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import re
import datetime

plt.style.use('seaborn-whitegrid')
fig = plt.figure()
ax = plt.axes()
for axis in [ax.xaxis, ax.yaxis]:
    axis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.set_ylabel('Chord Changes per Minute')
ax.set_xlabel('Days Practicing')
ax.set_title('Chord Change Progress')
min_date = datetime.datetime.strptime('2020.08.24', '%Y.%m.%d')

# Get all chord change files in the current directory
def get_files():
    # Get current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Regex to match data files
    regex = re.compile('[a-g]_[a-g]_chord_change\.txt')

    # Get all data files from current directory
    return [file for file in os.listdir(dir_path) if re.match(regex, file)]

# Parse data from a single file
def get_data(file_name):
    # Store dates and respective chord change counts separate
    dates = []
    chord_changes = []

    # Store all non-empty lines
    lines = open(file_name, 'r').read().splitlines()

    # Parse lines for date and chord change count
    for line in lines:
        l = line.split(' ')
        dates.append(datetime.datetime.strptime(l[0], '%Y.%m.%d'))
        chord_changes.append(int(l[1]))

    chord_names = file_name.split('_')
    chord_change_string = '' + chord_names[0] + ' - ' + chord_names[1]

    return (dates, chord_changes, chord_change_string)

def plot_data(dates, chord_changes, chord_change_string):
    num_days = [(date - min_date).days + 1 for date in dates]
    ax.plot(num_days, chord_changes, marker='o', label=chord_change_string)
    ax.legend()

file_names = get_files()
for file in file_names:
    d, cc, cc_string = get_data(file)
    plot_data(d, cc, cc_string)
plt.savefig('guitar_progress.png', bbox_inches='tight')
# plt.show()
