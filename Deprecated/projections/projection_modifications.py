from base_classes import *

###############
## Line Item ##
###############

class projected_line_item:
    '''When searching for the value of the line item, use data() function '''
    def __init__(self, title, method=None, line_position=None, parent=None):
    # Set values for class
        self.line_position = line_position
        self.parent = parent
        self.children = []
        self.title = title
    # For projections
        self.projection_default = method
        self.override = False
    # Add line item to children of parent line item
        if parent:
            self.parent.add_child(self)

    def add_child(self, child):
        ''' Function to add children to line item '''
        self.children.append(child)

    @property
    def data(self):
        ''' Ensures calculated line items are populated correctly '''
        if len(self.children) == 0:
            return self.value
        else:
            children_sum = sum([child.value for child in self.children])
            if self.value == 0:
                self.value = children_sum
                return self.value
            elif self.value == children_sum and self.value != 0:
                return self.value
            else:
                return self.value

    def set_projection_children(self, projection_children):
        ''' For projection method 4 which utilizes other
        line_items to assign a value

        projection_children should be a list, with line_items
        negated appropriately'''
        self.projection_children = projection_children

    def set_default_ratio(self, reference_line_item, metric):
        ''' For projection method 4 which utilizes another
        line_item and a metric to assign a value '''
        self.reference_metric = metric
        self.reference_line = reference_line_item

    def set_override(self, override_data):
        ''' will override naturally suggested projection methods

        override_data should be in format:
        {method to be overriden : replacement method} '''
        self.override = True
        self.override_data = override_data

    def assign_method(self, method_code):
        self.assigned_method = method_code

#######################################
## Functions for Projection Children ##
#######################################

