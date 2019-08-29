###################################################
## Changes format of SimFin output. ###############
## First indexes by Statement, then by line item ##
###################################################
## Input is the output of PullAnnualFinancials() 
##
def IndexRawFSData(RawFSData):
    # Output Variable
    ThreeStatements = {'Income Statement'       : [],
                       'Cash Flow Statement'    : [],
                       'Balance Sheet'          : []}
    # Input data in new format
    for Year in RawFSData.keys():
        IndexStatement(ThreeStatements['Income Statement'],
                       RawFSData[Year][0])
        IndexStatement(ThreeStatements['Cash Flow Statement'],
                       RawFSData[Year][1])
        IndexStatement(ThreeStatements['Balance Sheet'],
                       RawFSData[Year][2])
    # Populate Children
    AddChildren(ThreeStatements)
    return ThreeStatements


#################################################
## Takes each individual statement in, Formats ##
#################################################
## Input is one statement from one year
## Compatible with all 3 financial statements
##
def IndexStatement(OutputList, Statement):
    Date = Statement['periodEndDate']
    for x in range(len(Statement['values'])):
        LineItem = Statement['values'][x]
        Name     = LineItem['standardisedName']
        Value    = LineItem['valueChosen']
        SuppVal  = { 'Calculated' :  LineItem['valueCalculated'],
                     'Assigned'   :  LineItem['valueAssigned'] }
        try:
            # Add to Output if line items are the same
            if OutputList[x]['TID'] == LineItem['tid']:
                OutputList[x]['Values'][Date] = Value
                OutputList[x]['SuppVal'][Date] = SuppVal
            else:
                Error = (Name, Date)
                print('Error appending %s from %s statement' % Error)
        # If LineItem hasnt been added to Output yet, do so. 
        except IndexError:
            OutputList.append({'Name'      : Name,
                               'Calc   '   : LineItem['checkPossible'],
                               'Parent'    : LineItem['parent_tid'],
                               'TID'       : LineItem['tid'],
                               'Children'  : [],
                               'Values'    : { Date : Value },
                               'SuppVal'   : SuppVal })

# The only two items in a line item not being added, saved 
# here so they can be later on if necessary
#
#'Attributes' : { 'UID'   : LineItem['uid'],
#                 'DL'    : LineItem['displayLevel']}})

##########################################
## Adds children to each line item #######
##########################################
## Used for line items that are calculated
##
def AddChildren(ThreeStatements):
    # Loop through each statement
    for Statement in ThreeStatements.keys():
        # Loop through each line item
        for LineItem in ThreeStatements[Statement]:
            # Save LineItem's parent TID to variable
            ParentTID = LineItem['Parent']
            # Loop through LineItems again to find parent
            for Parents in ThreeStatements[Statement]:
                if ParentTID == Parents['TID']:
                    Parents['Children'].append(LineItem['TID'])

