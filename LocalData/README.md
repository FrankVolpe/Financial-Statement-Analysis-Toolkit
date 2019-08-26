## Storing Datasets Locally

### LocalData/

This folder consists of two scripts, one of which is built solely for command line functionality. The directories include *data/* and *reference/*. As of right now only *reference/* is in use.

### Saving Reference Data Locally

SimFin offers a lot of supplemental data for the companies listed. Beyond this, API calls for financial statements typically depend on information from a few other API calls. For free users with limited API usage each day, or for other datapoints you may want to use to sort through the data available to you (ie. sector information), it may make sense to store some of the 'reference datasets' locally. 

### Pulling Reference Datasets via iPython

First, import the necessary functions via LocalReference

```python
from LocalReference import *
```

This will automatically import your API Key as well from the main directory. 