class proj_income_statement(financial_statement):
    ''' __init__ will create the necessary accounts for an income statement.
    --------------------------------------------------------------------------
    No data must be added initially, use function add_data for this '''
    def __init__(self, self_at_T_1):
        self.at_T_1 = self_at_T_1
    ####################################
    ## Final Line Of Income Statement ##
    ####################################
        self.is_tid_58 = projected_line_item('Net Income Available to Common Shareholders', 57)
    ####################################
    ## Net Income & Final Adjustments ##
    ####################################
        self.is_tid_55 = projected_line_item('Net Income',
                                            54,
                                            parent=self.is_tid_58)
        self.is_tid_56 = projected_line_item('Preferred Dividends',
                                            method=2,
                                            55,
                                            parent=self.is_tid_58)
        self.is_tid_57 = projected_line_item('Other Adjustments',
                                            method=1,
                                            56,
                                            parent=self.is_tid_58)
    ####################################
    ## Factoring In Minority Interest ##
    ####################################
        self.is_tid_53 = projected_line_item('Income (Loss) Including Minority Interest',
                                            52,
                                            parent=self.is_tid_55)
        self.is_tid_54 = projected_line_item('Minority Interest',
                                            method=2,
                                            53,
                                            parent=self.is_tid_55)
    #########################
    ## Extraordinary Items ##
    #########################
        self.is_tid_50 = projected_line_item('Net Extraordinary Gains (Losses)',
                                            method=1,
                                            49,
                                            parent=self.is_tid_53)
        self.is_tid_51 = projected_line_item('     Discontinued Operations',
                                            method=1,
                                            50,
                                            parent=self.is_tid_50)
        self.is_tid_52 = projected_line_item('     XO & Accounting Charges & Other',
                                            method=1,
                                            51,
                                            parent=self.is_tid_50)
    ########################
    ## Income After Taxes ##
    ########################
        self.is_tid_49 = projected_line_item('Income (Loss) from Continuing Operations',
                                            48,
                                            parent=self.is_tid_53)
        self.is_tid_48 = projected_line_item('Income (Loss) from Affiliates, net of taxes',
                                            method=2,
                                            47,
                                            parent=self.is_tid_49)
    ####################
    ## Pre-Tax Income ##
    ####################
        self.is_tid_43 = projected_line_item('Pretax Income (Loss)',
                                            42,
                                            parent=self.is_tid_49)
        self.is_tid_28 = projected_line_item('Pretax Income (Loss), Adjusted',
                                            27,
                                            parent=self.is_tid_43)
    #################
    ## Tax Expense ##
    #################
        self.is_tid_44 = projected_line_item('Income Tax (Expense) Benefit, net',
                                            method=3,
                                            43,
                                            parent=self.is_tid_49)
        self.is_tid_44.set_default_ratio()
        self.is_tid_45 = projected_line_item('     Current Income Tax',
                                            method=3,
                                            44,
                                            parent=self.is_tid_44)
        self.is_tid_45.set_default_ratio()
        self.is_tid_46 = projected_line_item('     Deferred Income Tax',
                                            method=1,
                                            45,
                                            parent=self.is_tid_44)
        self.is_tid_47 = projected_line_item('     Tax Allowance/Credit',
                                            method=1,
                                            46,
                                            parent=self.is_tid_44)
    ####################################
    ## Abnormal Activities & Children ##
    ####################################
        self.is_tid_29 = projected_line_item('Abnormal Gains (Losses)',
                                            method=1,
                                            28,
                                            parent=self.is_tid_43)
        self.is_tid_30 = projected_line_item('     Acquired In-Process R&D',
                                            method=1,
                                            29,
                                            parent=self.is_tid_29)
        self.is_tid_31 = projected_line_item('     Merger / Acquisition Expense',
                                            method=1,
                                            30,
                                            parent=self.is_tid_29)
        self.is_tid_32 = projected_line_item('     Abnormal Derivatives',
                                            method=1,
                                            31,
                                            parent=self.is_tid_29)
        self.is_tid_33 = projected_line_item('     Disposal of Assets',
                                            method=1,
                                            32,
                                            parent=self.is_tid_29)
        self.is_tid_34 = projected_line_item('     Early extinguishment of Debt',
                                            method=1,
                                            33,
                                            parent=self.is_tid_29)
        self.is_tid_35 = projected_line_item('     Asset Write-Down',
                                            method=1,
                                            34,
                                            parent=self.is_tid_29)
        self.is_tid_36 = projected_line_item('     Impairment of Goodwill & Intangibles',
                                            method=1,
                                            35,
                                            parent=self.is_tid_29)
        self.is_tid_37 = projected_line_item('     Sale of Business',
                                            method=1,
                                            36,
                                            parent=self.is_tid_29)
        self.is_tid_38 = projected_line_item('     Legal Settlement',
                                            method=1,
                                            37,
                                            parent=self.is_tid_29)
        self.is_tid_39 = projected_line_item('     Restructuring Charges',
                                            method=1,
                                            38,
                                            parent=self.is_tid_29)
        self.is_tid_40 = projected_line_item('     Sale of and Unrealized Investments',
                                            method=1,
                                            39,
                                            parent=self.is_tid_29)
        self.is_tid_41 = projected_line_item('     Insurance Settlement',
                                            method=1,
                                            40,
                                            parent=self.is_tid_29)
        self.is_tid_42 = projected_line_item('     Other Abnormal Items',
                                            method=1,
                                            41,
                                            parent=self.is_tid_29)
    ##############################
    ## Non-Operating Activities ##
    ##############################
        self.is_tid_20 = projected_line_item('Non-Operating Income (Loss)',
                                            19,
                                            parent=self.is_tid_28)
        self.is_tid_21 = projected_line_item('     Interest Expense, net',
                                            method=3,
                                            20,
                                            parent=self.is_tid_20)
        self.is_tid_21.set_default_ratio()
        self.is_tid_22 = projected_line_item('       Interest Expense',
                                            method=3,
                                            21,
                                            parent=self.is_tid_21)
        self.is_tid_22.set_default_ratio()
        self.is_tid_23 = projected_line_item('       Interest Income',
                                            method=3,
                                            22,
                                            parent=self.is_tid_21)
        self.is_tid_23.set_default_ratio()
        self.is_tid_24 = projected_line_item('     Other Investment Income (Loss)',
                                            method=1,
                                            23,
                                            parent=self.is_tid_20)
        self.is_tid_25 = projected_line_item('     Foreign Exchange Gain (Loss)',
                                            method=1,
                                            24,
                                            parent=self.is_tid_20)
        self.is_tid_26 = projected_line_item('     Income (Loss) from Affiliates',
                                            method=1,
                                            25,
                                            parent=self.is_tid_20)
        self.is_tid_27 = projected_line_item('     Other Non-Operating Income (Loss)',
                                            method=1,
                                            26,
                                            parent=self.is_tid_20)
    ######################
    ## Operating Income ##
    ######################
        self.is_tid_19 = projected_line_item('Operating Income (Loss)',
                                            18,
                                            parent=self.is_tid_28)
        self.is_tid_10 = projected_line_item('     Other Operating Income',
                                            method=1,
                                            9,
                                            parent=self.is_tid_19)
    ###################################
    ## Operating Expenses & Children ##
    ###################################
        self.is_tid_11 = projected_line_item('Operating Expenses',
                                            method=3,
                                            10,
                                            parent=self.is_tid_19)
        self.is_tid_11.set_default_ratio()
        self.is_tid_12 = projected_line_item('     Selling, General & Administrative',
                                            method=3,
                                            11,
                                            parent=self.is_tid_11)
        self.is_tid_12.set_default_ratio()
        self.is_tid_13 = projected_line_item('       Selling & Marketing',
                                            method=3,
                                            12,
                                            parent=self.is_tid_12)
        self.is_tid_13.set_default_ratio()
        self.is_tid_14 = projected_line_item('       General & Administrative',
                                            method=3,
                                            13,
                                            parent=self.is_tid_12)
        self.is_tid_14.set_default_ratio()
        self.is_tid_15 = projected_line_item('     Research & Development',
                                            method=2,
                                            14,
                                            parent=self.is_tid_11)
        self.is_tid_16 = projected_line_item('     Depreciation & Amortization',
                                            method=3,
                                            15,
                                            parent=self.is_tid_11)
        self.is_tid_16.set_default_ratio()
        self.is_tid_17 = projected_line_item('     Provision For Doubtful Accounts',
                                            method=3,
                                            16,
                                            parent=self.is_tid_11)
        self.is_tid_17.set_default_ratio()
        self.is_tid_18 = projected_line_item('     Other Operating Expense',
                                            method=1,
                                            17,
                                            parent=self.is_tid_11)
    ##################
    ## Gross Profit ##
    ##################
        self.is_tid_4 = projected_line_item('Gross Profit',
                                            8,
                                            parent=self.is_tid_19)
    ##############################
    ## Cost of Sales & Children ##
    ##############################
        self.is_tid_2 = projected_line_item('Cost of revenue',
                                            method=3,
                                            4,
                                            parent=self.is_tid_4)
        self.is_tid_2.set_default_ratio()
        self.is_tid_7 = projected_line_item('     Cost of Goods & Services',
                                            method=3,
                                            5,
                                            parent=self.is_tid_2)
        self.is_tid_7.set_default_ratio()
        self.is_tid_8 = projected_line_item('     Cost of Financing Revenue',
                                            method=3,
                                            6,
                                            parent=self.is_tid_2)
        self.is_tid_8.set_default_ratio()
        self.is_tid_9 = projected_line_item('     Cost of Other Revenue',
                                            method=3,
                                            7,
                                            parent=self.is_tid_2)
        self.is_tid_9.set_default_ratio()
    ########################
    ## Revenue & Children ##
    ########################
        self.is_tid_1 = projected_line_item('Revenue',
                                            method=2,
                                            0,
                                            parent=self.is_tid_4)
        self.is_tid_3 = projected_line_item('     Sales & Services Revenue',
                                            method=2,
                                            1,
                                            parent=self.is_tid_1)
        self.is_tid_5 = projected_line_item('     Financing Revenue',
                                            method=2,
                                            2,
                                            parent=self.is_tid_1)
        self.is_tid_6 = projected_line_item('     Other Revenue',
                                            method=2,
                                            3,
                                            parent=self.is_tid_1)


