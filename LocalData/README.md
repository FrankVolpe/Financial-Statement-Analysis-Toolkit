# Storing Datasets Locally

## LocalData/

This folder consists of two scripts, one of which is built solely for command line functionality. The directories include *data/* and *reference/*. As of right now only *reference/* is in use.

## Saving Reference Data Locally

SimFin offers a lot of supplemental data for the companies listed. Beyond this, API calls for financial statements typically depend on information from a few other API calls. For free users with limited API usage each day, or for other datapoints you may want to use to sort through the data available to you (ie. sector information), it may make sense to store some of the 'reference datasets' locally. 

## Pulling Reference Datasets via iPython

First, import the necessary functions via LocalReference

```python
from LocalReference import *
```

This will automatically import your API Key as well from the main directory. Ensure that is populated or else none of the functions shown below will work. 

Each function will automatically return the output (purposely kept as un-modified as possible) and also store that same output as a .json file in *LocalData/reference/*. You can change the path of where the local directories are stored by editing the *path* variable on line 5 of *LocalReference.py*

All of the other functions depend on having a file in the AllEntities format. This utilizes an API call where your output is all of the companies in the SimFin database. It only holds each companies respective name, ticker, and SimId. 

To pull this dataset use:

```python
AllEntities = AllEntitiesJSON() 
```

No parameters are necessary, the ones available are as follows
* FName, (*str*): Output file name, default is *AllEntities.json*
* Sleep, (*bool*): Set to False to avoid resting between API calls, default is True
* APIKey, (*str*): API key, automatically imports with this file

The next dataset that can be added is supplemental information about each company including employee count, sector, and month in which their fiscal year ends

To add this data to AllEntities use:

```python
AllEntities = GeneralDataJSON(AllEntities) 
```

The only necessary parameter is the output of the *AllEntitiesJSON* function, other available parameters are
* FName, (*str*): Output file name, default is *AllEntitiesDetail.json*
* Sleep, (*bool*): Set to False to avoid resting between API calls, default is True
* APIKey, (*str*): API key, automatically imports with this file

It is worth noting that as of this writing there are over 2000 companies on the SimFin database. Because of this, if you are using the free version of the API, this function and the following function will take over 24 hours to fully execute. Because of this it is recomended that you either use a portion of *AllEntities* to run these functions, or register to SimFin+ for unlimited API calls. 


The next dataset you can add to AllEntities is a list of all of the available financial statements on the SimFin platform. Save that by using:

```python
AllEntities = AvailableStatementsJSON(AllEntities) 
```

The only necessary parameter is the output of the *AllEntitiesJSON* function. You do not need to add the supplemental data (*GeneralDataJSON()*) for this to work. Other available parameters are:
* FName, (*str*): Output file name, default is *AvailableStatements.json*
* Sleep, (*bool*): Set to False to avoid resting between API calls, default is True
* APIKey, (*str*): API key, automatically imports with this file


The next dataset you can store is a list of all of the industries and industry codes for the SimFin API Pull that data using:

```python
SectorCodes = SectorCodesJSON(AllEntities) 
```

The only necessary parameter is the output of the *GeneralDataJSON* function, other available parameters are:
* FName, (*str*): Output file name, default is *SectorCodes.json*

Finally, for a list of companies indexed by the sector in which they operate, you can use:

```python
SectorConstituents = SectorConstituentsJSON(AllEntities, SectorCodes) 
```

Necessary parameters are the outputs of the *GeneralDataJSON* and *SectorCodesJSON* functions, respectively. Other available parameters are:
* FName, (*str*): Output file name, default is *AllEntitiesDetail.json*

## Error Monitoring

When looping through individual companies, their can be errors for numerous reasons that arise from reasons out of the users control like data quality or internet connection. For this purpose, the ReportError function keeps track of which companies didn't finish the data generation process. All errors are stored in the variable *ErrorReport* and each instance documents the Operation being performed, Exception type, SimId of company for which it occured, and name of company for which the error occured. Eventually a function that loops through the error report to give the requests another try will be built out. 

