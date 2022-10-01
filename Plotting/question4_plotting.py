'''
Authors: Kirisan Suthanthireswaran (1186029)
Last Updated: (2022/03-22)

Functionality:
  This file will take a number of command line arguments including a data file, an output file, and a timeframe to plot. It will take the data between the given timeframe from the data file, write it to the output file, and then create a plot from that file using imported libraries. The output is written to standard output unless redirected to a file (recommended to redirect to a PDF)

  There are 8 commandline arguments and 1 optional argument: 
    - outbreak_data_file  (string)
    - plotting_data_file (string)
    - start_year (integer)
    - start_month (integer)
    - start_day (integer)
    - end_year (integer)
    - end_month (integer)
    - end_day (integer)
    - phu_name1
    - phu_name2
    - phu_name3
    - graphing_file (string)

To run on commandline:

python Plotting/question4_plotting.py question4_preprocessed.csv question4_plotted_data.csv 2020 11 01 2023 11 01 "TORONTO" "CITY OF OTTAWA" "NIAGARA REGION" plot4.pdf

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

# this imports tools for "ticks" along the x and y-axes and calls them "ticktools"
from matplotlib import ticker as ticktools

# CONSTANT VALUES #
NUM_X_TICKS = 6



def main(argv):

  #Checking if the correct amount of arguments are run on the command line
  if len(argv) < 13:
    print("Usage: question4_preprocess.py <outbreak_data_file> <plotting_data_file> <start_year> <start_month> <start_day> <end_year> <end_month> <end_day> <name of PHU1> <name of PHU2> <name of PHU3> <debugOn (optional)>")

  #Creating date variables for our time frame
  try:
    start_date = datetime.date(int(argv[3]), int(argv[4]), int(argv[5]))
  except IOError as err:
    print("Error {},Invalid arguments for start date range. Must be in the format <YYYY> <MM> <DD> for {} {} {}".format(err, argv[2], argv[3], argv[4]), file=sys.stderr)
    sys.exit(1)
  
  try:
    end_date = datetime.date(int(argv[6]), int(argv[7]), int(argv[8]))
  except IOError as err:
    print("Error {},Invalid arguments for start date range. Must be in the format <YYYY> <MM> <DD> for {} {} {}".format(err, argv[6], argv[7], argv[8]), file=sys.stderr)
    sys.exit(1)

  #Stores command-line arguments 
  outbreak_data_file_name = argv[1]
  plotting_data_file_name = argv[2]
  phu_name1 = argv[9]
  phu_name2 = argv[10]
  phu_name3 = argv[11]
  graphing_file = "plot4.svg"

  #Tries to open the files
  #Will notify the user if an error occurs
  try:
    outbreak_data_file = open(outbreak_data_file_name, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open outbreak_data_file '{}' : {}".format(outbreak_data_file_name, err), file=sys.stderr)
    sys.exit(1)
  try:
    plotting_data_file = open(plotting_data_file_name,"w", encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open plotting_data_file '{}' : {}".format(plotting_data_file_name, err), file=sys.stderr)
    sys.exit(1)

  #Createing csv reader to read the data file(s)
  outbreak_date_reader = csv.reader(outbreak_data_file)
  

  #Creating the header for the plotting_date file
  plotting_data_file.write("Date,Number_Of_Outbreaks,PHU_NAME\n")

  
  #To keep track of current row index
  current_index = 0


  #To ensure that we are within the given date range
  is_in_range = False

  #Looping through the givend data_file to extract data 
  for row_data_fields in outbreak_date_reader:
    
    if row_data_fields[0] == "date":
      continue
  # Check for if the current row_data_fields contains at least the correct amount of fields. Will terminate if the amount is less 
    if len(row_data_fields) < 3:
      print(f"Row {current_index} contains too few fields. The row_data_fields requires 3 but currently contains: ({len(row_data_fields)})", file=sys.stderr)
      sys.exit(1)


    #Taking the fields from the file and assigning them to variables
    date = row_data_fields[0]
    phu_name_from_file = row_data_fields[1]
    amount_of_outbreaks = int(row_data_fields[2])
    
    #Checking if the current date matches our range
    if (row_data_fields[0] == str(start_date)):
      is_in_range = True
      
    elif(row_data_fields[0] == str(end_date)):
      is_in_range = False

    #If we are within the given range, we continue with the code
    if (is_in_range == True):
      #Checking First PHU
      if(phu_name1 == phu_name_from_file):
        plotting_data_file.write(f"{date},{amount_of_outbreaks},\"{phu_name_from_file}\"\n")
      #Checking Second PHU
      elif(phu_name2 == phu_name_from_file):
        plotting_data_file.write(f"{date},{amount_of_outbreaks},\"{phu_name_from_file}\"\n")
      #Checking Third PHU
      elif(phu_name3 == phu_name_from_file):
        plotting_data_file.write(f"{date},{amount_of_outbreaks},\"{phu_name_from_file}\"\n")

  #PLOTTING 

  
  #Closing the file that has been written to
  plotting_data_file.close()

  #Reopening the file for reading in order to create our graph
  try:
    question4_plotting = pd.read_csv(argv[2])
  except IOError as err:
    print("Unable to open the newly created file '{}' : {}".format(argv[2], err), file=sys.stderr)
    sys.exit(-1)
  
  # Generate a figure for the seaborn library to draw in.
  fig = plt.figure()

  # Creates a lineplot using seaborn 
  # (Each name here must have the same name as its column in the CSV file)
  ax = sns.lineplot(x = "Date", y = "Number_Of_Outbreaks", hue="PHU_NAME", data=question4_plotting)

  # Set the max number of axis labels to NUM_X_TICKS, to avoid having ticks for each date
  ax.xaxis.set_major_locator(ticktools.MaxNLocator(NUM_X_TICKS))

  # Rotate the ticks on the x-axis to 45 degrees
  plt.xticks(rotation = 45, ha = 'right')

  # Saves the fig to a file
  fig.savefig(graphing_file, bbox_inches="tight")

    # Uncomment this line to show the figure on the screen.
  # (May need to use [CTR+C] to close the display after)
  #plt.show()
  
  #
  # END OF MAIN
  #


    
main(sys.argv)