import pandas as pd

#####################################################################
## Saves one financial statement as a pd.DataFrame ##################
#####################################################################
## Divisor: int, Show statement in thousands by setting to 1000, etc.
##          Set to None to show data as it came from API
##
## **** Mention .dropna() in README ****
##
def StatementToPandas(Input, Divisor=None):
    Statement = pd.DataFrame()
    # Loop through each Line Item
    for LineItem in Input:
        Data = {}
        # Loop through each year
        for Key in LineItem['Values'].keys():
            # Set Value as int or None
            try:
                Data[Key] = int(LineItem['Values'][Key])
            except TypeError:
                Data[Key] = None
        # Save LineItem as DataFrame
        DFLine = pd.DataFrame(data=Data, index=[LineItem['Name']])
        # Append LineItem to Statement
        Statement = Statement.append(DFLine)
    if Divisor == None:
        return Statement
    else:
        return Statement / Divisor

##########################################################
## Saves three statements as dict with pd.DataFrames #####
##########################################################
## Takes divisor from above function
##
def ThreeStatementsToPandas(PanelData, Divisor=None):
    Output = {}
    for Key in PanelData:
        Output[Key] = StatementToPandas(PanelData[Key], Divisor)
    return Output


##########################################################
## Saves one financial statement as a pd.DataFrame #######
##########################################################
## Divisor: Show statement in thousands by setting to 1000
##
## **** Mention .dropna() in README ****
##
def DisplayThreeStatements(PanelData, DisplayAs=None, HideEmpty=False):
    if DisplayAs == 'K':
        Divisor = 1000
        DAMessage = 'All Figures Shown in Thousands'
    elif DisplayAs == 'M':
        Divisor = 1000000
        DAMessage = 'All Figures Shown in Millions'
    else:
        Divisor = False
        DAMessage = ''
    Output = ThreeStatementsToPandas(PanelData, Divisor)
    for Key in Output:
        print(Key)
        print(DAMessage)
        print('\n')
        if HideEmpty == False:
            print(Output[Key])
        else:
            print(Output[Key].dropna())
        print('\n\n')
