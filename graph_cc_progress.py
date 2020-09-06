#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import datetime
import metadata

def get_chord_string(filename):
    c1, c2 = filename.strip(".txt").split("_")
    base_chars = "abcdefg"
    upper_map = str.maketrans(base_chars, base_chars.upper())
    c1 = c1.translate(upper_map)
    c2 = c2.translate(upper_map)
    return c1 + " - " + c2

def get_plot():
    # Look pretty
    plt.style.use('seaborn-whitegrid')
    ax = plt.axes()
    # Use whole numbers on the axes
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))
    # Labels and title
    ax.set_ylabel('Chord Changes per Minute')
    ax.set_xlabel('Days Practicing')
    ax.set_title('Chord Change Progress')
    return ax

def plot_data(data, files, start_date):
    ax = get_plot()

    num_lines = len(files)
    for i in range(num_lines):
        label = get_chord_string(files[i])
        dates = [x["date_offset"] + 1 for x in data[i]]
        counts = [x["count"] for x in data[i]]
        ax.plot(dates, counts, marker='o', label=label)
    ax.legend()


def get_data(files, start_date):
    num_files = len(files)
    # [[{date, count}, ...], ...]
    # Chord names related to data by matching index from `data` to `files`
    data = [[] for i in range(num_files)]
    for f in range(num_files):
        lines = open(os.path.join(metadata.data_path, files[f]), 'r').read().splitlines()
        num_lines = len(lines)
        data[f] = [{"date_offset": 0, "count": 0} for i in range(num_lines)]
        for l in range(num_lines):
            date_str, count_str = lines[l].split()
            data[f][l]["date_offset"] = (datetime.datetime.strptime(date_str, '%Y.%m.%d') - start_date).days
            data[f][l]["count"] = int(count_str)
    return data

def get_start_date():
    # TODO: Test failure
    return datetime.datetime.strptime(metadata.start_date, '%Y.%m.%d')

def data_path_is_valid():
    return os.path.exists(metadata.data_path) and os.path.isdir(metadata.data_path)

def main():
    # Validate path to chord change data
    if not data_path_is_valid():
        print("data_path in metadata.py is invalid.\nPlease fix metadata.py and try again.")
        return
    # Get file names from chord change data path
    files = os.listdir(metadata.data_path)
    # Parse the start date into datetime object
    start_date = get_start_date()
    # Parse and format data from all data files
    data = get_data(files, start_date)
    # Plot it!
    plot_data(data, files, start_date)
    plt.savefig('guitar_progress.png', bbox_inches='tight')
    #plt.show()

if __name__ == "__main__":
    main()
