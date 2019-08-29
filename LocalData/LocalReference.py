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
    for Entity in AllEntities:
        SimId = str(Entity['simId'])
        try:
            Detail = requests.get(Link % SimId, params=Params).json()
            # Add new data to AllEntities
            Entity['fyearEnd']   = Detail['fyearEnd']
            Entity['employees']  = Detail['employees']
            Entity['sectorName'] = Detail['sectorName']
            Entity['sectorCode'] = Detail['sectorCode']
        except Exception as E:
            # Keep track of errors as they occur
            ReportError('GenData',
                        type(E).__name__,
                        SimId,
                        Entity['name'])
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
    for Entity in AllEntities:
        SimId = str(Entity['simId'])
        try:
            Statements = requests.get(Link % SimId, params=Params).json()
            Entity['Statements'] = Statements
        except Exception as E:
            ReportError('StatementData',
                        type(E).__name__,
                        SimId,
                        Entity['name'])
        WaitTime(Sleep)
    ## Save to file
    with open(path+FName, 'w') as file:
        json.dump(AllEntities, file)
        file.close()
    return AllEntities

######################################################################
## Generate list of Sectors and corresponding codes in AllEntities ###
######################################################################
## { SectorCode : { 'Name'        : SectorName,
##                  'Companies'   : [] }}
##

def SectorCodesJSON(AllEntities, FName='SectorCodes.json'):
    Output = {}
    for Entity in AllEntities:
        try:
            SectorCode = Entity['sectorCode']
            SectorName = Entity['sectorName']
            Output[SectorCode] = {'Name'        : SectorName,
                                  'Companies'   : []}
        except Exception as E:
            ReportError('SectorCode',
                        type(E).__name__,
                        Entity['simId'],
                        Entity['name'])

    ## Save to file
    with open(path+FName, 'w') as file:
        json.dump(Output, file)
        file.close()
    return Output

##########################################################
## Add company names & SimIDs to corresponding sectors ###
##########################################################
## { SectorCode : { 'Name'        : SectorName,
##                  'Companies'   : [ { SimId : Name},
##                                    { SimId : Name} ]}}
##

def SectorConstituentsJSON(AllEntities,
                           SectorCodes,
                           FName='SectorConstituents.json'):
    for Entity in AllEntities:
        try:
            SimId  = Entity['simId']
            Name   = Entity['name']
            Sector = Entity['sectorCode']
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


