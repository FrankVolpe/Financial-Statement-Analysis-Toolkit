from panel_data import *
import copy

## Double check all values are coming from the right place
## Fix metrics that no longer work
## Add metrics from modelling temp and other


class fs_calculations:
    def __init__(self, panel_data):
        self.historic = panel_data
        self.range = self.historic.data_range
        self.new_range = self.range.copy()           # Attribute is the range excluding the first year
        self.new_range.remove(self.new_range[0])     # Attribute is the range excluding the first year
        self.metrics = {}                            # {metric_code : { year : metric object}}
        self.fs_delta()                              # Creates self.delta & self.average_delta
        self.calculate()                             # Populates self.metrics (DataFrame)
        self.days_measures()                         # Creates self.op_cycle (DataFrame)
        self.common_size()

    def fs_delta(self):
        statements = ['income_statement',
                     'balance_sheet',
                     'cash_flow_statement']
        self.delta = {}
        self.average_delta = {}
        for x in range(len(statements)):
            self.delta[statements[x]] = {}
            for y in range(len(self.new_range)):
                positions = list(self.historic.data[self.new_range[y]][statements[x]].keys())
                for z in range(len(positions)):
                    self.delta[statements[x]][positions[z]] = {}
            for y in range(len(self.new_range)):
                positions = list(self.historic.data[self.new_range[y]][statements[x]].keys())
                for z in range(len(positions)):
                    val_at_t = self.historic.data[self.new_range[y]][statements[x]][positions[z]].data
                    val_t_1 = self.historic.data[self.range[y]][statements[x]][positions[z]].data
                    try:
                        self.delta[statements[x]][positions[z]][self.new_range[y]] = val_at_t / val_t_1 - 1
                    except ZeroDivisionError:
                        self.delta[statements[x]][positions[z]][self.new_range[y]] = 0
        for x in range(len(statements)):
            self.average_delta[statements[x]] = {}
            positions = list(self.historic.data[self.new_range[0]][statements[x]].keys())
            for z in range(len(positions)):
                    self.average_delta[statements[x]][positions[z]] = mean(self.delta[statements[x]][positions[z]].values())

    def days_measures(self):
        df = pd.DataFrame()
        for x in range(len(self.new_range)):
            df.at["Days of Sales Outstanding", self.new_range[x]] = 365 / self.metrics['t_1'][self.new_range[x]].data
            df.at["Days of Inventory Outstanding", self.new_range[x]] = 365 / self.metrics['t_2'][self.new_range[x]].data
            df.at["Number of Days of Payables", self.new_range[x]] = 365 / self.metrics['t_6'][self.new_range[x]].data
            df.at["Cash Conversion Cycle", self.new_range[x]] = sum([df.at["Days of Sales Outstanding", self.new_range[x]],
                                                                     df.at["Days of Inventory Outstanding", self.new_range[x]],
                                                                     df.at["Number of Days of Payables", self.new_range[x]] * -1])
            df.at["Defense Interval", self.new_range[x]] = combine_li(self.historic.all_data[self.new_range[x]].b_s.bs_tid_1,
                                                                      self.historic.all_data[self.new_range[x]].b_s.bs_tid_4).data / (self.metrics['s_5'][self.new_range[x]].data / 365)
        self.op_cycle = df

    def calculate(self):
        for x in range(len(self.range)):
            data = self.historic.all_data[self.range[x]]
            new_metric_add(self.metrics,
                           's_1',
                           "EBIT",
                           self.range[x],
                           [data.i_s.is_tid_55,                   # Net Income
                            negate_li(data.i_s.is_tid_44),        # Income Tax Expense
                            negate_li(data.i_s.is_tid_21)])       # Interest Expense
            new_metric_add(self.metrics,
                           's_2',
                           "Total Debt",
                           self.range[x],
                           [data.b_s.bs_tid_47,                   # Short Term Debt
                            data.b_s.bs_tid_58])                  # Long Term Debt
            new_metric_add(self.metrics,
                           's_3',
                           "Working Capital",
                           self.range[x],
                           [data.b_s.bs_tid_21,                   # Current Assets
                            negate_li(data.b_s.bs_tid_57)])       # Current Liabiliities
            new_metric_add(self.metrics,
                           's_4',
                           "EBITDA",
                           self.range[x],
                           [self.metrics['s_1'][self.range[x]],   # EBIT
                            data.c_f.cf_tid_2])                   # Depreciation & Amortization
            new_metric_add(self.metrics,
                           's_5',
                           "Annual Expenditures",
                           self.range[x],
                           [negate_li(data.i_s.is_tid_2),          # Cost of Revenue
                            negate_li(data.i_s.is_tid_11),         # Operating Expenses
                            negate_li(data.c_f.cf_tid_2),          # Depreciation & Amortization
                            negate_li(data.c_f.cf_tid_3)])         # Non-Cash Items
            new_metric_div(self.metrics,
                            's_6',
                            "Tax Rate",
                            self.range[x],
                            negate_li(data.i_s.is_tid_44),         # Current Assets
                            data.i_s.is_tid_43)                    # Current Liabilities
            new_metric_add(self.metrics,
                            's_7',
                            "Total Capital",
                            self.range[x],
                            [self.metrics['s_2'][self.range[x]],    # Total Debt
                             data.b_s.bs_tid_43])                   # Total Equity
            #new_metric_add(self.metrics,
            #               's_',
            #               "Free Cash Flow to the Firm",
            #               self.range[x],
            #               [,                   #
            #                ])                  #
            #new_metric_add(self.metrics,
            #               's_',
            #               "Free Cash Flow to Equity",
            #               self.range[x],
            #               [,                   #
            #                ])                  #
            new_metric_div(self.metrics,
                            'l_1',
                            "Current Ratio",
                            self.range[x],
                            data.b_s.bs_tid_21,                    # Current Assets
                            data.b_s.bs_tid_57)                    # Current Liabilities
            new_metric_div(self.metrics,
                            'l_2',
                            "Quick Ratio",
                            self.range[x],
                            combine_li(data.b_s.bs_tid_1,          # Cash & Equivalents
                                       data.b_s.bs_tid_4),         # Accounts Receivable
                            data.b_s.bs_tid_57)                    # Current Liabilities
            new_metric_div(self.metrics,
                            'l_3',
                            "Cash Ratio",
                            self.range[x],
                            data.b_s.bs_tid_1,                     # Cash & Equivalents
                            data.b_s.bs_tid_57)                    # Current Liabilities
            new_metric_div(self.metrics,
                            'm_1',
                            "Gross Profit Margin",
                            self.range[x],
                            data.i_s.is_tid_4,                     # Gross Profit
                            data.i_s.is_tid_1)                     # Revenue
            new_metric_div(self.metrics,
                            'm_2',
                            "Operating Profit Margin",
                            self.range[x],
                            data.i_s.is_tid_19,                    # Operating Income
                            data.i_s.is_tid_1)                     # Revenue
            new_metric_div(self.metrics,
                            'm_3',
                            "Pretax Margin",
                            self.range[x],
                            data.i_s.is_tid_43,                    # Pre-Tax Income
                            data.i_s.is_tid_1)                     # Revenue
            new_metric_div(self.metrics,
                            'm_4',
                            "Net Profit Margin",
                            self.range[x],
                            data.i_s.is_tid_55,                    # Net Income
                            data.i_s.is_tid_1)                     # Revenue
            new_metric_div(self.metrics,
                           'so_1',
                           "Debt to Equity",
                           self.range[x],
                           self.metrics['s_2'][self.range[x]],     # Total Debt
                           data.b_s.bs_tid_84)                     # Total Equity
            new_metric_div(self.metrics,
                           'so_2',
                           "Debt to Capital",
                           self.range[x],
                           self.metrics['s_2'][self.range[x]],     # Total Debt
                           combine_li(data.b_s.bs_tid_84,          # Total Equity
                                       self.metrics['s_2'][self.range[x]]))   # Total Debt
            new_metric_div(self.metrics,
                           'so_3',
                           "Debt to Assets",
                           self.range[x],
                           self.metrics['s_2'][self.range[x]],     # Total Debt
                           data.b_s.bs_tid_41)                     # Total Assets
            new_metric_div(self.metrics,
                           'so_4',
                           "Interest Coverage",
                           self.range[x],
                           self.metrics['s_1'][self.range[x]],     # EBIT
                           negate_li(data.i_s.is_tid_21))          # Interest Expense
        ###########################################################
        ###########################################################
        ## Start metrics that require 2 years of data to compute ##
        ###########################################################
        ###########################################################
        for x in range(len(self.new_range)):
            data = self.historic.all_data[self.new_range[x]]  # three_statements object at T
            t_1_data = self.historic.all_data[self.range[x]]  # three_statements object at T-1
            new_metric_add(self.metrics,
                           's_9',
                           "Purchases",
                           self.new_range[x],
                           [data.b_s.bs_tid_8,                       # Inventory
                            negate_li(t_1_data.b_s.bs_tid_8),        # Inventory T-1
                            negate_li(data.i_s.is_tid_2)])           # Cost of Sales
            new_metric_div(self.metrics,
                           'so_5',
                           "Financial Leverage",
                           self.new_range[x],
                           mean_li(data.b_s.bs_tid_41,             # Total Assets
                                   t_1_data.b_s.bs_tid_41),        # Total Assets at T-1
                           mean_li(data.b_s.bs_tid_84,             # Total Equity
                                   t_1_data.b_s.bs_tid_84))        # Total Equity at T-1
            new_metric_div(self.metrics,
                           'p_1',
                           "Return on Assets",
                           self.new_range[x],
                           data.i_s.is_tid_55,                     # Net Income
                           mean_li(data.b_s.bs_tid_41,             # Total Assets
                                   t_1_data.b_s.bs_tid_41))        # Total Assets at T-1
            new_metric_div(self.metrics,
                           'p_2',
                           "Operating ROA",
                           self.new_range[x],
                           data.i_s.is_tid_19,                     # Operating Income
                           mean_li(data.b_s.bs_tid_41,             # Total Assets
                                   t_1_data.b_s.bs_tid_41))        # Total Assets at T-1
            new_metric_div(self.metrics,
                           'p_3',
                           "Return on Total Capital",
                           self.new_range[x],
                           self.metrics['s_1'][self.new_range[x]], # Operating Income
                           mean_li(self.metrics['s_7'][self.new_range[x]], # Total Capital
                                   self.metrics['s_7'][self.range[x]]))    # Total Capital at T-1
            new_metric_div(self.metrics,
                           'p_4',
                           "Return on Equity",
                           self.new_range[x],
                           data.i_s.is_tid_55,                     # Net Income
                           mean_li(data.b_s.bs_tid_84,             # Total Equity
                                   t_1_data.b_s.bs_tid_84))        # Total Equity at T-1
            #new_metric_div(self.metrics,
            #               'p_5',
            #               "Return on Common Equity",
            #               self.new_range[x],
            #               data.i_s.is_tid_58,                     # Net Income (available to common shares)
            #               )
            new_metric_div(self.metrics,
                           't_1',
                           "Receivables Turnover",
                           self.new_range[x],
                           data.i_s.is_tid_1,                        # Revenue
                           mean_li(data.b_s.bs_tid_4,                # Accounts Receivable
                                   t_1_data.b_s.bs_tid_4))           # Accounts Receivable T-1
            new_metric_div(self.metrics,
                           't_2',
                           "Inventory Turnover",
                           self.new_range[x],
                           negate_li(data.i_s.is_tid_2),                        # Cost of Revenue
                           mean_li(data.b_s.bs_tid_8,                # Inventory
                                   t_1_data.b_s.bs_tid_8))           # Inventory T-1
            new_metric_div(self.metrics,
                           't_3',
                           "Total Asset Turnover",
                           self.new_range[x],
                           data.i_s.is_tid_1,                        # Revenue
                           mean_li(data.b_s.bs_tid_41,               # Total Assets
                                   t_1_data.b_s.bs_tid_41))          # Total Assets T-1

            new_metric_div(self.metrics,
                           't_5',
                           "Fixed Asset Turnover",
                           self.new_range[x],
                           data.i_s.is_tid_1,                        # Revenue
                           mean_li(data.b_s.bs_tid_22,               # Net PP & E
                                   t_1_data.b_s.bs_tid_22))          # Net PP & E T-1
            new_metric_div(self.metrics,
                           't_6',
                           "Payables Turnover",
                           self.new_range[x],
                           self.metrics['s_9'][self.new_range[x]],    # Purchases
                           mean_li(data.b_s.bs_tid_42,                # Accounts Payable
                                   t_1_data.b_s.bs_tid_42))           # Accounts Payable T-1
            new_metric_div(self.metrics,
                           't_7',
                           "Working Capital Turnover",
                           self.new_range[x],
                           data.i_s.is_tid_1,                          # Revenue
                           mean_li(self.metrics['s_3'][self.range[x]], # Working Capital
                                   self.metrics['s_3'][self.new_range[x]])) # Working Capital T-1

    def deep_dive_display(self):
        '''displays metrics as well as the
        line items used to calculate them'''
        pass

    def key_reference(self):
        ''' Displays metrics and corresponding keys '''
        ref_keys = list(self.metrics.keys())
        df = pd.DataFrame(index=ref_keys, columns = ['Line Item', 'Available Periods'])
        for x in range(len(ref_keys)):
            one_metric = self.metrics[ref_keys[x]]
            available_years = list(one_metric.keys())
            df.at[ref_keys[x], 'Available Periods'] = available_years
            df.at[ref_keys[x], 'Line Item'] = one_metric[available_years[0]].title
        return df.sort_index()

    def display(self, key='all'):
        '''key = 'all' produces all metrics'''
        df = pd.DataFrame()
        if key == 'all':
            frames = []
            metrics_keys = list(self.metrics.keys())
            for x in range(len(metrics_keys)):
                frames.append(self.display(metrics_keys[x]))
            return pd.concat(frames)
        else:
            try:
                data = self.metrics[key]
                for x in range(len(self.range)):
                    try:
                        df.at[data[self.range[x]].title, self.range[x]] = data[self.range[x]].data
                    except KeyError:
                        years = list(data.keys())
                        title = data[years[0]].title
                        df.at[title, self.range[x]] = float('NaN')
            except KeyError:
                print("The key you entered is not valid. See below for valid keys.")
                print(self.metrics.keys())
            return df

    def common_size(self):
        statements = {'income_statement': 0,
                      'balance_sheet': 40}
        self.common_size = {}
        stmt_keys = list(statements.keys())
        for x in range(len(stmt_keys)):
            for y in range(len(self.range)):
                self.common_size[self.range[y]] = {stmt_keys[x] : {}}
                positions = list(self.historic.data[self.range[y]][stmt_keys[x]].keys())
                denominator = self.historic.data[self.range[y]][stmt_keys[x]][statements[stmt_keys[x]]].data
                for z in range(len(positions)):
                    cs_measure = self.historic.data[self.range[y]][stmt_keys[x]][positions[z]].data / denominator
                    self.common_size[self.range[y]][stmt_keys[x]][positions[z]] = cs_measure
