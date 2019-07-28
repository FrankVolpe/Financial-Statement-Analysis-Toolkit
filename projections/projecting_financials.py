from fs_calculations import *
from projection_modifications import *

class projected_statements(panel_data):
    def __init__(self, historic_data, years_out):
        self.historic = historic_data
        self.calculations = fs_calculations(self.historic)
        self.all_data = {}
        self.multiplier = {}
        self.set_timeframe(years_out)
        self.set_default()
        self.applicable_lineitems()

    ###############################################
    ## To Initialize projected_statements Object ##
    ###############################################

    def set_timeframe(self, years_out):
        at_T = max(self.historic.data_range)
        self.at_T = self.historic.all_data[at_T]
        self.data_range = list(range(at_T + 1, at_T + 1 + years_out))
        self_at_T_1 = self.at_T
        for x in range(len(self.data_range)):
            self.all_data[self.data_range[x]] = three_statements(proj_income_statement(self_at_T_1.i_s),
                                                                 proj_cash_flow_statement(self_at_T_1.c_f),
                                                                 proj_balance_sheet(self_at_T_1.b_s))
            self.multiplier[self.data_range[x]] = x+1
            self_at_T_1 = self.all_data[self.data_range[x]]
        self.data = {}
        for x in range(len(self.data_range)):
            self.data[self.data_range[x]] = self.all_data[self.data_range[x]].data

    def set_default(self):
        for x in range(len(self.data_range)):
            one_year = self.all_data[self.data_range[x]]
            one_year.i_s.set_default()
            one_year.c_f.set_default()
            one_year.b_s.set_default()
        self.assumptions_log = {'income_statement' : {},
                                'cash_flow_statement' : {},
                                'balance_sheet' : {}}

    def applicable_lineitems(self):
        '''creates attributes used by the base case to decide whether
        or not a line_item needs to be projected.

        line_items that werent used in historic data: self.zero_balance
        line_items calculated by children: self.assumption_log['Not Projected']
        all other line_items: self.to_be_calculated '''

        statements = ['income_statement',
                     'cash_flow_statement',
                     'balance_sheet']
        one_year = self.at_T.data
        ## Properly formats dictionary to record whether line_items are calculated
        check_relevance = {}
        for y in range(len(statements)):
            one_statement = one_year[statements[y]]
            one_statement_lines = list(one_year[statements[y]].keys())
            check_relevance[statements[y]] = {}
            for z in range(len(one_statement_lines)):
                check_relevance[statements[y]][one_statement_lines[z]] = []
        ## Populated dictionary recording whether line_items are calculated
        for x in range(len(self.historic.data_range)):
            one_year = self.historic.data[self.historic.data_range[x]]
            for y in range(len(statements)):
                one_statement = one_year[statements[y]]
                one_statement_lines = list(one_year[statements[y]].keys())
                for z in range(len(one_statement_lines)):
                    check_relevance[statements[y]][one_statement_lines[z]].append(one_statement[one_statement_lines[z]].populated)
        ## Creates dicts of lists of line_items that are
        ## either calculated or not calculated
        calculated = {}
        not_calculated = {}
        for y in range(len(statements)):
            calculated[statements[y]] = []
            not_calculated[statements[y]] = []
            one_statement_lines = list(check_relevance[statements[y]].keys())
            for z in range(len(one_statement_lines)):
                is_populated = sum(check_relevance[statements[y]][one_statement_lines[z]])
                is_true = len(self.historic.data_range) * True
                if is_true != is_populated:
                    calculated[statements[y]].append(one_statement_lines[z])
                else:
                    not_calculated[statements[y]].append(one_statement_lines[z])
        ## Takes note of which values are empty in every year of historic data
        is_zero = {}
        for x in range(len(statements)):
            is_zero[statements[x]] = {}
            positions = not_calculated[statements[x]]
            for y in range(len(positions)):
                is_zero[statements[x]][positions[y]] = []
                for z in range(len(self.historic.data_range)):
                    line_item = self.return_line_item(statements[x],
                                                      positions[y],
                                                      self.historic.data_range[z],
                                                      historic=True)
                    is_zero[statements[x]][positions[y]].append(line_item.data)
        self.zero_balance = {}
        self.to_be_calculated = {}
        for x in range(len(statements)):
            positions = not_calculated[statements[x]]
            self.zero_balance[statements[x]] = []
            self.to_be_calculated[statements[x]] = []
            for y in range(len(positions)):
                values = is_zero[statements[x]][positions[y]]
                count = 0
                for z in range(len(values)):
                    if values[z] == 0:
                        count += 1
                if count == len(self.historic.data_range):
                    self.zero_balance[statements[x]].append(positions[y])
                else:
                    self.to_be_calculated[statements[x]].append(positions[y])
        ## Records which line_items are calculated by natural FS flow in assumptions_log
        self.assumptions_log['Not Projected'] = calculated

    ##############################################
    ## For calling line_items within the object ##
    ##############################################

    def return_line_item(self, statement, position, year=None, historic=False):
        '''Returns line_item object to improve programs legibility,
        year is set to the first year of the projected statement by
        default where only the title is necessary to pull '''
        if historic == False:
            if year == None:
                year = self.data_range[0]
            return self.data[year][statement][position]
        elif historic == True:
            if year == None:
                return self.return_line_item_at_T(statement, position)
            else:
                return self.historic.data[year][statement][position]
        else:
            print("Historic must be True or False. By default it is False")

    def return_line_item_at_T(self, statement, position):
        ''' Returns line_item object at the most recent year of
        historic financials '''
        return self.at_T.data[statement][position]

    #######################################
    ## Projection methods for line_items ##
    #######################################

    def project_by_constant_growth(self, statement, line_position, growth_rate):
        ## Records assumptions appropriately
        if growth_rate != type(metric):
            assumption = {"constant % change" : growth_rate}
        else:
            assumption = {"constant % change" : {growth_rate.title : growth_rate.data}}
            growth_rate = growth_rate.data
        ## Begin calculating and assigning values
        if statement == 'income_statement' or 'balance_sheet' or 'cash_flow_statement':
            value_at_T = self.return_line_item_at_T(statement, line_position).data
            for x in range(len(self.data_range)):
                value_multiplier = (1 + growth_rate)**self.multiplier[self.data_range[x]]
                current_line_item = self.return_line_item(statement,
                                                          line_position,
                                                          self.data_range[x])
                current_line_item.value = value_at_T * value_multiplier
            self.assumptions_log[statement][current_line_item.title] = assumption
        else:
            print("statement variable must equal 'income_statement',")
            print("'balance_sheet', or 'cash_flow_statement'.")

    def project_as_percentage(self, metric, reference_line, projection_line, statement_1, statement_2=None):
        ''' reference_line * metric = projection_line
        reference_line goes with statement_1, projection_line goes with statement_2'''
        percentage = metric.data
        assumption = {'percentage' : {metric.title : percentage}}
        ## If no statement_2 argument, it is assumed reference_line and projection_line
        ## Are from the same statement
        if statement_2 == None:
            if statement_1 == 'income_statement' or 'balance_sheet' or 'cash_flow_statement':
                for x in range(len(self.data_range)):
                    line_item_to_assign = self.return_line_item(statement_1,
                                                                projection_line,
                                                                self.data_range[x])
                    line_item_to_refer_to = self.return_line_item(statement_1,
                                                                  reference_line,
                                                                  self.data_range[x])
                    line_item_to_assign.value = line_item_to_refer_to.data * percentage
                self.assumptions_log[statement_1][line_item_to_assign.title] = assumption
            else:
                print("statement variable must equal 'income_statement',")
                print("'balance_sheet', or 'cash_flow_statement'.")
        else:
            values = {}
            ## Begin Calculating Values
            if statement_1 == 'income_statement' or 'balance_sheet' or 'cash_flow_statement':
                for x in range(len(self.data_range)):
                    line_item_to_refer_to = self.return_line_item(statement_1,
                                                                  reference_line,
                                                                  self.data_range[x])
                    values[self.data_range[x]] = line_item_to_refer_to.data * percentage
            else:
                print("statement variable must equal 'income_statement',")
                print("'balance_sheet', or 'cash_flow_statement'.")
            ## Begin Assigning Values & Recording Assumptions
            if statement_2 == 'income_statement' or 'balance_sheet' or 'cash_flow_statement':
                for x in range(len(self.data_range)):
                    line_item_to_assign = self.return_line_item(statement_2,
                                                                projection_line,
                                                                self.data_range[x])
                    line_item_to_assign.value = values[self.data_range[x]]
                self.assumptions_log[statement_2][line_item_to_assign.title] = assumption
            else:
                print("statement variable must equal 'income_statement',")
                print("'balance_sheet', or 'cash_flow_statement'.")

    def set_constant(self, statement, line_position, value=None, as_mean=False):
        '''utilize either value or as_mean argument '''
        error_testing = 0
        if value != None:
            assumption = {'constant' : {'at the value: ' : value}}
            if statement == 'income_statement' or 'balance_sheet' or 'cash_flow_statement':
                for x in range(len(self.data_range)):
                    current_line_item = self.return_line_item(statement,
                                                              line_position,
                                                              self.data_range[x])
                    current_line_item.value = value
                self.assumptions_log[statement][current_line_item.title] = assumption
            else:
                print("statement variable must equal 'income_statement',")
                print("'balance_sheet', or 'cash_flow_statement'.")
            error_testing += 1
        elif as_mean != False:
            assumption = {'constant' : 'at the historic mean'}
            mean = 0
            if statement == 'income_statement' or 'balance_sheet' or 'cash_flow_statement':
                for x in range(len(self.historic.data_range)):
                    current_line_item = self.return_line_item(statement,
                                                              line_position,
                                                              self.historic.data_range[x],
                                                              historic = True)
                    mean += current_line_item.data
                mean = mean / len(self.historic.data_range)
                for x in range(len(self.data_range)):
                    current_line_item = self.return_line_item(statement,
                                                              line_position,
                                                              self.data_range[x])
                    current_line_item.value = mean
                self.assumptions_log[statement][current_line_item.title] = assumption
            else:
                print("statement variable must equal 'income_statement',")
                print("'balance_sheet', or 'cash_flow_statement'.")
            error_testing += 1
        else:
            print("This function must be given either a value argument")
            print("or have as_mean set as something other than False.")
        if error_testing == 2:
            print("You utilized both options for assigning a constant value")
            print("please review your input for improved efficiency.")

    def from_projection_children(self, statement, line_position):
        assumption = {'calculated' : self.return_line_item(statement,
                                                           line_position).projection_children}
        if statement == 'income_statement' or 'balance_sheet' or 'cash_flow_statement':
            for x in range(len(self.data_range)):
                current_line_item = self.return_line_item(statement,
                                                          line_position,
                                                          self.data_range[x])
                current_line_item.value = sum(current_line_item.projection_children)
            self.assumptions_log[statement][current_line_item.title] = assumption

    ################################################
    ## Assigning Projection Methods to Line Items ##
    ################################################

    def base_case(self):
        # Formats self.projection_settings
        projection_codes = [0, 1, 2, 3, 4, None]
        self.projection_settings = {'income_statement' : {} ,
                                    'cash_flow_statement' : {} ,
                                    'balance_sheet' : {} }
        statements = list(self.projection_settings.keys())
        for x in range(len(statements)):
            for y in range(len(projection_codes)):
                self.projection_settings[statements[x]][projection_codes[y]] = []
            # Populates self.projection_settings with defaults
            reference = self.data[statements[x]]
            positions = list(reference.keys())
            for z in range(len(positions)):
                self.projection_settings[statements[x]][reference[positions[z]].projection_default].append(positions[z])
        ## loop through self.zero_balance for those being set to zero
        to_be_removed = {}
        for x in range(len(statements)):
            set_to_zero = self.zero_balance[statements[x]]
            self.projection_settings[statements[x]][0] = set_to_zero
            to_be_removed[statements[x]] = {}
            for y in range(len(projection_codes)):
                if projection_codes[y] != 0:
                    to_be_removed[statements[x]][projection_codes[y]] = []
                    for z in range(len(set_to_zero)):
                        if set_to_zero[z] in self.projection_settings[statements[x]][projection_codes[y]]:
                            to_be_removed[statements[x]][projection_codes[y]].append(set_to_zero[z])
        ## Remove line_items from self.projection_settings that were changed from default method to be set to zero
        for x in range(len(statements)):
            for y in range(len(projection_codes)):
                removals = to_be_removed[statements[x]][projection_codes[y]]
                for z in range(len(removals)):
                    try:
                        self.projection_settings[statements[x]][projection_codes[y]].remove(removals[z])
                    except ValueError:
                        continue
        ## loop through self.assumptions_log['Not Projected']
        to_be_removed = {}
        for x in range(len(statements)):
            calc_from_children = self.assumptions_log['Not Projected'][statements[x]]
            self.projection_settings[statements[x]][None] = calc_from_children
            to_be_removed[statements[x]] = {}
            for y in range(len(projection_codes)):
                if projection_codes[y] != None:
                    to_be_removed[statements[x]][projection_codes[y]] = []
                    for z in range(len(calc_from_children)):
                        if calc_from_children[z] in self.projection_settings[statements[x]][projection_codes[y]]:
                            to_be_removed[statements[x]][projection_codes[y]].append(calc_from_children[z])
        ## Remove line_items from self.projection_settings that were changed from default method to be calculated
        for x in range(len(statements)):
            for y in range(len(projection_codes)):
                removals = to_be_removed[statements[x]][projection_codes[y]]
                for z in range(len(removals)):
                    try:
                        self.projection_settings[statements[x]][projection_codes[y]].remove(removals[z])
                    except ValueError:
                        continue
        ## loop through line items again to record overrides
        to_be_removed = {}
        for x in range(len(statements)):
            reference = self.data[statements[x]]
            to_be_removed[statements[x]] = {}
            for y in range(len(projection_codes)):
                positions = self.projection_settings[statements[x]][projection_codes[y]]
                to_be_removed[statements[x]][projection_codes[y]] = []
                for z in range(len(positions)):
                    if reference[positions[z]].override == True:
                        try:
                            new_method = reference[positions[z]].override_data[projection_codes[y]]
                            self.projection_settings[statements[x]][new_method].append(positions[z])
                            to_be_removed[statements[x]][projection_codes[y]].append(positions[z])
                        except KeyError:
                            continue
        ## Remove line_items from self.projection_settings that were changed due to an override
        for x in range(len(statements)):
            for y in range(len(projection_codes)):
                removals = to_be_removed[statements[x]][projection_codes[y]]
                for z in range(len(removals)):
                    try:
                        self.projection_settings[statements[x]][projection_codes[y]].remove(removals[z])
                    except ValueError:
                        continue
        ## Update the assumptions_log to reflect overrides from auto-calculated values
        for x in range(len(statements)):
            removals = to_be_removed[statements[x]][projection_codes[None]]
            for z in range(len(removals)):
                try:
                    self.assumptions_log['Not Projected'][statements[x]].remove(removals[z])
                except ValueError:
                    continue

    def modify_projection_methods(self, statement, line_position, new_projection_code):
        pass

    def modify_projection_settings(self, statement, line_position):
        pass

    def calculate(self):
        ## Calculate projections
        pass

    def check_results(self):
        pass


    ################################
    ## For Displaying Assumptions ##
    ################################

    def assumptions_report(self):
        pass

    ############################
    ## Displaying Projections ##
    ############################

    def display_all(self, omit=False, second_index=True):
        frames = [self.historic.display(second_index=second_index),
                  self.display(second_index=second_index)]
        df = pd.concat(frames, axis=1)
        if omit == False:
            return df
        else:
            return df[(df.T != 0).any()]
