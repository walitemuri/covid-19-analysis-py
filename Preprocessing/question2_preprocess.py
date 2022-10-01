'''
Authors: Mehtab Kaur (1054984)
Last Updated: (15-03-2022)

Functionality:
  This file will take 1 data file from the commandline argument and pre-process its data into a simpler file from which data can be read according to desired parameters. The processed data is written to standard output unless redirected into the desired file.

  There is 1 commandline argument and 1 optional parameter: 
    - school_data_file (string)
    - debugOn (integer)

  From this file, we read these fields (ignoring the rest):
    - collected_date
    - school_board
    - total_confirmed_cases

  The output file will have these fields:
    - collected_date
    - school_board
    - total_confirmed_cases
    
  The preprocessed data can then be taken and interpreted to be plotted.

To run on commandline:
python Preprocessing/question2_preprocess.py Data/schoolrecentcovid2021_2022_2022-02-08_22-17.csv

'''
# Packages/Modules #
import sys
import csv
import datetime

# Main Function #
def main(argv):

  # Checks for the right amount of arguments. 
  if len(argv) < 2:
    print("Usage: question2_preprocess.py <school_data_file> <debugOn (optional)>")
    sys.exit(1)

  # Store commandline arguments in appropriate variables
  school_data_file_name = argv[1]

  # Stores optional debugOn argument.
  # This displays debug information in stderr if set to on. Major errors that cause program exit will still be displayed if it is False.
  try:
    debugOn = bool(int(argv[2]) > 0)
  except:
    debugOn = False

  # Tries opening the file
  # Prints error message if it fails
  try:
      school_data_file = open(school_data_file_name, encoding="utf-8-sig")
  except IOError as err:
    print(f"Unable to open school_data_file '{school_data_file_name}' : {err}", file=sys.stderr)
    sys.exit(1)

  # Create a CSV reader to read the data file 
  school_data_reader = csv.reader(school_data_file)

  # Prints first line of output - header
  print("collected_date,school_board,total_confirmed_cases")

  #Store the current line number
  curr_line_num = 0

  #store current date, school board, and confirmed cases
  #to concatenate confirmed case numbers for same school board on same day
  curr_date = datetime.date.min
  curr_school_board = "NULL"
  curr_case_count= 0
  
  #loop through rows in school data file
  for row_data in school_data_reader:

    # If the row has less than the required amount of fields, prints error and stops
    if len(row_data) < 10:
      print(f"Row {curr_line_num} in school_data_file has too few fields! Needs: 10, Has: {len(row_data)}", file=sys.stderr)
      sys.exit(1)
      
    # Skips the first line
    if row_data[0] == "collected_date":
      # Increments current line number
      curr_line_num += 1
      continue

    #Create variables to store required fields
    # Tries converting data into date format 
    try:
      date = datetime.date.fromisoformat(row_data[0]) 
    except ValueError:
      if debugOn:
        print(f"Could not convert '{row_data[0]}' to a date for collected date (Row {curr_line_num})", file=sys.stderr)
      curr_date = datetime.date.min

    # School board is stored as a string, so no conversion necessary
    school_board = row_data[2]

    # Convert total_confirmed_cases to an integer
    try:
      school_covid_cases = int(row_data[9])
    except ValueError:
      if debugOn:
        print(f"Could not convert '{row_data[9]}' to an integer value for total confirmed cases (Row {curr_line_num}", file=sys.stderr)
      school_covid_cases = 0

    # If the date and school board are the same as the current one stored, add it to confirmed school covid cases
    if date == curr_date and school_board == curr_school_board:
      curr_case_count += school_covid_cases
    else:
      if curr_school_board != "NULL":
        print(f"{curr_date},{curr_school_board},{curr_case_count}")
      curr_date = date;
      curr_school_board = school_board
      curr_case_count = school_covid_cases

      #increments current line num
      curr_line_num += 1

#
# END OF MAIN
#
    
# Run Main
main(sys.argv)

