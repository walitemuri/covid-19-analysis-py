'''
Authors: Roman Blotsky (1168123), Mehtab Kaur (1054984), Kirisan Suthanthireswaran (1186029) Wali Temuri (1183379)
Last Updated: (22-03-2022)

Functionality:
  This file will take a number of command line arguments including a data file, an output file, timeframe and output filename to plot. It will take the data between the given timeframe from the data file, write it to the output file, and then create a plot from that file using imported libraries. The output is written to standard output unless redirected to a file (recommended to redirect to a PDF)

  There are 9 commandline arguments and 1 optional argument: 
    - q3_processed_file (string)
    - q3_plotting_file (string)
    - start_year (integer)
    - start_month (integer)
    - start_day (integer)
    - end_year (integer)
    - end_month (integer)
    - end_day (integer)
    - graphic file (string)
    - debugOn (integer, optional)

To run on commandline:
python Plotting/question3_plotting.py question3_preprocessed.csv question3_plotted_data.csv 2021 8 10 2022 1 29 plot3.pdf
'''

# Packages/Modules #
import sys
import csv
import datetime
import pandas as pd

import seaborn as sns
from matplotlib import pyplot as plt

# this imports tools for "ticks" along the x and y-axes and calls them "ticktools"
from matplotlib import ticker as ticktools

# MAIN FUNCTION #
def main(argv):

  # Ensures a valid amount of commandline arguments passed
  if len(argv) < 9:
    print("Usage: question2_plotting.py <q3_preprocessed_file>  <q3_plotting_file> <start_year> <start_month> <start_day> <end_year> <end_month> <end_day> <graphic file> <debugOn (optional)>")

  # Stores all the arguments
  try:
    start_date = datetime.date(int(argv[3]), int(argv[4]), int(argv[5]))
  except ValueError:
    print(f"Invalid input given for start date! Must be integers, received: {argv[3]} {argv[4]} {argv[5]}", file=sys.stderr)
    sys.exit(1)

  try:
    end_date = datetime.date(int(argv[6]), int(argv[7]), int(argv[8]))
  except ValueError:
    print(f"Invalid input given for end date! Must be integers, received: {argv[6]} {argv[7]} {argv[8]}", file=sys.stderr)
    sys.exit(1)

  #PDF file name will be given as cmnd line arg
  output_file = argv[9]
  #try to open preprocessed file
  try:
    q3PreprocessedFile = open(argv[1], encoding="utf-8-sig")
  except IOError:
    print(f"Could not open \"q3_preprocessed_file\" from arguments: {argv[1]} is an invalid file path!", file=sys.stderr)
    sys.exit(1)

  #try to create plotting file
  try:
    q3PlottingFile = open(argv[2],"w", encoding="utf-8-sig")
  except IOError:
    print(f"Could not create \"q3_plotting_file\" from arguments: {argv[2]} is an invalid or cannot be overwritten!", file=sys.stderr)
    sys.exit(1)


  # Stores optional debugOn argument.
  # This displays debug information in stderr if set to on.
  try:
    debugOn = bool(int(argv[2]) > 0)
  except:
    debugOn = False 

  #store current line num
  currentRow = 0;

  #Initializing read variable for Q3 preprocessed file
  q3Read = csv.reader(q3PreprocessedFile)

  #Writing first line outlining parameters
  q3PlottingFile.write("Date,Number of Cases,Age Group\n")

  #Loops through preprocessed file row_data by row_data
  for row_data in q3Read:

    #Skips first row_data 
    if row_data[0] == "Accurate_Episode_Date" or row_data[1] == "UNKNOWN":
      currentRow += 1
      continue

    #Ensures the row_data has 3 columuns
    if len(row_data) < 3:
      print(f"Row {currentRow} has too few columns, Needs 3, Has: {len(row_data)}", file=sys.stderr)
      sys.exit(1)

    #Extracting time info from file
    try:
      date = datetime.date.fromisoformat(row_data[0])
    except ValueError:
      print(f"Could not convert \"{row_data[0]}\"to a date on row_data {currentRow}", file=sys.stderr)
      date = datetime.date.min

    #Initializing and assigning variables to corresponding columns in file
    age_group = row_data[1]
    number_cases = row_data[2]

    #Ensures date entered is within range
    if date >= start_date and date <= end_date:
      q3PlottingFile.write(f"{date}, {number_cases}, {age_group}\n")

    #Closes file
  q3PlottingFile.close()

  # START PLOTTING HERE #

  #Try opening the plotting csv file 
  try:
    q3Plot = pd.read_csv(argv[2])
  except IOError as err:
    print("Unable to open generated CSV file", argv[2],       ": {}".format(err), file=sys.stderr)
    sys.exit(0)

  if debugOn:
    print(q3Plot)

  #Declaring and setting figure size for the seaborn lineplot
  figure = plt.figure(figsize = (12,6))

  #Setting variables to the appropriate parameters, setting line width = 2
  ax = sns.lineplot(x = "Date", y = "Number of Cases",hue = "Age Group", data=q3Plot)

  #Setting number of ticks across the x-axis representing time to 5
  ax.xaxis.set_major_locator(ticktools.MaxNLocator(5))

  #Rotating the ticks by 45 degrees and setting horizontal ticks to right side
  plt.xticks(rotation = 45, ha = 'right')

  #Saving figure using the output file format
  figure.savefig(output_file, bbox_inches = "tight")
#
# END OF MAIN
#

# Runs main
main(sys.argv)