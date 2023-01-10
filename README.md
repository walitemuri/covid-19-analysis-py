# Project Title

COVID-19 Regional Analysis

## Description

Using a collection of Data sets (listed below) relating to COVID-19 me and my peers used 4 distinct approaches to analyze the information in order to extract relevant corelations. Each generated plot seeks to aid in answering 4 distinct questions that relate to the handling and policy decisions for the COVID-19 pandemic. 

### Question 1) What percentage of each vaccination group in the Ontario population got admitted to ICU?

The first plot is focused on examining the relationship between Vaccination and COVID-19 patients being admitted into the ICU.

Vaccination Groups: 
* Partially Vaccinated
* Fully Vaccinated (2 shots at this time)
* No Vaccination

Example Plot:

![plot1](https://user-images.githubusercontent.com/108627530/211439214-a534f0bc-b75d-44b5-bece-abe83a529cbe.svg)



### Question 2) How many students from a specified school board in Ontario got COVID-19?

Plot 2 is focused on analyzing which regions in Ontario were able to contain the virus and which regions were not as successful. 

Example Plot:

![plot2](https://user-images.githubusercontent.com/108627530/211439339-209d9819-2a2d-4321-af8a-9d7eb4685065.svg)

### Question 3) How does the quantity of positive COVID-19 cases differ between each age group over time?

Plot 3 illustrates the relationship between COVID-19 cases across different age groups and how it changes over time with the introduction of complex
variants. 

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

Example plot:

![plot4](https://user-images.githubusercontent.com/108627530/211439090-6fd845c0-13ec-46f4-a62d-d1035ad34da2.svg)

##Dependencies

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

##Running

## Data Set

* [Confirmed Cases of COVID-19](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario) : this is the data set we examined last week

* [Government of Ontario Datasets](https://data.ontario.ca/dataset)
    * This is the Open Government data portal.  There are many datasets available for analysis, on COVID-19 and on other topics.
    * Data here is [licensed under the Open Government License - Ontario](https://www.ontario.ca/page/open-government-licence-ontario) and is available for many uses -- please see the license for details.  The [Open Government initiative was set up in 2016](https://www.ipc.on.ca/wp-content/uploads/2016/09/open-government-key-concepts-and-benefits.pdf).

* [Government of Ontario Datasets tagged with "COVID-19"](https://data.ontario.ca/dataset?keywords_en=COVID-19)
    * These are the subset of the above data tagged with this keyword

* [Statistics Canada Health Profile Data](https://www12.statcan.gc.ca/health-sante/82-228/search-recherche/lst/page.cfm?Lang=E&GeoLevel=PR&GEOCODE=35)
    * This data provides demographic and other information about specific Public Health Units within the province

