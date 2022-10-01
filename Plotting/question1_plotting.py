'''
Authors: Roman Blotsky (1168123), Mehtab Kaur (1054984), Kirisan Suthanthireswaran (1186029)
Last Updated: (15-03-2022)

Functionality:
  This file will take a number of command line arguments including a data file, an output file, and a timeframe to plot. It will take the data between the given timeframe from the data file, write it to the output file, and then create a plot from that file using imported libraries. The output is written to standard output unless redirected to a file (recommended to redirect to a PDF)

  There are 8 commandline arguments and 1 optional argument: 
    - q1_processed_file (string)
    - q1_plotting_file (string)
    - start_year (integer)
    - start_month (integer)
    - start_day (integer)
    - end_year (integer)
    - end_month (integer)
    - end_day (integer)
    - graphics_file (string)
    - debugOn (integer, optional)

To run on commandline:
python Plotting/question1_plotting.py question1_preprocessed.csv question1_plotted_data.csv 2020 8 10 2022 3 10 plot1.pdf
'''

# Packages/Modules #
import sys
import csv
import datetime
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker as ticktools


# CONSTANTS #
NUM_X_TICKS = 5

# MAIN FUNCTION #
def main(argv):

  # Ensures a valid amount of commandline arguments passed
  if len(argv) < 10:
    print("Usage: question1_plotting.py <q1_preprocessed_file>  <q1_plotting_file> <start_year> <start_month> <start_day> <end_year> <end_month> <end_day> <graphics_file> <debugOn (optional)>")

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

  try:
    q1_preprocessed_file = open(argv[1], encoding="utf-8-sig");
  except IOError:
    print(f"Could not open \"q1_preprocessed_file\" from arguments: {argv[1]} is an invalid file path!", file=sys.stderr)
    sys.exit(1)

  try:
    q1_plotting_file = open(argv[2],"w",encoding="utf-8-sig")
  except IOError:
    print(f"Could not create \"q1_plotting_file\" from arguments: {argv[2]} is invalid or cannot be overwritten!", file=sys.stderr)
    sys.exit(1)

  graphics_filename = argv[9]

  # Stores optional debugOn argument.
  # This displays debug information in stderr if set to on. Major errors that cause program exit will still be displayed if it is False.
  try:
    debugOn = bool(int(argv[10]) > 0)
  except:
    debugOn = False
  
  # Stores current row index
  current_row_index = 0
  
  # Creates a CSV reader from q1 preprocessed file
  q1_reader = csv.reader(q1_preprocessed_file)

  # Writes column headers
  q1_plotting_file.write("Date,% of Population in ICU,Vaccination Status\n")

  # Loops through all rows in q1_preprocessed_file
  for row_data in q1_reader:

    # Ignores first row
    if row_data[0] == "date":
      current_row_index += 1
      continue

    # Ensures there are at least 4 columns, terminates if not.
    if len(row_data) < 4:
      print(f"Row {current_row_index} has too few columns! Needs: 4, Has: {len(row_data)}", file=sys.stderr)
      sys.exit(1)
    
    # Takes data from the file
    try:
      date = datetime.date.fromisoformat(row_data[0])
    except ValueError:
      print(f"Could not convert \"{row_data[0]}\" to a date on row {current_row_index}", file=sys.stderr)
      date=datetime.date.min

    unvac_percent = row_data[1]
    partial_vac_percent = row_data[2]
    full_vac_percent = row_data[3]

    # If the date is within range, prints it to the new plotting data file
    if date >= start_date and date <= end_date:
      q1_plotting_file.write(f"{date},{unvac_percent},Unvaccinated\n")
      q1_plotting_file.write(f"{date},{partial_vac_percent},Partially Vaccinated\n")
      q1_plotting_file.write(f"{date},{full_vac_percent},Fully Vaccinated\n")

  # Closes file
  q1_plotting_file.close()
  
  # Starts plotting #
  # Creates CSV reader for the plotting file
  try:
    q1_plotter = pd.read_csv(argv[2])
  except IOError as err:
    print("Unable to open generated CSV file", argv[2],
      ": {}".format(err), file=sys.stderr)
    sys.exit(-1)

  # If debugging, prints out the file frame (all data in the file nicely formatted)
  if debugOn:
    print(q1_plotter)

  # Generate a figure for the seaborn library to draw in.
  fig = plt.figure()

  # Creates a lineplot using seaborn 
  # (Each name here must have the same name as its column in the CSV file)
  ax = sns.lineplot(x = "Date", y = "% of Population in ICU", hue="Vaccination Status", data=q1_plotter)

  # Set the max number of axis labels to NUM_X_TICKS, to avoid having ticks for each date
  ax.xaxis.set_major_locator(ticktools.MaxNLocator(NUM_X_TICKS))

  # Rotate the ticks on the x-axis to 45 degrees
  plt.xticks(rotation = 45, ha = 'right')

  # Saves the fig to a file
  fig.savefig(graphics_filename, bbox_inches="tight")

  # Uncomment this line to show the figure on the screen.
  # (May need to use [CTR+C] to close the display after)
  #plt.show()
  
  #
  # END OF MAIN
  #

# Runs main
main(sys.argv)