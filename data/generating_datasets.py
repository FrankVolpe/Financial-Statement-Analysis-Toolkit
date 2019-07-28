import requests
import json


## Generate all entities with SimFin API
all_entities = requests.get('https://simfin.com/api/v1/info/all-entities?api-key=yjSXF9TUOiYVtZAtbYK7bGNMajVCDk3y').json()

## Save all entities as .json file
with open('simfin_constituents_base.json', 'w') as file:
    json.dump(all_entities, file)
    file.close()

#######################################################################
#######################################################################

## To insure we dont run out of API calls
import time

## For adding more detailed information to entities file
base_link = 'https://simfin.com/api/v1/companies/id/'
link_end = '?api-key=yjSXF9TUOiYVtZAtbYK7bGNMajVCDk3y'

## For compiling new information
new_dict = {}

## Set sleep time to account for API call limit
sleep_time = 60

## Loop through API to call supplemental information
for x in range(len(all_entities)):
    ## Create link
    link = base_link + str(all_entities[x]['simId']) + link_end
    ## Call link
    one_company = requests.get(link).json()
    ## Re-format
    one_company = {all_entities[x]['name'] : one_company}
    ## Add to dict
    entities_v2.update(one_company)
    ## Sleep to avoid maxing out API calls
    time.sleep(sleep_time)

#######################################################################
#######################################################################

## Make sure you didnt call the API too many times

## List of all entities
entities_list = (entities_v2.keys())

## Set count to be the number of entities
count = len(entities_list)

## Directory for failed names
failed_names = []

## Loop through entities to find errors
for x in range(count):
    try:
        ## If error is a key, append entity name to failed_names
        test_var = entities_v2[entities_list[x]]['error']
        failed_names.append(entities_list[x])
    except KeyError:
        continue

## Visualize failed names if any
print(failed_names)

####################################################
### If no failed names show up, skip to line 118 ###
####################################################

#######################################################################
#######################################################################

## Create directory for failed names
failed_names_v2 = []

## Create directory from original variable with entity information
## That variable is 'all_entities'

for x in range(len(failed_names)):
     company = failed_names[x]
     for y in range(len(all_entities)):
         refer = all_entities[y]['name']
         if company == refer:
             failed_names_v2.append(all_entities[y])

## Assert the amount of failed entities is equal on both lists
len(failed_names) == len(failed_names_v2)

## Loop through failed names and save them to entities_v2
for x in range(len(failed_names_v2)):
    one_co = failed_names_v2[x]
    one_simid = str(one_co['simId'])
    one_name = one_co['name']
    entities_v2[one_name] = requests.get(base_link + one_simid + api_key).json()

## Run the error test one more time

## Loop through entities to find errors
for x in range(count):
    try:
        ## If error is a key, append entity name to failed_names
        test_var = entities_v2[entities_list[x]]['error']
        failed_names.append(entities_list[x])
    except KeyError:
        continue

## Visualize failed names if any
print(failed_names)

## Save this information as a .json file
with open('simfin_constituents.json', 'w') as file:
     json.dump(entities_v2, file)
     file.close()

#######################################################################
#######################################################################

## Directory for sectors
all_sectors = {}

## Loop through entities_v2 to populate directory
for x in range(len(entities_list)):
    try:
        all_sectors[entities_v2[entities_list[x]]['sectorCode']] = data[data_keys[x]]['sectorName']
    ## JUUUUUUUUUST in case there are any errors we somehow missed
    except KeyError:
         failed_names.append(entities_list[x])

## Save sectors directory
with open('all_sectors_base.json', 'w') as file:
    json.dump(all_sectors, file)
    file.close()

#######################################################################
#######################################################################

## List of all sector codes
sector_codes = list(all_sectors.keys())

## Combined directory for companies and sectors
sectors_and_companies = {}

## Format directory properly
for x in range(len(sector_codes)):
    sectors_and_companies[sector_codes[x]] = {'sector' : all_sectors[sector_codes[x]],
                                              'companies' : []}

## Add companies to directory
for x in range(len(entities_list)):
    one_company = entities_v2[entities_list[x]]
    current_sector = one_company['sectorCode']
    sectors_and_companies[current_sector]['companies'].append(one_company)

## Save file
with open('sectors_and_companies.json', 'w') as file:
    json.dump(new_format, file)
    file.close()

#######################################################################
#######################################################################

## Set new link_end variable
link_end = '/statements/list?api-key=yjSXF9TUOiYVtZAtbYK7bGNMajVCDk3y'

## Add all available statements to Directory
for x in range(len(sector_codes)):
    current_sector = sectors_and_companies[sector_codes[x]]['companies']
    for y in range(len(current_sector)):
        current_simID = str(current_sector[y]['simId'])
        all_available_statements = requests.get(base_link + current_simID + link_end).json()
        current_sector[y]['availability'] = all_available_statements
        time.sleep(sleep_time)