class proj_cash_flow_statement(financial_statement):
    ''' __init__ will create the necessary accounts for a cash flow statement.'''
    def __init__(self, self_at_T_1):
        self.at_T_1 = self_at_T_1
    #######################################
    ## Final Line Of Cash Flow Statement ##
    #######################################
        self.cf_tid_46 = projected_line_item('Net Changes in Cash', 51)
    ######################################
    ## Factoring In FX Gains and Losses ##
    ######################################
        self.cf_tid_44 = projected_line_item('     Effect of Foreign Exchange Rates',
                                              method=1,
                                              50,
                                              parent=self.cf_tid_46)
        self.cf_tid_55 = projected_line_item('Net Cash Before FX',
                                              49,
                                              parent=self.cf_tid_46)
    ##########################################
    ## Factoring in Discontinued Operations ##
    ##########################################
        self.cf_tid_56 = projected_line_item('Net Cash Before Disc. Operations and FX',
                                              47,
                                              parent=self.cf_tid_55)
        self.cf_tid_45 = projected_line_item('     Change in Cash from Disc. Operations and Other',
                                              method=1,
                                              48,
                                              parent=self.cf_tid_55)
    ####################################
    ## Cash From Operating Activities ##
    ####################################
        self.cf_tid_13 = projected_line_item('Cash from Operating Activities',
                                              15,
                                              parent=self.cf_tid_56)
    ###########################
    ## Net Income & Children ##
    ###########################
        self.cf_tid_1 = projected_line_item('Net Income/Starting Line',
                                             method=4,
                                             0,
                                             parent=self.cf_tid_13)
        self.cf_tid_1.set_projection_children()
        self.cf_tid_47 = projected_line_item('     Net Income',
                                              method=4,
                                              1,
                                              parent=self.cf_tid_1)
        self.cf_tid_47.set_projection_children()
        self.cf_tid_48 = projected_line_item('     Net Income From Discontinued Operations',
                                              method=4,
                                              2,
                                              parent=self.cf_tid_1)
        self.cf_tid_48.set_projection_children()
        self.cf_tid_49 = projected_line_item('     Other Adjustments',
                                              method=1,
                                              3,
                                              parent=self.cf_tid_1)
    ###############################
    ## Non-Cash Items & Children ##
    ###############################
        self.cf_tid_3 = projected_line_item('Non-Cash Items',
                                             method=1,
                                             5,
                                             parent=self.cf_tid_13)
        self.cf_tid_4 = projected_line_item('     Stock-Based Compensation',
                                             method=2,
                                             6,
                                             parent=self.cf_tid_3)
        self.cf_tid_5 = projected_line_item('     Deferred Income Taxes',
                                             method=1,
                                             7,
                                             parent=self.cf_tid_3)
        self.cf_tid_6 = projected_line_item('     Other Non-Cash Adjustments',
                                             method=1,
                                             8,
                                             parent=self.cf_tid_3)
    ##########################################
    ## Change in Working Capital & Children ##
    ##########################################
        self.cf_tid_7 = projected_line_item('Change in Working Capital',
                                             method=1,
                                             9,
                                             parent=self.cf_tid_13)
        self.cf_tid_8 = projected_line_item('     (Increase) Decrease in Accounts Receivable',
                                             method=4,
                                             10,
                                             parent=self.cf_tid_7)
        self.cf_tid_8.set_projection_children()
        self.cf_tid_9 = projected_line_item('     (Increase) Decrease in Inventories',
                                             method=4,
                                             11,
                                             parent=self.cf_tid_7)
        self.cf_tid_9.set_projection_children()
        self.cf_tid_10 = projected_line_item('     Increase (Decrease) in Accounts Payable',
                                             method=4,
                                             12,
                                             parent=self.cf_tid_7)
        self.cf_tid_10.set_projection_children()
        self.cf_tid_11 = projected_line_item('     Increase (Decrease) in Other',
                                             method=2,
                                             13,
                                             parent=self.cf_tid_7)
    #########################################
    ## Cash From Operating Children, Other ##
    #########################################
        self.cf_tid_12 = projected_line_item('Net Cash From Discontinued Operations (operating)',
                                             method=1,
                                             14,
                                             parent=self.cf_tid_13)
        self.cf_tid_2 = projected_line_item('Depreciation & Amortization',
                                             method=4,
                                             4,
                                             parent=self.cf_tid_13)
        self.cf_tid_2.set_projection_children()
    ####################################
    ## Cash From Investing Activities ##
    ####################################
        self.cf_tid_31 = projected_line_item('Cash from Investing Activities',
                                              34,
                                              parent=self.cf_tid_56)
    ###################################################
    ## Fixed Asset/Intangibles Activity and Children ##
    ###################################################
        self.cf_tid_14 = projected_line_item('Change in Fixed Assets & Intangibles',
                                              method=1,
                                              16,
                                              parent=self.cf_tid_31)
    #######################################
    ## Continued, Disposition Acitivites ##
    #######################################
        self.cf_tid_15 = projected_line_item('     Disposition of Fixed Assets & Intangibles',
                                              method=1,
                                              17,
                                              parent=self.cf_tid_14)
        self.cf_tid_16 = projected_line_item('       Disposition of Fixed Assets',
                                              method=1,
                                              18,
                                              parent=self.cf_tid_15)
        self.cf_tid_17 = projected_line_item('       Disposition of Intangible Assets',
                                              method=1,
                                              19,
                                              parent=self.cf_tid_15)
    #######################################
    ## Continued, Acquisition Acitivites ##
    #######################################
        self.cf_tid_18 = projected_line_item('     Acquisition of Fixed Assets & Intangibles',
                                              method=1,
                                              20,
                                              parent=self.cf_tid_14)
        self.cf_tid_19 = projected_line_item('       Purchase of Fixed Assets',
                                              method=2,
                                              21,
                                              parent=self.cf_tid_18)
        self.cf_tid_20 = projected_line_item('       Acquisition of Intangible Assets',
                                              method=2,
                                              22,
                                              parent=self.cf_tid_18)
        self.cf_tid_21 = projected_line_item('     Other Change in Fixed Assets & Intangibles',
                                              method=1,
                                              23,
                                              parent=self.cf_tid_14)
    #########################################
    ## LT Investment Activity and Children ##
    #########################################
        self.cf_tid_22 = projected_line_item('Net Change in Long Term Investment',
                                              24,
                                              parent=self.cf_tid_31)
        self.cf_tid_23 = projected_line_item(     'Decrease in Long Term Investment',
                                              method=2,
                                              25,
                                              parent=self.cf_tid_22)
        self.cf_tid_24 = projected_line_item('     Increase in Long Term Investment',
                                              method=2,
                                              26,
                                              parent=self.cf_tid_22)
    #################################
    ## M & A Activity and Children ##
    #################################
        self.cf_tid_25 = projected_line_item('Net Cash From Acquisitions & Divestitures',
                                              method=1,
                                              27,
                                              parent=self.cf_tid_31)
        self.cf_tid_26 = projected_line_item('     Net Cash from Divestitures',
                                              method=1,
                                              28,
                                              parent=self.cf_tid_25)
        self.cf_tid_27 = projected_line_item('     Cash for Acqusition of Subsidiaries',
                                              method=1,
                                              29,
                                              parent=self.cf_tid_25)
        self.cf_tid_28 = projected_line_item('     Cash for Joint Ventures',
                                              method=1,
                                              30,
                                              parent=self.cf_tid_25)
        self.cf_tid_50 = projected_line_item('     Net Cash from Other Acquisitions',
                                              method=1,
                                              31,
                                              parent=self.cf_tid_25)
    #########################################
    ## Cash From Investing Children, Other ##
    #########################################
        self.cf_tid_29 = projected_line_item('Other Investing Activities',
                                              method=1,
                                              32,
                                              parent=self.cf_tid_31)
        self.cf_tid_30 = projected_line_item('Net Cash From Discontinued Operations (investing)',
                                              method=1,
                                              33,
                                              parent=self.cf_tid_31)
    ####################################
    ## Cash From Financing Activities ##
    ####################################
        self.cf_tid_43 = projected_line_item('Cash from Financing Activities',
                                              46,
                                              parent=self.cf_tid_56)
    ##########################################
    ## Debt Financing Activity and Children ##
    ##########################################
        self.cf_tid_33 = projected_line_item('Cash From (Repayment of) Debt',
                                              method=3,
                                              36,
                                              parent=self.cf_tid_43)
        self.cf_tid_33.set_default_ratio()
        self.cf_tid_34 = projected_line_item('Cash From (Repayment of) Short Term Debt, net',
                                              method=3,
                                              37,
                                              parent=self.cf_tid_33)
        self.cf_tid_34.set_default_ratio()
    ###################################
    ## Continued, LT Debt Acitivites ##
    ###################################
        self.cf_tid_35 = projected_line_item('     Cash From (Repayment of) Long Term Debt, net',
                                              method=3,
                                              38,
                                              parent=self.cf_tid_33)
        self.cf_tid_35.set_default_ratio()
        self.cf_tid_36 = projected_line_item('       Repayments of Long Term Debt',
                                              method=3,
                                              39,
                                              parent=self.cf_tid_35)
        self.cf_tid_36.set_default_ratio()
        self.cf_tid_37 = projected_line_item('       Cash From Long Term Debt',
                                              method=1,
                                              40,
                                              parent=self.cf_tid_35)
    ############################################
    ## Equity Financing Activity and Children ##
    ############################################
        self.cf_tid_38 = projected_line_item('Cash From (Repurchase of) Equity',
                                              method=2,
                                              41,
                                              parent=self.cf_tid_43)
        self.cf_tid_39 = projected_line_item('     Increase in Capital Stock',
                                              method=2,
                                              42,
                                              parent=self.cf_tid_38)
        self.cf_tid_40 = projected_line_item('     Decrease in Capital Stock',
                                              method=2,
                                              43,
                                              parent=self.cf_tid_38)
    #########################################
    ## Cash From Financing Children, Other ##
    #########################################
        self.cf_tid_32 = projected_line_item('Dividends Paid',
                                              method=2,
                                              35,
                                              parent=self.cf_tid_43)
        self.cf_tid_41 = projected_line_item('Other Financing Activities',
                                              method=1,
                                              44,
                                              parent=self.cf_tid_43)
        self.cf_tid_42 = projected_line_item('Net Cash From Discontinued Operations (financing)',
                                              method=1,
                                              45,
                                              parent=self.cf_tid_43)


