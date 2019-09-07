# Financial Statement Generation through SimFin API

Before I begin, I find it absolutely necessary to thank [@SimFin](https://github.com/SimFin) for free access to this data via their API. 

## This code is being redesigned, as it was one of the first projects I undertook and improvements in the underlying structure are being prioritized prior to adding new capabilities. The deprecated code scripts however, still do work. They can be found and utilized through the *Deprecated* folder. They will remain there until all of the capabilities of the original program are replicated using the new layout. Necessary README information can be found in that folder. 

## Current Use Cases

The program pulls data from the SimFin API. It can be displayed in an iPython terminal (in pandas format). More functionality is available via the Deprecated folder.

This program only supports annual financials at this time

## Before you start

* Read about the SimFin API here:
https://simfin.com/api/v1/documentation/
* Add your API Key to APIKey.txt
  * If you dont already have one, you can create one for free on the SimFin Website

### Dependencies:

* Pandas
* Requests
* Json
* XlsxWriter

## Usage

Move to the main directory & open an iPython Terminal. From the command line:

```bash
$ cd Financial-Statement-Analysis-Toolkit
$ ipython
```

From the iPython Terminal, Import the necessary module to pull data from the SimFin API:

```python
from src.PullData import *
```

Next, locate the SimId from the ticker you wish to work with:

```python
SimId = IdFromTicker('AAPL')
```

The example above imports from Apple, which trades via the ticker AAPL. Input is required to be in the string format, so quotations must surround the ticker. 

Next, we want to pull all the available statements for the company in question, and then sort through those statements to determine which years have full fiscal year financials available. This is done using the following three functions: 

```python
AllAvailStatements = AvailableStatements(SimId)
AllYears = SortAvailableYears(AllAvailableStatements)
FullFYAvailability = FilterForAnnual(AllAvailStatements, AllYears)
```

Next, pull raw financials using the information we just gathered:

```python
RawFinancials = PullAnnualFinancials(SimId,
                                     FullFYAvailability,
                                     'standardised',
                                     3)
```

The above inputs to the *PullAnnualFinancials* function will return raw output of the SimFin output for the 3 most recent years, in standardised format.

The SimFin API output can be financials that are 'Standardised' or 'As Reported.' So far, this program only supports standardised financials, as with this selection, more data about the flow of the financial statements is provided. This allows for a financial model output (in .xlsx format) that supports formulas. 

Next, we want to clean the data to a more 'friendly' format. in order to do this, we first must import the functions to do so:

```python
from src.CleanData import *
```

Now, we will clean the data and save it to the *Financials* variable:

```python
Financials = IndexRawFSData(RawFinancials)
```

Once you have the *Financials* variable (output to *IndexRawFSData*, you can utilize the display features as well as the export to .xlsx features. 

These will be documented and uploaded to this repository at a later date. 


