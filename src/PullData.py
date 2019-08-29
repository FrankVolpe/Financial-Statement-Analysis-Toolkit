import requests
import json
import time

#######################################
## Pull API Key and save as variable ##
#######################################
##
with open('APIKey.txt', 'r') as file:
    APIKey = file.read().replace('\n', '')
    file.close()

######################################
## Set path for saving data locally ##
######################################
##
path = 'LocalData/data/'

###################################################################
## For use in below functions to export raw data in .json format ##
###################################################################
##
def SaveToJSON(Data, FName, TimeStamp, path=path):
    if TimeStamp == True:
        ts = time.strftime('-%Y-%m-%d')
        File = '%s%s%s.json' % (path, FName, ts)
    else:
        File = '%s%s.json' % (path, FName)
    with open(File, 'w') as Output:
        json.dump(Data, Output)
        Output.close()

###############################################################
## Return SimId from Ticker ###################################
###############################################################
## TryLocal will attempt to use local data first if set to True 
##
def IdFromTicker(Ticker, TryLocal=False):
    # Attempt to pull data locally
    if TryLocal == True:
        try:
            with open('LocalData/reference/SimIds.json', 'r') as File:
                txt = File.read()
                SimIds = json.loads(txt)
                File.close()
            return str(SimIds[Ticker.upper()])
        except:
            pass
    # Pull via API
    Link = 'https://simfin.com/api/v1/info/find-id/ticker/%s'
    Params = {'api-key' : APIKey}
    Output = requests.get(Link % Ticker.upper(), params=Params).json()
    try:
        return str(Output[0]['simId'])
    except ValueError:
        print('Failed to locate SimId')

###############################################################
## Return Statement Availability from SimId ###################
###############################################################
## TryLocal will attempt to use local data first if set to True
## SaveLocal will save the raw data if set to True 
##
def AvailableStatements(SimId, TryLocal=False, SaveLocal=True):
    # Attempt to pull data locally
    if TryLocal == True:
        try:
            with open('LocalData/reference/Statements.json', 'r') as File:
                txt = File.read()
                SimIds = json.loads(txt)
                File.close()
            return CleanStatementAvailability(Statements[SimId])
        except:
            pass
    # Pull via API
    Link = 'https://simfin.com/api/v1/companies/id/%s/statements/list'
    Params = {'api-key' : APIKey}
    Output = requests.get(Link % SimId, params=Params).json()
    # Save raw data if called to do so
    if SaveLocal == True:
        SaveToJSON(Output, '%s-Raw-Availability' % SimId, False)
    return CleanStatementAvailability(Output, SimId)

################################################
## Cleans Output of Statement Availability #####
################################################
## SaveLocal will save the output if set to True 
##{ 2019 : [ 'TTM', 
##           'TTM-0.25', 
##           'TTM-0.5'],
##  2018 : [ 'TTM-1', 
##           'Q4']}
##
def CleanStatementAvailability(StatementTestOutput, SimId, SaveOutput=True):
    # Ensure Available Statements Exist
    try:
        ISRaw = StatementTestOutput['pl']
        CFRaw = StatementTestOutput['cf']
        BSRaw = StatementTestOutput['bs']
    except:
        print('Necessary statements were not all available')
    IS = {}
    CF = {}
    BS = {}
    # Process Income Statement
    for Statement in ISRaw:
        try:
            IS[Statement['fyear']].append(Statement['period'])
        except KeyError:
            IS[Statement['fyear']] = [Statement['period']]
    # Process Cash Flow Statement
    for Statement in CFRaw:
        try:
            CF[Statement['fyear']].append(Statement['period'])
        except KeyError:
            CF[Statement['fyear']] = [Statement['period']]
    # Process Balance Sheet
    for Statement in BSRaw:
        try:
            BS[Statement['fyear']].append(Statement['period'])
        except KeyError:
            BS[Statement['fyear']] = [Statement['period']]
    if SaveOutput == True:
        SaveToJSON([IS,CF,BS], '%s-Clean-Availability' % SimId, False)
    return [IS,CF,BS]

##################################################################
## Returns list of years for which all statements are available ##
##################################################################
##
def SortAvailableYears(CleanAvailability):
    IS = list(CleanAvailability[0].keys())
    CF = list(CleanAvailability[1].keys())
    BS = list(CleanAvailability[2].keys())
    Output = []
    for x in IS:
        for y in CF:
            for z in BS:
                if x == y == z:
                    Output.append(x)
    Output.sort()
    return Output

##############################################################
## Returns list of years for which full years are available ##
##############################################################
##
def FilterForAnnual(CleanAvailability, Years):
    Output = []
    for x in Years:
        if 'FY' in CleanAvailability[0][x]:
            if 'FY' in CleanAvailability[1][x]:
                if 'Q4' in CleanAvailability[2][x]:
                    Output.append(x)
    return Output

#################################################################
## Returns raw financial statement data for a company ###########
#################################################################
## SimId        = str
## Years        = list, All years for which full year data exists
## Format       = 'standardised' or 'original' (as reported)
## Range        = int, how many years to pull or 'all'
## SaveOutput   = bool, set as True to save raw output locally
##
def PullAnnualFinancials(SimId, Years, Format, Range, SaveOutput=True):
    # Format link
    Link = 'https://simfin.com/api/v1/companies/id/%s/statements/%s'
    Link = Link % (SimId, Format)
    # Output Variable
    Financials = {}
    if Range != 'all':
        Years = Years[-Range:]
    for Year in Years:
        # Params for Income Statement and pull
        Params = {'stype'   : 'pl',
                  'ptype'   : 'FY',
                  'fyear'   : Year,
                  'api-key' : APIKey}
        IS = requests.get(Link, params=Params).json()
        # Change Params for Cash Flow Statement and pull
        Params['stype'] = 'cf'
        CF = requests.get(Link, params=Params).json()
        # Change Params for Balance Sheet and pull
        Params['stype'] = 'bs'
        Params['ptype'] = 'Q4'
        BS = requests.get(Link, params=Params).json()
        # Save three statements to output variable
        Financials[Year] = [IS, CF, BS]
    # Save raw data if called to do so
    if SaveOutput == True:
        SaveToJSON(Financials,
                '%s-%s-A-Financials' % (SimId, str(Range)),
                True)
    return Financials