class proj_balance_sheet(financial_statement):
    ''' __init__ will create the necessary accounts for a balance sheet.
    ----------------------------------------------------------------------------
    No data must be added initially, use function add_data for this '''
    def __init__(self, self_at_T_1):
        self.at_T_1 = self_at_T_1
    ################
    ## All Assets ##
    ################
        self.bs_tid_41 = projected_line_item('Total Assets', 40)
    ####################
    ## Current Assets ##
    ####################
        self.bs_tid_21 = projected_line_item('Total Current Assets',
                                            20,
                                            parent=self.bs_tid_41)
        self.bs_tid_7 = projected_line_item('Unbilled Revenues',
                                            method=1,
                                            6,
                                            parent=self.bs_tid_21)
    ##################################
    ## Cash, Equivalents & Children ##
    ##################################
        self.bs_tid_1 = projected_line_item('Cash, Cash Equivalents & Short Term Investments',
                                            method=4,
                                            0,
                                            parent=self.bs_tid_21)
        self.bs_tid_1.set_projection_children()
        self.bs_tid_2 = projected_line_item('     Cash & Cash Equivalents',
                                            method=4,
                                            1,
                                            parent=self.bs_tid_1)
        self.bs_tid_2.set_projection_children()
        self.bs_tid_3 = projected_line_item('     Short Term Investments',
                                            method=4,
                                            2,
                                            parent=self.bs_tid_1)
        self.bs_tid_3.set_projection_children()
    ############################
    ## Receivables & Children ##
    ############################
        self.bs_tid_4 = projected_line_item('Accounts & Notes Receivable',
                                            method=3,
                                            3,
                                            parent=self.bs_tid_21)
        self.bs_tid_4.set_default_ratio()
        self.bs_tid_5 = projected_line_item('     Accounts Receivable, Net',
                                            method=3,
                                            4,
                                            parent=self.bs_tid_4)
        self.bs_tid_5.set_default_ratio()
        self.bs_tid_6 = projected_line_item('     Notes Receivable, Net',
                                            method=3,
                                            5,
                                            parent=self.bs_tid_4)
        self.bs_tid_6.set_default_ratio()
    ##########################
    ## Inventory & Children ##
    ##########################
        self.bs_tid_8 = projected_line_item('Inventories',
                                            method=3,
                                            7,
                                            parent=self.bs_tid_21)
        self.bs_tid_8.set_default_ratio()
        self.bs_tid_9 = projected_line_item('     Raw Materials',
                                            method=3,
                                            8,
                                            parent=self.bs_tid_8)
        self.bs_tid_9.set_default_ratio()
        self.bs_tid_10 = projected_line_item('     Work In Process',
                                            method=3,
                                            9,
                                            parent=self.bs_tid_8)
        self.bs_tid_10.set_default_ratio()
        self.bs_tid_11 = projected_line_item('     Finished Goods',
                                            method=3,
                                            10,
                                            parent=self.bs_tid_8)
        self.bs_tid_11.set_default_ratio()
        self.bs_tid_12 = projected_line_item('     Other Inventory',
                                            method=3,
                                            11,
                                            parent=self.bs_tid_8)
        self.bs_tid_12.set_default_ratio()
    ######################
    ## Other & Children ##
    ######################
        self.bs_tid_13 = projected_line_item('Other Short Term Assets',
                                            method=1,
                                            12,
                                            parent=self.bs_tid_21)
        self.bs_tid_14 = projected_line_item('     Prepaid Expenses',
                                            method=1,
                                            13,
                                            parent=self.bs_tid_13)
        self.bs_tid_15 = projected_line_item('     Derivative & Hedging Assets',
                                            method=1,
                                            14,
                                            parent=self.bs_tid_13)
        self.bs_tid_16 = projected_line_item('     Assets Held-for-Sale',
                                            method=1,
                                            15,
                                            parent=self.bs_tid_13)
        self.bs_tid_17 = projected_line_item('     Deferred Tax Assets',
                                            method=1,
                                            16,
                                            parent=self.bs_tid_13)
        self.bs_tid_18 = projected_line_item('     Income Taxes Receivable',
                                            method=1,
                                            17,
                                            parent=self.bs_tid_13)
        self.bs_tid_19 = projected_line_item('     Discontinued Operations',
                                            method=1,
                                            18,
                                            parent=self.bs_tid_13)
        self.bs_tid_20 = projected_line_item('     Miscellaneous Short Term Assets',
                                            method=1,
                                            19,
                                            parent=self.bs_tid_13)
    ########################
    ## Non-Current Assets ##
    ########################
        self.bs_tid_40 = projected_line_item('Total Noncurrent Assets',
                                            39,
                                            parent=self.bs_tid_41)
    ############
    ## PP & E ##
    ############
        self.bs_tid_22 = projected_line_item('Property, Plant & Equipment, Net',
                                            method=2,
                                            21,
                                            parent=self.bs_tid_40)
        self.bs_tid_23 = projected_line_item('     Property, Plant & Equipment',
                                            method=2,
                                            22,
                                            parent=self.bs_tid_22)
        self.bs_tid_24 = projected_line_item('     Accumulated Depreciation',
                                            method=3,
                                            23,
                                            parent=self.bs_tid_22)
        self.bs_tid_24.set_default_ratio()
    ###############################
    ## LT Investments & Children ##
    ###############################
        self.bs_tid_25 = projected_line_item('Long Term Investments & Receivables',
                                            method=2,
                                            24,
                                            parent=self.bs_tid_40)
        self.bs_tid_26 = projected_line_item('     Long Term Investments',
                                            method=2,
                                            25,
                                            parent=self.bs_tid_25)
        self.bs_tid_27 = projected_line_item('     Long Term Marketable Securities',
                                            method=2,
                                            26,
                                            parent=self.bs_tid_25)
        self.bs_tid_28 = projected_line_item('     Long Term Receivables',
                                            method=2,
                                            27,
                                            parent=self.bs_tid_25)
    ######################
    ## Other & Children ##
    ######################
        self.bs_tid_29 = projected_line_item('Other Long Term Assets',
                                            method=2,
                                            28,
                                            parent=self.bs_tid_40)
        self.bs_tid_30 = projected_line_item('     Intangible Assets',
                                            method=2,
                                            29,
                                            parent=self.bs_tid_29)
        self.bs_tid_31 = projected_line_item('     Goodwill',
                                            method=2,
                                            30,
                                            parent=self.bs_tid_29)
        self.bs_tid_32 = projected_line_item('     Other Intangible Assets',
                                            method=2,
                                            31,
                                            parent=self.bs_tid_29)
        self.bs_tid_33 = projected_line_item('     Prepaid Expense',
                                            method=1,
                                            32,
                                            parent=self.bs_tid_29)
        self.bs_tid_34 = projected_line_item('     Deferred Tax Assets',
                                            method=1,
                                            33,
                                            parent=self.bs_tid_29)
        self.bs_tid_35 = projected_line_item('     Derivative & Hedging Assets',
                                            method=1,
                                            34,
                                            parent=self.bs_tid_29)
        self.bs_tid_36 = projected_line_item('     Prepaid Pension Costs',
                                            method=1,
                                            35,
                                            parent=self.bs_tid_29)
        self.bs_tid_37 = projected_line_item('     Discontinued Operations',
                                            method=1,
                                            36,
                                            parent=self.bs_tid_29)
        self.bs_tid_38 = projected_line_item('     Investments in Affiliates',
                                            method=1,
                                            37,
                                            parent=self.bs_tid_29)
        self.bs_tid_39 = projected_line_item('     Miscellaneous Long Term Assets',
                                            method=2,
                                            38,
                                            parent=self.bs_tid_29)
    ################################
    ## All Liabilities and Equity ##
    ################################
        self.bs_tid_85 = projected_line_item('Total Liabilities & Equity', 84)
    ##################
    ## Liabilities  ##
    ##################
        self.bs_tid_73 = projected_line_item('Total Liabilities',
                                            72,
                                            parent=self.bs_tid_85)
    #########################
    ## Current Liabilities ##
    #########################
        self.bs_tid_57 = projected_line_item('Total Current Liabilities',
                                            56,
                                            parent=self.bs_tid_73)
    #########################
    ## Payables & Children ##
    #########################
        self.bs_tid_42 = projected_line_item('Payables & Accruals',
                                            method=3,
                                            41,
                                            parent=self.bs_tid_57)
        self.bs_tid_42.set_default_ratio()
        self.bs_tid_43 = projected_line_item('     Accounts Payable',
                                            method=3,
                                            42,
                                            parent=self.bs_tid_42)
        self.bs_tid_43.set_default_ratio()
        self.bs_tid_44 = projected_line_item('     Accrued Taxes',
                                            method=3,
                                            43,
                                            parent=self.bs_tid_42)
        self.bs_tid_44.set_default_ratio()
        self.bs_tid_45 = projected_line_item('     Interest & Dividends Payable',
                                            method=3,
                                            44,
                                            parent=self.bs_tid_42)
        self.bs_tid_45.set_default_ratio()
        self.bs_tid_46 = projected_line_item('     Other Payables & Accruals',
                                            method=3,
                                            45,
                                            parent=self.bs_tid_42)
        self.bs_tid_46.set_default_ratio()
    #####################
    ## Debt & Children ##
    #####################
        self.bs_tid_47 = projected_line_item('Short Term Debt',
                                            method=4,
                                            46,
                                            parent=self.bs_tid_57)
        self.bs_tid_47.set_projection_children()
        self.bs_tid_48 = projected_line_item('     Short Term Borrowings',
                                            method=4,
                                            47,
                                            parent=self.bs_tid_47)
        self.bs_tid_48.set_projection_children()
        self.bs_tid_49 = projected_line_item('     Short Term Capital Leases',
                                            method=1,
                                            48,
                                            parent=self.bs_tid_47)
        self.bs_tid_50 = projected_line_item('     Current Portion of Long Term Debt',
                                            method=3,
                                            49,
                                            parent=self.bs_tid_47)
        self.bs_tid_50.set_default_ratio()
    ######################
    ## Other & Children ##
    ######################
        self.bs_tid_51 = projected_line_item('Other Short Term Liabilities',
                                            method=2,
                                            50,
                                            parent=self.bs_tid_57)
        self.bs_tid_52 = projected_line_item('     Deferred Revenue',
                                            method=2,
                                            51,
                                            parent=self.bs_tid_51)
        self.bs_tid_53 = projected_line_item('     Derivatives & Hedging',
                                            method=1,
                                            52,
                                            parent=self.bs_tid_51)
        self.bs_tid_54 = projected_line_item('     Deferred Tax Liabilities',
                                            method=1,
                                            53,
                                            parent=self.bs_tid_51)
        self.bs_tid_55 = projected_line_item('     Discontinued Operations',
                                            method=1,
                                            54,
                                            parent=self.bs_tid_51)
        self.bs_tid_56 = projected_line_item('     Miscellaneous Short Term Liabilities',
                                            method=1,
                                            55,
                                            parent=self.bs_tid_51)
    #############################
    ## Non-Current Liabilities ##
    #############################
        self.bs_tid_72 = projected_line_item('Total Noncurrent Liabilities',
                                            71,
                                            parent=self.bs_tid_73)
    #####################
    ## Debt & Children ##
    #####################
        self.bs_tid_58 = projected_line_item('Long Term Debt',
                                            method=4,
                                            57,
                                            parent=self.bs_tid_72)
        self.bs_tid_58.set_projection_children()
        self.bs_tid_59 = projected_line_item('     Long Term Borrowings',
                                            method=3,
                                            58,
                                            parent=self.bs_tid_58)
        self.bs_tid_59.set_default_ratio()
        self.bs_tid_60 = projected_line_item('     Long Term Capital Leases',
                                            method=3,
                                            59,
                                            parent=self.bs_tid_58)
        self.bs_tid_60.set_default_ratio()
    ######################
    ## Other & Children ##
    ######################
        self.bs_tid_61 = projected_line_item('Other Long Term Liabilities',
                                            method=2,
                                            60,
                                            parent=self.bs_tid_72)
        self.bs_tid_62 = projected_line_item('     Accrued Liabilities',
                                            method=1,
                                            61,
                                            parent=self.bs_tid_61)
        self.bs_tid_66 = projected_line_item('     Deferred Compensation',
                                            method=2,
                                            65,
                                            parent=self.bs_tid_61)
        self.bs_tid_67 = projected_line_item('     Deferred Revenue',
                                            method=2,
                                            66,
                                            parent=self.bs_tid_61)
        self.bs_tid_68 = projected_line_item('     Deferred Tax Liabilities',
                                            method=1,
                                            67,
                                            parent=self.bs_tid_61)
        self.bs_tid_69 = projected_line_item('     Derivatives & Hedging',
                                            method=1,
                                            68,
                                            parent=self.bs_tid_61)
        self.bs_tid_70 = projected_line_item('     Discontinued Operations',
                                            method=1,
                                            69,
                                            parent=self.bs_tid_61)
        self.bs_tid_71 = projected_line_item('     Miscellaneous Long Term Liabilities',
                                            method=2,
                                            70,
                                            parent=self.bs_tid_61)
    #########################
    ## Continued, Pensions ##
    #########################
        self.bs_tid_63 = projected_line_item('     Pension Liabilities',
                                            method=2,
                                            62,
                                            parent=self.bs_tid_61)
        self.bs_tid_64 = projected_line_item('       Pensions',
                                            method=2,
                                            63,
                                            parent=self.bs_tid_63)
        self.bs_tid_65 = projected_line_item('       Other Post-Retirement Benefits',
                                            method=2,
                                            64,
                                            parent=self.bs_tid_63)
    #############
    ## Equity  ##
    #############
        self.bs_tid_84 = projected_line_item('Total Equity',
                                            83,
                                            parent=self.bs_tid_85)
        self.bs_tid_83 = projected_line_item('Minority Interest',
                                            method=1,
                                            82,
                                            parent=self.bs_tid_84)
    #####################################
    ## Equity Before Minority Interest ##
    #####################################
        self.bs_tid_82 = projected_line_item('Equity Before Minority Interest',
                                            81,
                                            parent=self.bs_tid_84)
        self.bs_tid_74 = projected_line_item('     Preferred Equity',
                                            method=4,
                                            73,
                                            parent=self.bs_tid_82)
        self.bs_tid_74.set_projection_children()
        self.bs_tid_79 = projected_line_item('     Treasury Stock',
                                            method=4,
                                            78,
                                            parent=self.bs_tid_82)
        self.bs_tid_79.set_projection_children()
        self.bs_tid_80 = projected_line_item('     Retained Earnings',
                                            method=4,
                                            79,
                                            parent=self.bs_tid_82)
        self.bs_tid_80.set_projection_children()
        self.bs_tid_81 = projected_line_item('     Other Equity',
                                            method=1,
                                            80,
                                            parent=self.bs_tid_82)
    ##############################
    ## Continued, Issued Equity ##
    ##############################
        self.bs_tid_75 = projected_line_item('Share Capital & Additional Paid-In Capital',
                                            method=2,
                                            74,
                                            parent=self.bs_tid_82)
        self.bs_tid_76 = projected_line_item('     Common Stock',
                                            method=2,
                                            75,
                                            parent=self.bs_tid_75)
        self.bs_tid_77 = projected_line_item('     Additional Paid in Capital',
                                            method=2,
                                            76,
                                            parent=self.bs_tid_75)
        self.bs_tid_78 = projected_line_item('     Other Share Capital',
                                            method=1,
                                            77,
                                            parent=self.bs_tid_75)
