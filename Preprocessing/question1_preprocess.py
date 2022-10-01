'''
Authors: Roman Blotsky (1168123), Mehtab Kaur (1054984), Kirisan Suthanthireswaran (1186029)
Last Updated: (15-03-2022)

Functionality:
  This file will take 2 data files from the commandline arguments and pre-process their data into a single, simpler file from which data can be read according to desired parameters. The processed data is written to standard output unless redirected into the desired file.

  There are 3 commandline arguments: 
    - vaccine_data_file (string)
    - icu_data_file (string)
    - debugOn (integer)

  From these 2 files, we read these fields:
    - icu_unvac (icu_data_file)
    - icu_partial_vac (icu_data_file)
    - icu_full_vac (icu_data_file)
    - Date (icu_data_file)
    - total_individuals_partially_vaccinated (vaccine_data_file)
    - total_individuals_fully_vaccinated (vaccine_data_file)
    - report_date (vaccine_data_file)

  The output file will have these fields:
    - date
    - icu_percent_unvac
    - icu_percent_partial_vac
    - icu_percent_full_vac

  The preprocessed data can then be taken and interpreted to be plotted.

To run on commandline:
python Preprocessing/question1_preprocess.py Data/vaccine_doses_given.csv Data/icu_data_by_vac_status.csv > question1_preprocessed.csv
'''

# Packages/Modules #
import sys
import csv
import datetime


# Constants #
OUTPUT_DECIMAL_PLACES = 4
ONTARIO_POPULATION = 14915270 # Retrieved from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901

