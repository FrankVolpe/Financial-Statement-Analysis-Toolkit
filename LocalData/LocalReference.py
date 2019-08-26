import requests
import json
import time

path = 'reference/'

## Pull API Key and save as variable
with open("../APIKey.txt", 'r') as file:
    APIKey = file.read().replace('\n', '')
    file.close()

###########################################################
## Sleep to avoid maxing out API Calls. Can be opted out ##
###########################################################

def WaitTime(Sleep):
    if Sleep == True:
        time.sleep(45)

#############################################
## Report errors to correct after the fact ##
#############################################

ErrorReport = []

def ReportError(Operation,
                ExceptType,
                SimId,
                CompanyName,
                ErrorReport=ErrorReport):
    print('Unable to save data for ' + CompanyName)
    print('This occured while pulling' + Operation +'\n')
    ErrorReport.append({'O'     :   Operation,
                        'E'     :   ExceptType,
                        'ID'    :   SimId,
                        'N'     :   CompanyName})

#######################################################################
## .json file with all entities in the SIMFIN database, format below: #
#######################################################################
##[{ "name": "Apple Inc",
##   "simId": 111052,
##   "ticker": "AAPL"}]

def AllEntitiesJSON(FName='AllEntities.json',
                    Sleep=True,
                    APIKey=APIKey):
    ## Link Information
    Link  = 'https://simfin.com/api/v1/info/all-entities'
    Params    = {'api-key' : APIKey}
    ## Pull From API
    AllEntities = requests.get(Link, params=Params).json()
    WaitTime(Sleep)
    ## Save to file
    with open(path+FName, 'w') as file:
        json.dump(AllEntities, file)
        file.close()
    return AllEntities

##################################################################
## More detailed information to AllEntities Data, format below: ##
##################################################################
##[{ "simId"     : 111052,
##   "name"      : "Apple Inc",
##   "ticker"    : "AAPL",
##   "fyearEnd"  : 9,
##   "employees" : 120301,
##   "sectorName": "Computer Hardware",
##   "sectorCode": 101001 }]

def GeneralDataJSON(AllEntities,
                    FName='AllEntitiesDetail.json',
                    Sleep=True,
                    APIKey=APIKey):
    ## Link Information
    Link = 'https://simfin.com/api/v1/companies/id/%s'
    Params = {'api-key' : APIKey}
    ## Loop through AllEntities
    for x in range(len(AllEntities)):
        SimId = str(AllEntities[x]['simId'])
        try:
            Detail = requests.get(Link % SimId, params=Params).json()
            # Add new data to AllEntities
            AllEntities[x]['fyearEnd']   = Detail['fyearEnd']
            AllEntities[x]['employees']  = Detail['employees']
            AllEntities[x]['sectorName'] = Detail['sectorName']
            AllEntities[x]['sectorCode'] = Detail['sectorCode']
        except Exception as E:
            # Keep track of errors as they occur
            ReportError('GenData',
                        type(E).__name__,
                        SimId,
                        AllEntities[x]['name'])
        WaitTime(Sleep)
    ## Save to file
    with open(path+FName, 'w') as file:
        json.dump(AllEntities, file)
        file.close()
    return AllEntities

#############################################
## Add Available Statements to AllEntities ##
#############################################
##{"pl": [{"period": "Q1",
##          "fyear": 2017,
##          "calculated": false}],
## "bs": [{"period": "Q1",
##         "fyear": 2017,
##         "calculated": false}],
## "cf": [{"period": "Q1",
##         "fyear": 2017,
##         "calculated": false}]}
## This is the value associated with key 'Statements'

def AvailableStatementsJSON(AllEntities,
                            FName='AvailableStatements.json',
                            Sleep=True,
                            APIKey=APIKey):
    ## Link Information
    Link = 'https://simfin.com/api/v1/companies/id/%s/statements/list'
    Params = {'api-key' : APIKey}
    ## Loop through AllEntities
    for x in range(len(AllEntities)):
        SimId = str(AllEntities[x]['simId'])
        try:
            Statements = requests.get(Link % SimId, params=Params).json()
            AllEntities[x]['Statements'] = Statements
        except Exception as E:
            ReportError('StatementData',
                        type(E).__name__,
                        SimId,
                        AllEntities[x]['name'])
        WaitTime(Sleep)
    ## Save to file
    with open(path+FName, 'w') as file:
        json.dump(AllEntities, file)
        file.close()
    return AllEntities

######################################################################
## Generate list of Sectors and corresponding codes in AllEntities ###
######################################################################

def SectorCodesJSON(AllEntities, FName='SectorCodes.json'):
    Output = {}
    for x in range(len(AllEntities)):
        try:
            SectorCode = AllEntities[x]['sectorCode']
            SectorName = AllEntities[x]['sectorName']
            Output[SectorCode] = {'Name'        : SectorName,
                                  'Companies'   : []}
        except Exception as E:
            ReportError('SectorCode',
                        type(E).__name__,
                        AllEntities[x]['simId'],
                        AllEntities[x]['name'])

    ## Save to file
    with open(path+FName, 'w') as file:
        json.dump(Output, file)
        file.close()
    return Output

##########################################################
## Add company names & SimIDs to corresponding sectors ###
##########################################################

def SectorConstituentsJSON(AllEntities,
                           SectorCodes,
                           FName='SectorConstituents.json'):
    for x in range(len(AllEntities)):
        try:
            SimId  = AllEntities[x]['simId']
            Name   = AllEntities[x]['name']
            Sector = AllEntities[x]['sectorCode']
            SectorCodes[Sector]['Companies'].append({SimId : Name})
        except Exception as E:
            ReportError('SectorConstituent',
                        type(E).__name__,
                        SimId,
                        Name)
    ## Save to file
    with open(path+FName, 'w') as file:
        json.dump(SectorCodes, file)
        file.close()
    return SectorCodes


