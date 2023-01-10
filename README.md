# Project Title

COVID-19 Regional Analysis

## Description

Using a collection of Data sets (listed below) relating to COVID-19 me and my peers used 4 distinct approaches to analyze the information in order to extract relevant corelations. Each generated plot seeks to aid in answering 4 relevant questions that relate to the handling and policy decisions for the COVID-19 pandemic. 

The date range (x - axis) is taken in as a command-line argument, the user is free to decide the desired timeframe to analyze. More information is available in the Running section.

### Question 1) What percentage of each vaccination group in the Ontario population got admitted to ICU?

The first plot is focused on examining the relationship between Vaccination and COVID-19 patients being admitted into the ICU.

Vaccination Groups: 
* Partially Vaccinated
* Fully Vaccinated (2 shots at this time)
* No Vaccination

Data Sets: 

https://data.ontario.ca/en/dataset/covid-19-vaccine-data-in-ontario
https://data.ontario.ca/en/dataset/covid-19-vaccine-data-in-ontario/resource/eed63cf2-83dd-4598-b337-b288c0a89a16
https://data.ontario.ca/en/dataset/covid-19-vaccine-data-in-ontario/resource/274b819c-5d69-4539-a4db-f2950794138c
 

Example Plot:

![plot1](https://user-images.githubusercontent.com/108627530/211439214-a534f0bc-b75d-44b5-bece-abe83a529cbe.svg)



### Question 2) How many students from a specified school board in Ontario got COVID-19?

Plot 2 is focused on analyzing which regions in Ontario were able to contain the virus and which regions were not as successful. 

Data Sets: https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/ 

Example Plot:

![plot2](https://user-images.githubusercontent.com/108627530/211439339-209d9819-2a2d-4321-af8a-9d7eb4685065.svg)

### Question 3) How does the quantity of positive COVID-19 cases differ between each age group over time?

Plot 3 illustrates the relationship between COVID-19 cases across different age groups and how it changes over time with the introduction of complex
variants. 

Data Sets: 

https://data.ontario.ca/dataset
https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350

Age Groups:
* 90+
* 80-89
* 70-79
* 60-69
* 50-59
* 40-49
* 30-39
* 20-29
* <20

Example Plot:

![plot3](https://user-images.githubusercontent.com/108627530/211439379-76fa8ff6-db1b-48b1-81d8-a71e4c8f926d.svg)

### Question 4) What is the quantity of outbreaks by Public Health Unit in Ontario over time?

Finally, the final question plots the quantity of outbreaks by PHU, multiple are plotted at the same time in order to allow comparison.

Data Sets: 

https://data.ontario.ca/dataset/ontario-covid-19-outbreaks-data
https://data.ontario.ca/dataset/ontario-covid-19-outbreaks-data/resource/36048cc1-3c47-48ff-a49f-8c7840e32cc2

Example plot:

![plot4](https://user-images.githubusercontent.com/108627530/211439090-6fd845c0-13ec-46f4-a62d-d1035ad34da2.svg)

## Dependencies

* Python 3.10+

```
contourpy==1.0.6
cycler==0.11.0
fonttools==4.38.0
kiwisolver==1.4.4
matplotlib==3.6.2
numpy==1.24.1
packaging==23.0
pandas==1.5.2
Pillow==9.4.0
pyparsing==3.0.9
python-dateutil==2.8.2
pytz==2022.7
seaborn==0.12.2
six==1.16.0
```

## Preprocessing

In order to plot the relevant data in an efficient manner, the data sets are preprocessed into csv files containing the only the fields relevant to each plot. Each plotting script has a corresponding preprocessing script that will need to be run beforehands, the steps to accomplish this are as follows:

### Question 1 Preprocessing:

Enter root folder and run:

```
python Preprocessing/question1_preprocess.py Data/vaccine_doses_given.csv Data/icu_data_by_vac_status.csv > question1_preprocessed.csv
```

### Question 2:

```
python Preprocessing/question2_preprocess.py Data/schoolrecentcovid2021_2022_2022-02-08_22-17.csv > question2_preprocessed.csv
```

### Question 3:

```
python Preprocessing/question3_preprocess.py Data/covid_case_file/conposcovidloc.csv > question3_preprocessed.csv
```

### Question 4:

```
python Preprocessing/question4_preprocess.py Data/ongoing_outbreaks_phu.csv > question4_preproceseed.csv
```

Upon running all 4 scripts the following files should be output:

* question1_preprocessed.csv
* question2_preprocessed.csv
* question3_preprocessed.csv
* question4_preprocessed.csv

## Plotting The Graphs

In order to plot the graph the plotting scripts must be run, the user can specify certain commandline arguments for each to control output.

### Question 1 Plotting:

There are 8 commandline arguments and 1 optional argument: 
   
* q1_plotting_file (string)
* start_year (integer)
* start_month (integer)
* start_day (integer)
* end_year (integer)
* end_month (integer)
* end_day (integer)
* graphics_file (string)
* debugOn (integer, optional)
    
Output: The default output is .svg file, you can specify the file format in the commandline args.
    
Enter Root Directory and run:

```
python {q1_plotting_script} {q1_processed_file} {q1_plotting_file} {start_year} {start_month} {start_day} {end_year} {end_month} {end_day} {graphics_file}
```

Example Run:

```
python Plotting/question1_plotting.py question1_preprocessed.csv question1_plotted_data.csv 2020 8 10 2022 3 10 plot1.pdf
```

### Question 2 Plotting:

There are 10 commandline arguments and 1 optional argument: 

* q2_processed_file (string)
* q2_plotting_file (string)
* start_year (integer)
* start_month (integer)
* start_day (integer)
* end_year (integer)
* end_month (integer)
* end_day (integer)
* school_board (string)
* graphics_filename (string)
* debugOn (integer, optional)

Run on commandline:

```
python {q2_plotting_script} {q2_processed_file} {q2_plotting_file} {start_year} {start_month} {start_day} {end_year} {end_month} {end_day} {school_board} {graphics_file}
```

Example run:

```
python Plotting/question2_plotting.py question2_preprocessed.csv question2_plotted_data.csv 2020 8 10 2022 3 10 'Peel District School Board' plot2.pdf
```

### Question 3 Plotting:

There are 9 commandline arguments and 1 optional argument: 

* q3_processed_file (string)
* q3_plotting_file (string)
* start_year (integer)
* start_month (integer)
* start_day (integer)
* end_year (integer)
* end_month (integer)
* end_day (integer)
* graphic file (string)
* debugOn (integer, optional)


To run on commandline:
python Plotting/question3_plotting.py question3_preprocessed.csv question3_plotted_data.csv 2021 8 10 2022 1 29 plot3.pdf

Run on cmnd line:

```
python {q3_plotting_script} {q3_processed_file} {q3_plotting_file} {start_year} {start_month} {start_day} {end_year} {end_month} {end_day} {graphics_file}

```



Example Run:

```
python Plotting/question3_plotting.py question3_preprocessed.csv question3_plotted_data.csv 2021 8 10 2022 1 29 plot3.pdf
```

### Question 4 Plotting:

There are 8 commandline arguments and 1 optional argument: 

* outbreak_data_file  (string)
* plotting_data_file (string)
* start_year (integer)
* start_month (integer)
* start_day (integer)
* end_year (integer)
* end_month (integer)
* end_day (integer)
* phu_name1
* phu_name2
* phu_name3
* graphing_file (string)
    
To run on commandline:

```
python {q4_plotting_script} {q4_processed_file} {q4_plotting_file} {start_year} {start_month} {start_day} {end_year} {end_month} {end_day} {phu_name1} {phu_name2} {phu_name3} {graphics_file}

```

```
python Plotting/question4_plotting.py question4_preprocessed.csv question4_plotted_data.csv 2020 11 01 2023 11 01 "TORONTO" "CITY OF OTTAWA" "NIAGARA REGION" plot4.pdf
```

## Author Information

* Roman Blotsky
1168123

* Mehtab Kaur
1054984

* Kirisan Suthanthireswaran
1186029

* Wali Temuri	
1183379


## Data Set

* [Confirmed Cases of COVID-19](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario) : this is the data set we examined last week

* [Government of Ontario Datasets](https://data.ontario.ca/dataset)
    * This is the Open Government data portal.  There are many datasets available for analysis, on COVID-19 and on other topics.
    * Data here is [licensed under the Open Government License - Ontario](https://www.ontario.ca/page/open-government-licence-ontario) and is available for many uses -- please see the license for details.  The [Open Government initiative was set up in 2016](https://www.ipc.on.ca/wp-content/uploads/2016/09/open-government-key-concepts-and-benefits.pdf).

* [Government of Ontario Datasets tagged with "COVID-19"](https://data.ontario.ca/dataset?keywords_en=COVID-19)
    * These are the subset of the above data tagged with this keyword

* [Statistics Canada Health Profile Data](https://www12.statcan.gc.ca/health-sante/82-228/search-recherche/lst/page.cfm?Lang=E&GeoLevel=PR&GEOCODE=35)
    * This data provides demographic and other information about specific Public Health Units within the province

