from three_stmts import *
from simfin_basics import *

#######################################
## Used to link all three statements ##
#######################################

class three_statements:
    def __init__(self, income_statement, cash_flow_statement, balance_sheet, period=None):
        self.i_s = income_statement
        self.c_f = cash_flow_statement
        self.b_s = balance_sheet
        self.period = period
        self.data = {'income_statement' : self.i_s.create_reference(),
                     'cash_flow_statement' : self.c_f.create_reference(),
                     'balance_sheet' : self.b_s.create_reference()}

    def set_period(self, period):
        self.period = period

    def display_3s(self, omit=False):
        i_s = self.i_s.display(omit)
        c_f = self.c_f.display(omit)
        b_s = self.b_s.display(omit)
        return [i_s, c_f, b_s]

    def display_line_items(self, format='Series'):
        reference = { **self.i_s.__dict__,
                      **self.c_f.__dict__,
                      **self.b_s.__dict__ }
        ref_list = list(reference.keys())
        for x in range(len(ref_list)):
            reference[ref_list[x]] = reference[ref_list[x]].title
        if format == 'Series':
            return pd.Series(reference)
        else:
            return reference

#########################################################
## Link multiple periods of three financial statements ##
#########################################################

class panel_data:
    def __init__(self, data=None):
    # Proper format is data[period] = three_statements object
        if data:
            self.add_data_from_dict(data)


    def add_data_from_dict(self, data):
        self.data_range = list(data.keys())
        self.data_range.sort()
        self.all_data = data
        self.data = {}
        for x in range(len(self.data_range)):
            self.data[self.data_range[x]] = self.all_data[self.data_range[x]].data


    def display(self, omit=False, second_index=True):
        display_dict = {}
        if second_index == True:
            for x in range(len(self.data_range)):
                display_dict[self.data_range[x]] = pd.concat(self.all_data[self.data_range[x]].display_3s(),
                                                             keys=['Income Statement',
                                                                   'Cash Flow Statement',
                                                                   'Balance Sheet'])
        else:
            for x in range(len(self.data_range)):
                display_dict[self.data_range[x]] = pd.concat(self.all_data[self.data_range[x]].display_3s())
        df = pd.DataFrame(display_dict)
        if omit == False:
            return df
        else:
            return df[(df.T != 0).any()]

###########################################
## Function creates five_year_panel_data ##
####### object populated with data ########
###########################################

def upload(ticker):
    panel_dict = {}
    try:
        id = check_ticker(ticker)
        data_years = statement_test(id)
        raw_data = data_call(id, data_years)
    except ConnectionError:
        print("Program could not connect to internet when attempting to pull data from ", ticker, ".")
        print("Because of this, it will be halted for 5 minutes. Please fix network connection.")
    for x in range(len(data_years)):
        i_s = income_statement(raw_data[data_years[x]][0])
        c_f = cash_flow_statement(raw_data[data_years[x]][1])
        b_s = balance_sheet(raw_data[data_years[x]][2])
        panel_dict[data_years[x]] = three_statements(i_s, c_f, b_s)
    return panel_data(panel_dict)
