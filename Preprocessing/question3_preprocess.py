'''
Authors: Kirisan Suthanthireswaran (1186029), Mehtab Kaur (1054984)
Last Updated: (15-03-2022)

Functionality:
  This file will take 1 data file from the commandline argument and pre-process its data into a simpler file from which data can be read according to desired parameters. The processed data is written to standard output unless redirected into the desired file.

  There is 1 commandline argument: 
    - age_data_file (string)

  From this file, we read these fields:
    - age_group
    - accurate_episode_date

  The output file will have these fields:
    - age_group
    - accurate_episode_date

  The preprocessed data can then be taken and interpreted to be plotted.

To run on commandline:
python Preprocessing/question3_preprocess.py Data/covid_case_file/conposcovidloc.csv

'''
# Packages/Modules #
import sys
import csv
import datetime

# Main Function #
def main(argv):

  # Checks for the right amount of command line arguments. Final argument is optional
  if len(argv) < 2:
    print("Usage: question3_preprocess.py <age_data_file>  <debugOn (optional)>")
    sys.exit(1)

  # Stores optional debugOn argument.
  # This displays debug information in stderr if set to on.   Major errors that cause program exit will still be displayed if it is False.
  try:
    debugOn = bool(int(argv[2]) > 0)
  except:
    debugOn = False
    
  # Stores the commandline arguments 
  age_data_file_name = argv[1]

  # Tries to open the files
  # Will notify the user if an error occurs
  try:
    age_data_file = open(age_data_file_name, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open outbreak_data_file '{}' : {}".format(age_data_file_name, err), file=sys.stderr)
    sys.exit(1)


  # Create csv reader to read the data file
  age_data_reader = csv.reader(age_data_file)

  # Creates variables to keep track of the current line number and rows in timeframe
  current_row_index = 0
  
  #Statement declaring which field is which
  print("Accurate_Episode_Date,Age_Group,Number_of_cases")

  #Creating variables to store data
  last_row_date = "NONE";
  dictionary_of_ages = {}
 
  #Loops through the case data reader, stores the required fields into its respective list 
  for row in age_data_reader:
    
    #Check for if the current row contains the correct amount of fields. Will terminate if the amount is less 
    if len(row) < 18:
      print(f"Row {current_row_index} contains too few fields. The row requires 18 but currently contains: ({len(row)})", file=sys.stderr)
      sys.exit(1)

    #Skips the first line
    if row[0] == "Row_ID":
      current_row_index += 1
      continue

    # Saves current date
    current_row_date = row[1]

    #Assigning last_row_date for the first instance
    if (current_row_index == 1):
      last_row_date = current_row_date
      
    # Checks if it's the same date as now
    if debugOn:
      print(f"Checking row {current_row_index}", file=sys.stderr)
    if current_row_date == last_row_date:

      # If age range has not been seen previously, adds it to the dictionary, otherwise increments the age ranges cases by 1
      if row[5] not in dictionary_of_ages.keys():
        dictionary_of_ages[row[5]] = 1
      else:
        dictionary_of_ages[row[5]] += 1
        
    else:
      if debugOn:
        print("Date is NOT the same!", file=sys.stderr)
        
      for key in dictionary_of_ages.keys():
        print(f"{current_row_date},{key},{dictionary_of_ages[key]}")
        
        if debugOn:
          print(f"Resetting age range {key} for date {current_row_date}")
          
        dictionary_of_ages[key] = 0

    #Increments the row index and saves the current date as last date
    current_row_index += 1;
    last_row_date = current_row_date
     
main(sys.argv)
