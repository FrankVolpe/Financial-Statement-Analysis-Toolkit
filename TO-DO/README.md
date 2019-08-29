## /SIMFIN/LocalData/
* Command line functionality
* New functions to support Local Imports from PullData.py

## /SIMFIN/src/PullData.py
* Pull Quarterly standardised
* Pull Annual as reported
* Pull Quarterly as reported

## /SIMFIN/src/CleanData.py
* Function to change Line item manually
* Change LineItem['Values'] to only include 'Chosen'

## /SIMFIN/CalcRatios/
* NOT DONE IN PANDAS. LIMIT DEPENDENCIES
* Create Data Structure for a ratio that can be easily integrated into an excel formula

## /SIMFIN/
* Export functionality
* Storing in both .json and viewing in Pandas
* Display functionality
* Function to add new line item, mid statement (%change, margin)

## /SIMFIN/BuildModel/
* Use XlsxWriter to format blank workbook
* Set formulas and which cells go in them
* Option to set the template type to ensure model works across different templated
* Dictionary with assumptions to base projections from
  * Should be able to populate this from the command line

* Regarding building model from as reported statements
  * Function called 'Locate' that allows the user to identify key line items from those provided, use those in calculating ratios/making projections

