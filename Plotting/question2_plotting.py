'''
Authors: Roman Blotsky (1168123), Mehtab Kaur (1054984), Kirisan Suthanthireswaran (1186029)
Last Updated: (15-03-2022)

Functionality:
  This file will take a number of command line arguments including a data file, an output file, and a timeframe and school board to plot. It will take the data between the given timeframe from the data file, write it to the output file, and then create a plot from that file using imported libraries. The output is written to standard output unless redirected to a file (recommended to redirect to a PDF)

  There are 10 commandline arguments and 1 optional argument: 
    - q2_processed_file (string)
    - q2_plotting_file (string)
    - start_year (integer)
    - start_month (integer)
    - start_day (integer)
    - end_year (integer)
    - end_month (integer)
    - end_day (integer)
    - school_board (string)
    - graphics_filename (string)
    - debugOn (integer, optional)

To run on commandline:
python Plotting/question2_plotting.py question2_preprocessed.csv question2_plotted_data.csv 2020 8 10 2022 3 10 'Peel District School Board' plot2.pdf
'''

# Packages/Modules #
import sys
import csv
import datetime
import pandas as pd

# seaborn and matplotlib are for plotting.  The matplotlib
# library is the actual graphics library, and seaborn provides
# a nice interface to produce plots more easily.
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker as ticktools

# MAIN FUNCTION #
def main(argv):

  # Ensures a valid amount of commandline arguments passed
  if len(argv) < 11:
    print("Usage: question2_plotting.py <q2_preprocessed_file> <q2_plotting_file> <start_year> <start_month> <start_day> <end_year> <end_month> <end_day> <school_board> <graphics_filename> <debugOn (optional)>")

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

  # Try to open preprocessed file
  try:
    q2_preprocessed_file = open(argv[1], encoding="utf-8-sig")
  except IOError:
    print(f"Could not open \"q2_preprocessed_file\" from arguments: {argv[1]} is an invalid file path!", file=sys.stderr)
    sys.exit(1)

  # Try to create plotting file
  try:
    q2_plotting_file = open(argv[2],"w", encoding="utf-8-sig")
  except IOError:
    print(f"Could not create \"q2_plotting_file\" from arguments: {argv[2]} is an invalid or cannot be overwritten!", file=sys.stderr)
    sys.exit(1)

  school_board = argv[9]
  graphics_filename = argv[10]

  # Stores optional debugOn argument.
  # This displays debug information in stderr if set to on.
  try:
    debugOn = bool(int(argv[11]) > 0)
  except:
    debugOn = False 

  # Store current line num
  curr_line_num = 0;

  # Create CSV reader from q2 preprocessed file
  q2_preprocessed_reader = csv.reader(q2_preprocessed_file)

  # First line of output - header
  q2_plotting_file.write("Date,School Board,Confirmed School Cases\n")

  #loop through all rows in q2_preprocessed_file
  for row_data in q2_preprocessed_reader:
    #Skip first row - header
    if row_data[0] == "collected_date":
      curr_line_num += 1
      continue

    # If the row has less than the 3 required fields, prints error and stops
    if len(row_data) < 3:
      print(f"Row {curr_line_num} in q2_preprocessed_file has too few fields! Needs: 3, Has: {len(row_data)}", file=sys.stderr)
      sys.exit(1)

    # Extract date info from file
    try:
        date = datetime.date.fromisoformat(row_data[0]) 
    except ValueError:
        if debugOn:
          print(f"Could not convert \'{row_data[0]}'\ to a date for collected date (Row {curr_line_num})", file=sys.stderr)
        date = datetime.date.min

    # Assign appropriate variables to fields in file 
    school_board_from_file = row_data[1]
    confirmed_cases = int(row_data[2])

    # Print data to plotting file if date is within range
    if date >= start_date and date <= end_date:
      if school_board == school_board_from_file:
        q2_plotting_file.write(f"{date},\"{school_board}\",{confirmed_cases}\n")

  # Close the file
  q2_plotting_file.close()

  # START PLOTTING #

  # Open the data file using "pandas" and create csv reader for the plotting file
  try:
    q2_plot = pd.read_csv(argv[2])
  except IOError as err:
    print("Unable to open generated CSV file", argv[2],
      ": {}".format(err), file=sys.stderr)
    sys.exit(-1)

  # Creates figure to draw the plot in
  fig = plt.figure()

  # Creates lineplot using seaborn
  # Refer to column heading names in csv file
  ax = sns.lineplot(x = "Date", y = "Confirmed School Cases", hue = "School Board", data = q2_plot)
  
  # Max number of ticks are 5
  ax.xaxis.set_major_locator(ticktools.MaxNLocator(6))

  # Rotate the ticks on the x-axis to 45 degrees
  plt.xticks(rotation = 45, ha = 'right')

  # Save the matplotlib figure that seaborn has drawn to a file
  fig.savefig(graphics_filename, bbox_inches="tight")

  # Uncomment this line to show the figure on the screen.
  # (May need to use [CTR+C] to close the display after)
  #plt.show()
    
#
# END OF MAIN
#

# Runs main
main(sys.argv)