# Main Function #
def main(argv):

  # Checks for the right amount of arguments. Final argument is optional.
  if len(argv) < 3:
    print("Usage: question1_preprocess.py <vaccine_data_file> <icu_data_file> <debugOn (optional)>")
    sys.exit(1)  

  # Stores commandline arguments
  vaccine_data_file_name = argv[1]
  icu_data_file_name = argv[2]

  # Stores optional debugOn argument.
  # This displays debug information in stderr if set to on. Major errors that cause program exit will still be displayed if it is False.
  try:
    debugOn = bool(int(argv[3]) > 0)
  except:
    debugOn = False

  # Tries opening the files
  # Prints error messages if it fails
  try:
      vaccine_data_file = open(vaccine_data_file_name, encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open vaccine_data_file '{}' : {}".format(
            vaccine_data_file_name, err), file=sys.stderr)
    sys.exit(1)

  try:
    icu_data_file = open(icu_data_file_name, encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open icu_data_file '{}' : {}".format(
          icu_data_file_name, err), file=sys.stderr)
    sys.exit(1)
  
  
  # Create csv readers to read both data files
  vaccine_data_reader = csv.reader(vaccine_data_file)
  icu_data_reader = csv.reader(icu_data_file)

  # Store the data that is found in the array (Stored as a list - we assume both files have the same number of lines, extra lines in either are discarded)
  unvac_total_daily = []
  partial_vac_total_daily = []
  full_vac_total_daily = []
  row_date = []

  # Store the current row number
  curr_row_index = 0   
  
  # loop through case data reader, store cases per day per vac group
  for row_data in vaccine_data_reader:

    # If the row has less than required amount of fields, prints error and stops.
    if len(row_data) < 11:
      print(f"Row {curr_row_index} in icu_data_file has too few fields! Needs: 11, Has: ({len(row_data)})", file=sys.stderr)
      sys.exit(1)

    # Increments current row index
    curr_row_index += 1
    
    # Skips first line
    if row_data[0] == 'report_date':
      continue
    
    # Tries reading the file and storing data as integers.
    # If any error reading data (eg. empty data), sets to 0 to ensure
    # each array position is for the right day.
    try:
      curr_date = datetime.datetime.fromisoformat(row_data[0])  
    except ValueError:
      if debugOn:
        print(f"Could not convert '{row_data[0]}' to a date for report date (Row {curr_row_index})", file=sys.stderr)
      curr_date = datetime.datetime.min
      
    try:  
      partial_vac_amount = int(row_data[7])
    except ValueError:
      if debugOn:
        print(f"Could not convert '{row_data[7]}' to an integer value for partial vac (Row {curr_row_index})", file=sys.stderr)
      partial_vac_amount = 0
      
    try:  
      full_vac_amount = int(row_data[9])
    except ValueError:
      if debugOn:
        print(f"Could not convert '{row_data[9]}' to an integer value for full vac (Row {curr_row_index})", file=sys.stderr)
      full_vac_amount = 0

    # Appending each data field from the file to its respective empty list
    row_date.append(curr_date)
    unvac_total_daily.append(ONTARIO_POPULATION-partial_vac_amount-full_vac_amount)
    partial_vac_total_daily.append(partial_vac_amount)
    full_vac_total_daily.append(full_vac_amount)    

  # Prints first line of output
  print("date,icu_percent_unvac,icu_percent_partial_vac,icu_percent_full_vac")
  
  # Loop through icu file, print percentage per day per vac group using stored data
  curr_stored_data_index = 0
  curr_row_index = 0
  
  for row_data in icu_data_reader:

    # If the row has less than required amount of fields, prints error and stops.
    if len(row_data) < 8:
      print(f"Row {curr_row_index} in icu_data_file has too few fields! Needs: 8, Has: ({len(row_data)})",file=sys.stderr)
      sys.exit(1)
    
    # Increments current row index (this is done immediately as it tracks the current file)
    curr_row_index += 1
    
    # Skips first row
    if row_data[0] == '_id':
      continue
    
    # Tries storing all the data from this row in proper formats.
    # Prints errors if any arise.
    # Sets values to 0 if they aren't read properly.
    try:
      curr_date = datetime.datetime.fromisoformat(row_data[1])
    except ValueError:
      if debugOn:
        print(f"Could not convert {row_data[1]} to a date for report date (Row {curr_stored_data_index})", file=sys.stderr)
      curr_date = datetime.datetime.min    
    
    try:
      unvac_icu = int(row_data[2])
    except ValueError:
      if debugOn:
        print(f"Could not convert {row_data[2]} to integer (Row {curr_stored_data_index})")
      unvac_icu = 0
    
    try:
      partial_vac_icu = int(row_data[3])
    except ValueError:
      if debugOn:
        print(f"Could not convert {row_data[3]} to integer (Row {curr_stored_data_index})")
      partial_vac_icu = 0
    
    try:
      full_vac_icu = int(row_data[4])
    except ValueError:
      if debugOn:
        print(f"Could not convert {row_data[4]} to integer (Row {curr_stored_data_index})")
      full_vac_icu = 0

      
    # Potential problem: Vaccine data file starts earlier than ICU data file
    # Solution: If the date stored at the current row index is earlier than this date, we loop through stored data list until it reaches the current date.
    while row_date[curr_stored_data_index] - curr_date < datetime.timedelta(0):
      if debugOn:
        print(f"Skipping item {curr_stored_data_index} in stored data as it is dated too early ({row_date[curr_stored_data_index]} earlier than {curr_date}).", file=sys.stderr);
      curr_stored_data_index += 1

    # Potential problem: Vaccine data file starts later than ICU data file
    # Solution: If the date stored at the current row index is later than this date, we do not increment curr_stored_data_index 
    if row_date[curr_stored_data_index] - curr_date > datetime.timedelta(0):
      if debugOn:
        print(f"Skipping row {curr_row_index} in icu_data_file as it is earlier than stored vaccine data ({row_date[curr_stored_data_index]} later than {curr_date})", file=sys.stderr)
      continue

    # Increments current item being read from the stored vaccine data (this is done only once we start reading data from the vaccine data file)
    curr_stored_data_index += 1

    # Calculates percentages, sets to 0 if no people are in the category
    if unvac_total_daily[curr_stored_data_index] != 0:
      unvac_percentage = unvac_icu/unvac_total_daily[curr_stored_data_index]
    else:
      unvac_percentage = 0
    
    if partial_vac_total_daily[curr_stored_data_index] != 0:
      partial_vac_percentage = partial_vac_icu/partial_vac_total_daily[curr_stored_data_index]
    else:
      partial_vac_percentage = 0

    if full_vac_total_daily[curr_stored_data_index] != 0:
      full_vac_percentage = full_vac_icu/full_vac_total_daily[curr_stored_data_index]
    else:
      full_vac_percentage = 0

    # Converts decimal values to percentages, then rounds
    unvac_percentage = round(unvac_percentage*100, OUTPUT_DECIMAL_PLACES)
    partial_vac_percentage = round(partial_vac_percentage*100, OUTPUT_DECIMAL_PLACES)
    full_vac_percentage = round(full_vac_percentage*100, OUTPUT_DECIMAL_PLACES)

    # Prints processed data
    print(f"{curr_date.date()},{unvac_percentage},{partial_vac_percentage},{full_vac_percentage}")

#
# END OF MAIN
#
    
# Run Main
main(sys.argv)