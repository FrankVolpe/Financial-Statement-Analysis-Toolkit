# Financial Statement Generation through SimFin API

Before I begin, I find it absolutely necessary to thank [@SimFin](https://github.com/SimFin) for access to this data. Hard work like they're doing will make important datasets more accessable to everyone. 

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
* If you pay for SimFin premium, it is worth your time to browse through some of the functions to remove the "time" functions. These are in place to ensure free users do not run out of API calls.
* The projections folder is not yet in use.
* The data folder is the start of efforts to make this rely less on OOP. If you use anything from it, I will trust that you will change the API key to your own where necessary 


## Usage

This was designed for use within an iPython terminal. Jupyter Notebooks are also fine if that's your cup of tea. Please ensure you are using Python 3 (or higher) when utilizing any scripts from this program.


### Dependencies:

* Pandas
* Requests
* Json


### Pull data & Calculate Ratios

Importing the fs\_calculations.py file will be all inclusive, this would be necessary for any calculations you wish to make with the data being generated

```python
from fs_calculations import *
```

Pull data using the upload function

```python
data = upload('AAPL')
```

To view the data, use the display function

```python
data.display()
```

Create a fs\_calculations object

```python
calculations = fs_calculations(data)
```

To display the calculations, use the display function (same as above)

```python
calculations.display()
```

### Only pull data

If you would just like to pull the data, you can import panel\_data.py instead

```python
from panel_data import *
```

Pull data with the upload function

```python
data = upload('AAPL')
```

To view the data, use the display function

```python
data.display()
```

### Exporting Data

Since the display function is how the DataFrames are developed, you would preface any exports with it. For example, if you were to export to CSV, you would use:

```python
data.display().to_csv('YOUR PATH HERE')
```

More information about the to\_csv function can be found [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html)

## Improvements to be made

* Stronger Excel/Database integration
* Less reliance on OOP
* Support for quarterly financial statements
* Projections of financial statements

