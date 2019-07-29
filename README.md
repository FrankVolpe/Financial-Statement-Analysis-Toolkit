# Financial Statement Generation through SimFin API

## Current Use Cases

The program uses OOP to download financial statement data. Basic calculations can also be made using the program, most of which being ratios/margins. 

This program only supports annual financials at this time

At risk of stating the obvious, this is very much still a work in progress. It was started as a first project for me, and was placed on the back burner for quite some time. If you wish to contribute, and would like any clarification not listed here, feel free to send me an email at frank.volpe.ny@gmail.com to discuss. 

## Before you start

* Read about the SimFin API here:
https://simfin.com/api/v1/documentation/
* Go to simfin\_basics.py and add your API key to the global\_api\_key variable (Line 4) 
* If you dont already have one, you can create one for free on the SimFin Website
* Please note that while database\_access.py has been created, it is not yet functional. Database compatibility is one of the priorities listed below.


## Usage

This was designed for use within an iPython terminal. Jupyter Notebooks are also fine if that's your cup of tea. Please ensure you are using Python 3 (or higher) when utilizing any scripts from this program.

### Dependencies:

* Pandas
* Requests
* Json

### Pull data & Calculate Ratios

Importing the fs\_calculations.py file will be all inclusive, this would be necessary for any calculations you wish to make with the data being generated

'''from fs_calculations import *'''

Pull data using the upload function

'''data = upload('AAPL')'''

To view the data, use the display function

'''data.display()'''

Create a fs\_calculations object

'''calculations = fs_calculations(data)'''

To display the calculations, use the display function (same as above)

'''calculations.display()'''

### Only pull data

If you would just like to pull the data, you can import panel\_data.py instead

'''from panel_data import *'''

Pull data with the upload function

'''data = upload('AAPL')'''

To view the data, use the display function

'''data.display()'''


## Improvements to be made

* Stronger Excel/Database integration
* Less reliance on OOP
* Support for quarterly financial statements
* Projections of financial statements

