import requests
import json

global_api_key = ""

def check_ticker(ticker):                                       ## Look up if ticker is available in simfin
    api_key = "?api-key=" + global_api_key               # used to construct API link
    base_link = "https://simfin.com/api/v1/info/find-id/ticker/"        # used to construct API link
    API_html = base_link + ticker.upper() + api_key                     # creates API link
    API_output = requests.get(API_html).json()                          # requests data from API link
    try:
        if 'simId' in API_output[0].keys():                         ## Checks if there is a SimFin ID for ticker
            id = str(API_output[0]['simId'])                        ## Assigns SimFin ID to a variable
            return id
    except ValueError:
        return "error"

def statement_test(sim_id):                                     ## Tests if statements are available
    api_key = "/statements/list?api-key=" + global_api_key     # used to construct API link
    base_link = "https://simfin.com/api/v1/companies/id/"                     # used to construct API link
    API_html = base_link + sim_id + api_key                                   # creates API link
    API_output = requests.get(API_html).json()                                # requests data from API link
    try:
        if "bs" and "cs" and "pl" in API_output:                    ## Ensures all 3 financial statements are available for ticker
            is_op = API_output['pl']
            cf_op = API_output['cf']
            bs_op = API_output['bs']
            return compat_test(is_op, bs_op, cf_op)
    except ValueError:
        return "error"

def compat_test(is_op, bs_op, cf_op):
    op1 = available_statements(is_op, 'FY')
    op2 = available_statements(bs_op, 'Q4')
    op3 = available_statements(cf_op, 'FY')
    if op1 <= op2 and op3:
        years = op1
    elif op2 <= op1 and op3:
        years = op2
    else:
        years = op3
    years.sort()
    return years[-5:]

def available_statements(op, period):
    desired_stmnts = []
    for x in range(len(op)):
        stmt_data = op[x]
        if stmt_data['period'] == period:
            stmt_year = stmt_data['fyear']
            desired_stmnts.append(stmt_year)
    return desired_stmnts

def data_call(sim_id, years):
    base_link = "https://simfin.com/api/v1/companies/id/" + str(sim_id)
    pull_is = "/statements/standardised?stype=pl&ptype=FY&fyear="
    pull_bs = "/statements/standardised?stype=bs&ptype=q4&fyear="
    pull_cf = "/statements/standardised?stype=cf&ptype=FY&fyear="
    api_key = "&api-key=" + global_api_key
    data = {}
    for x in range(len(years)):
        current_year = []
        loop_year = years[x]
        is_api_link = base_link + pull_is + str(loop_year) + api_key
        cf_api_link = base_link + pull_cf + str(loop_year) + api_key
        bs_api_link = base_link + pull_bs + str(loop_year) + api_key
        income_statement = requests.get(is_api_link).json()
        cash_flow_statement = requests.get(cf_api_link).json()
        balance_sheet = requests.get(bs_api_link).json()
        current_year = [income_statement,
                        cash_flow_statement,
                        balance_sheet]
        data[loop_year] = current_year
    return data
