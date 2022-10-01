'''
Authors:Kirisan Suthanthireswaran (1186029), Roman Blotsky (1168123)
Last Updated: (15-03-2022)

Functionality:
  This file will take 1 data file from the commandline argument and pre-process its data into a simpler file from which data can be read according to desired parameters. The processed data is written to standard output unless redirected into the desired file.

  There is 1 commandline argument: 
    - outbreaks_data_file (string)

  From this file, we read these fields:
    - Date
    - phu_name
    - number_of_outbreaks

  The output file will have these fields:
    - Date
    - phu_name
    - number_of_outbreaks

  The preprocessed data can then be taken and interpreted to be plotted.

To run on commandline:

python Preprocessing/question4_preprocess.py Data/ongoing_outbreaks_phu.csv > question4_preproceseed.csv

'''
# Packages/Modules #
import sys
import csv
import datetime

# Main Function #
def main(argv):
  
  # Checks for the right amount of command line arguments. Final argument is optional
  if len(argv) < 2:
    print("Usage: question4_preprocess.py <outbreak_data_file> <debugOn (optional)>")
    sys.exit(1)
    
  # Stores the commandline arguments 
  outbreak_data_file_name = argv[1]

  # Stores optional debugOn argument.
  # This displays debug information in stderr if set to on. Major errors that cause program exit will still be displayed if it is False.
  try:
    debugOn = bool(int(argv[2]) > 0)
  except:
    debugOn = False

  #Tries to open the files
  #Will notify the user if an error occurs
  try:
    outbreak_data_file = open(outbreak_data_file_name, encoding = "utf-8-sig")
  except IOError as err:
    print("Unable to open outbreak_data_file '{}' : {}".format(outbreak_data_file_name, err), file=sys.stderr)
    sys.exit(1)

  # Create csv reader to read the data file
  outbreak_data_reader = csv.reader(outbreak_data_file)
  
  # To keep track of the current row index
  current_index = 0
  
  # Prints first row of output (column headers)
  print("date,phu_name,number_of_outbreaks")

  # Stores the current date, PHU, and outbreak count 
  # to concatenate different outbreak counts for the same PHU on the same day
  current_date = datetime.date.min
  current_phu_name = "NULL_PHU"
  current_phu_outbreaks = 0
  
  # Loops through the case data reader, stores the required fields into its respective list 
  for row_data_fields in outbreak_data_reader:

    
    # Check for if the current row_data_fields contains at least the correct amount of fields. Will terminate if the amount is less 
    if len(row_data_fields) < 5 :
      print(f"Row {current_index} contains too few fields. The row_data_fields requires 5 but currently contains: ({len(row_data_fields)})", file=sys.stderr)
      sys.exit(1)
    
    # Skips the first line
    if row_data_fields[0] == "date":
      current_index += 1
      continue
      
    # Creating variables to store the 3 fields required
    try:
      date = datetime.date.fromisoformat(row_data_fields[0])
    except ValueError:
      if debugOn == True:
        print(f"Could not convert '{row_data_fields[0]}' to a date value for (Row {current_index})", file=sys.stderr)
        date = datetime.date.min
      
    name = row_data_fields[1]

    try:
      number_of_outbreaks = int(row_data_fields[4])
    except ValueError:
      if debugOn == True:
        print(f"Could not convert '{row_data_fields[4]}' to an integer value for outbreak count (Row {current_index})", file=sys.stderr)
      number_of_outbreaks = 0
      

    # If the date and PHU are the same as the current cached one, adds to its outbreak total
    if date == current_date and name == current_phu_name:
      current_phu_outbreaks += number_of_outbreaks
    else:
      if current_phu_name != "NULL_PHU":
        print(f"{current_date},\"{current_phu_name}\",{current_phu_outbreaks}")
      current_date = date
      current_phu_name = name
      current_phu_outbreaks = number_of_outbreaks


    # Increments current row index
    current_index += 1

#
# END OF MAIN
#

# Runs main function
main(sys.argv)