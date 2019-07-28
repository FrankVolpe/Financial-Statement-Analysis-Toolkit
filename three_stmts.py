from base_classes import *

class income_statement(financial_statement):
    ''' __init__ will create the necessary accounts for an income statement.
    --------------------------------------------------------------------------
    No data must be added initially, use function add_data for this '''
    def __init__(self, data=None):
    ####################################
    ## Final Line Of Income Statement ##
    ####################################
        self.is_tid_58 = line_item('Net Income Available to Common Shareholders', 57)
    ####################################
    ## Net Income & Final Adjustments ##
    ####################################
        self.is_tid_55 = line_item('Net Income',
                                    54,
                                    parent=self.is_tid_58)
        self.is_tid_56 = line_item('Preferred Dividends',
                                    55,
                                    parent=self.is_tid_58)
        self.is_tid_57 = line_item('Other Adjustments',
                                    56,
                                    parent=self.is_tid_58)
    ####################################
    ## Factoring In Minority Interest ##
    ####################################
        self.is_tid_53 = line_item('Income (Loss) Including Minority Interest',
                                    52,
                                    parent=self.is_tid_55)
        self.is_tid_54 = line_item('Minority Interest',
                                    53,
                                    parent=self.is_tid_55)
    #########################
    ## Extraordinary Items ##
    #########################
        self.is_tid_50 = line_item('Net Extraordinary Gains (Losses)',
                                    49,
                                    parent=self.is_tid_53)
        self.is_tid_51 = line_item('     Discontinued Operations',
                                    50,
                                    parent=self.is_tid_50)
        self.is_tid_52 = line_item('     XO & Accounting Charges & Other',
                                    51,
                                    parent=self.is_tid_50)
    ########################
    ## Income After Taxes ##
    ########################
        self.is_tid_49 = line_item('Income (Loss) from Continuing Operations',
                                    48,
                                    parent=self.is_tid_53)
        self.is_tid_48 = line_item('Income (Loss) from Affiliates, net of taxes',
                                    47,
                                    parent=self.is_tid_49)
    ####################
    ## Pre-Tax Income ##
    ####################
        self.is_tid_43 = line_item('Pretax Income (Loss)',
                                    42,
                                    parent=self.is_tid_49)
        self.is_tid_28 = line_item('Pretax Income (Loss), Adjusted',
                                    27,
                                    parent=self.is_tid_43)
    #################
    ## Tax Expense ##
    #################
        self.is_tid_44 = line_item('Income Tax (Expense) Benefit, net',
                                    43,
                                    parent=self.is_tid_49)
        self.is_tid_45 = line_item('     Current Income Tax',
                                    44,
                                    parent=self.is_tid_44)
        self.is_tid_46 = line_item('     Deferred Income Tax',
                                    45,
                                    parent=self.is_tid_44)
        self.is_tid_47 = line_item('     Tax Allowance/Credit',
                                    46,
                                    parent=self.is_tid_44)
    ####################################
    ## Abnormal Activities & Children ##
    ####################################
        self.is_tid_29 = line_item('Abnormal Gains (Losses)',
                                    28,
                                    parent=self.is_tid_43)
        self.is_tid_30 = line_item('     Acquired In-Process R&D',
                                    29,
                                    parent=self.is_tid_29)
        self.is_tid_31 = line_item('     Merger / Acquisition Expense',
                                    30,
                                    parent=self.is_tid_29)
        self.is_tid_32 = line_item('     Abnormal Derivatives',
                                    31,
                                    parent=self.is_tid_29)
        self.is_tid_33 = line_item('     Disposal of Assets',
                                    32,
                                    parent=self.is_tid_29)
        self.is_tid_34 = line_item('     Early extinguishment of Debt',
                                    33,
                                    parent=self.is_tid_29)
        self.is_tid_35 = line_item('     Asset Write-Down',
                                    34,
                                    parent=self.is_tid_29)
        self.is_tid_36 = line_item('     Impairment of Goodwill & Intangibles',
                                    35,
                                    parent=self.is_tid_29)
        self.is_tid_37 = line_item('     Sale of Business',
                                    36,
                                    parent=self.is_tid_29)
        self.is_tid_38 = line_item('     Legal Settlement',
                                    37,
                                    parent=self.is_tid_29)
        self.is_tid_39 = line_item('     Restructuring Charges',
                                    38,
                                    parent=self.is_tid_29)
        self.is_tid_40 = line_item('     Sale of and Unrealized Investments',
                                    39,
                                    parent=self.is_tid_29)
        self.is_tid_41 = line_item('     Insurance Settlement',
                                    40,
                                    parent=self.is_tid_29)
        self.is_tid_42 = line_item('     Other Abnormal Items',
                                    41,
                                    parent=self.is_tid_29)
    ##############################
    ## Non-Operating Activities ##
    ##############################
        self.is_tid_20 = line_item('Non-Operating Income (Loss)',
                                    19,
                                    parent=self.is_tid_28)
        self.is_tid_21 = line_item('     Interest Expense, net',
                                    20,
                                    parent=self.is_tid_20)
        self.is_tid_22 = line_item('       Interest Expense',
                                    21,
                                    parent=self.is_tid_21)
        self.is_tid_23 = line_item('       Interest Income',
                                    22,
                                    parent=self.is_tid_21)
        self.is_tid_24 = line_item('     Other Investment Income (Loss)',
                                    23,
                                    parent=self.is_tid_20)
        self.is_tid_25 = line_item('     Foreign Exchange Gain (Loss)',
                                    24,
                                    parent=self.is_tid_20)
        self.is_tid_26 = line_item('     Income (Loss) from Affiliates',
                                    25,
                                    parent=self.is_tid_20)
        self.is_tid_27 = line_item('     Other Non-Operating Income (Loss)',
                                    26,
                                    parent=self.is_tid_20)
    ######################
    ## Operating Income ##
    ######################
        self.is_tid_19 = line_item('Operating Income (Loss)',
                                    18,
                                    parent=self.is_tid_28)
        self.is_tid_10 = line_item('     Other Operating Income',
                                        9,
                                        parent=self.is_tid_19)
    ###################################
    ## Operating Expenses & Children ##
    ###################################
        self.is_tid_11 = line_item('Operating Expenses',
                                    10,
                                    parent=self.is_tid_19)
        self.is_tid_12 = line_item('     Selling, General & Administrative',
                                    11,
                                    parent=self.is_tid_11)
        self.is_tid_13 = line_item('       Selling & Marketing',
                                    12,
                                    parent=self.is_tid_12)
        self.is_tid_14 = line_item('       General & Administrative',
                                    13,
                                    parent=self.is_tid_12)
        self.is_tid_15 = line_item('     Research & Development',
                                    14,
                                    parent=self.is_tid_11)
        self.is_tid_16 = line_item('     Depreciation & Amortization',
                                    15,
                                    parent=self.is_tid_11)
        self.is_tid_17 = line_item('     Provision For Doubtful Accounts',
                                    16,
                                    parent=self.is_tid_11)
        self.is_tid_18 = line_item('     Other Operating Expense',
                                    17,
                                    parent=self.is_tid_11)
    ##################
    ## Gross Profit ##
    ##################
        self.is_tid_4 = line_item('Gross Profit',
                                    8,
                                    parent=self.is_tid_19)
    ##############################
    ## Cost of Sales & Children ##
    ##############################
        self.is_tid_2 = line_item('Cost of revenue',
                                    4,
                                    parent=self.is_tid_4)
        self.is_tid_7 = line_item('     Cost of Goods & Services',
                                    5,
                                    parent=self.is_tid_2)
        self.is_tid_8 = line_item('     Cost of Financing Revenue',
                                    6,
                                    parent=self.is_tid_2)
        self.is_tid_9 = line_item('     Cost of Other Revenue',
                                    7,
                                    parent=self.is_tid_2)
    ########################
    ## Revenue & Children ##
    ########################
        self.is_tid_1 = line_item('Revenue',
                                    0,
                                    parent=self.is_tid_4)
        self.is_tid_3 = line_item('     Sales & Services Revenue',
                                    1,
                                    parent=self.is_tid_1)
        self.is_tid_5 = line_item('     Financing Revenue',
                                    2,
                                    parent=self.is_tid_1)
        self.is_tid_6 = line_item('     Other Revenue',
                                    3,
                                    parent=self.is_tid_1)
        if data:
            self.add_data(data)


class cash_flow_statement(financial_statement):
    ''' __init__ will create the necessary accounts for a cash flow statement.
    --------------------------------------------------------------------------
    No data must be added initially, use function add_data for this '''
    def __init__(self, data=None):
    #######################################
    ## Final Line Of Cash Flow Statement ##
    #######################################
        self.cf_tid_46 = line_item('Net Changes in Cash', 51)
    ######################################
    ## Factoring In FX Gains and Losses ##
    ######################################
        self.cf_tid_44 = line_item('     Effect of Foreign Exchange Rates',
                              50,
                              parent=self.cf_tid_46)
        self.cf_tid_55 = line_item('Net Cash Before FX',
                              49,
                              parent=self.cf_tid_46)
    ##########################################
    ## Factoring in Discontinued Operations ##
    ##########################################
        self.cf_tid_56 = line_item('Net Cash Before Disc. Operations and FX',
                              47,
                              parent=self.cf_tid_55)
        self.cf_tid_45 = line_item('     Change in Cash from Disc. Operations and Other',
                              48,
                              parent=self.cf_tid_55)
    ####################################
    ## Cash From Operating Activities ##
    ####################################
        self.cf_tid_13 = line_item('Cash from Operating Activities',
                              15,
                              parent=self.cf_tid_56)
    ###########################
    ## Net Income & Children ##
    ###########################
        self.cf_tid_1 = line_item('Net Income/Starting Line',
                             0,
                             parent=self.cf_tid_13)
        self.cf_tid_47 = line_item('     Net Income',
                              1,
                              parent=self.cf_tid_1)
        self.cf_tid_48 = line_item('     Net Income From Discontinued Operations',
                              2,
                              parent=self.cf_tid_1)
        self.cf_tid_49 = line_item('     Other Adjustments',
                              3,
                              parent=self.cf_tid_1)
    ###############################
    ## Non-Cash Items & Children ##
    ###############################
        self.cf_tid_3 = line_item('Non-Cash Items',
                             5,
                             parent=self.cf_tid_13)
        self.cf_tid_4 = line_item('     Stock-Based Compensation',
                              6,
                              parent=self.cf_tid_3)
        self.cf_tid_5 = line_item('     Deferred Income Taxes',
                             7,
                             parent=self.cf_tid_3)
        self.cf_tid_6 = line_item('     Other Non-Cash Adjustments',
                             8,
                             parent=self.cf_tid_3)
    ##########################################
    ## Change in Working Capital & Children ##
    ##########################################
        self.cf_tid_7 = line_item('Change in Working Capital',
                             9,
                             parent=self.cf_tid_13)
        self.cf_tid_8 = line_item('     (Increase) Decrease in Accounts Receivable',
                             10,
                             parent=self.cf_tid_7)
        self.cf_tid_9 = line_item('     (Increase) Decrease in Inventories',
                             11,
                             parent=self.cf_tid_7)
        self.cf_tid_10 = line_item('     Increase (Decrease) in Accounts Payable',
                              12,
                              parent=self.cf_tid_7)
        self.cf_tid_11 = line_item('     Increase (Decrease) in Other',
                              13,
                              parent=self.cf_tid_7)
    #########################################
    ## Cash From Operating Children, Other ##
    #########################################
        self.cf_tid_12 = line_item('Net Cash From Discontinued Operations (operating)',
                              14,
                              parent=self.cf_tid_13)
        self.cf_tid_2 = line_item('Depreciation & Amortization',
                             4,
                             parent=self.cf_tid_13)
    ####################################
    ## Cash From Investing Activities ##
    ####################################
        self.cf_tid_31 = line_item('Cash from Investing Activities',
                              34,
                              parent=self.cf_tid_56)
    ###################################################
    ## Fixed Asset/Intangibles Activity and Children ##
    ###################################################
        self.cf_tid_14 = line_item('Change in Fixed Assets & Intangibles',
                              16,
                              parent=self.cf_tid_31)
    #######################################
    ## Continued, Disposition Acitivites ##
    #######################################
        self.cf_tid_15 = line_item('     Disposition of Fixed Assets & Intangibles',
                              17,
                              parent=self.cf_tid_14)
        self.cf_tid_16 = line_item('       Disposition of Fixed Assets',
                              18,
                              parent=self.cf_tid_15)
        self.cf_tid_17 = line_item('       Disposition of Intangible Assets',
                              19,
                              parent=self.cf_tid_15)
    #######################################
    ## Continued, Acquisition Acitivites ##
    #######################################
        self.cf_tid_18 = line_item('     Acquisition of Fixed Assets & Intangibles',
                              20,
                              parent=self.cf_tid_14)
        self.cf_tid_19 = line_item('       Purchase of Fixed Assets',
                              21,
                              parent=self.cf_tid_18)
        self.cf_tid_20 = line_item('       Acquisition of Intangible Assets',
                              22,
                              parent=self.cf_tid_18)
        self.cf_tid_21 = line_item('     Other Change in Fixed Assets & Intangibles',
                              23,
                              parent=self.cf_tid_14)
    #########################################
    ## LT Investment Activity and Children ##
    #########################################
        self.cf_tid_22 = line_item('Net Change in Long Term Investment',
                              24,
                              parent=self.cf_tid_31)
        self.cf_tid_23 = line_item(     'Decrease in Long Term Investment',
                              25,
                              parent=self.cf_tid_22)
        self.cf_tid_24 = line_item('     Increase in Long Term Investment',
                              26,
                              parent=self.cf_tid_22)
    #################################
    ## M & A Activity and Children ##
    #################################
        self.cf_tid_25 = line_item('Net Cash From Acquisitions & Divestitures',
                              27,
                              parent=self.cf_tid_31)
        self.cf_tid_26 = line_item('     Net Cash from Divestitures',
                              28,
                              parent=self.cf_tid_25)
        self.cf_tid_27 = line_item('     Cash for Acqusition of Subsidiaries',
                              29,
                              parent=self.cf_tid_25)
        self.cf_tid_28 = line_item('     Cash for Joint Ventures',
                              30,
                              parent=self.cf_tid_25)
        self.cf_tid_50 = line_item('     Net Cash from Other Acquisitions',
                              31,
                              parent=self.cf_tid_25)
    #########################################
    ## Cash From Investing Children, Other ##
    #########################################
        self.cf_tid_29 = line_item('Other Investing Activities',
                              32,
                              parent=self.cf_tid_31)
        self.cf_tid_30 = line_item('Net Cash From Discontinued Operations (investing)',
                              33,
                              parent=self.cf_tid_31)
    ####################################
    ## Cash From Financing Activities ##
    ####################################
        self.cf_tid_43 = line_item('Cash from Financing Activities',
                              46,
                              parent=self.cf_tid_56)
    ##########################################
    ## Debt Financing Activity and Children ##
    ##########################################
        self.cf_tid_33 = line_item('Cash From (Repayment of) Debt',
                              36,
                              parent=self.cf_tid_43)
        self.cf_tid_34 = line_item('Cash From (Repayment of) Short Term Debt, net',
                              37,
                              parent=self.cf_tid_33)
    ###################################
    ## Continued, LT Debt Acitivites ##
    ###################################
        self.cf_tid_35 = line_item('     Cash From (Repayment of) Long Term Debt, net',
                              38,
                              parent=self.cf_tid_33)
        self.cf_tid_36 = line_item('       Repayments of Long Term Debt',
                              39,
                              parent=self.cf_tid_35)
        self.cf_tid_37 = line_item('       Cash From Long Term Debt',
                              40,
                              parent=self.cf_tid_35)
    ############################################
    ## Equity Financing Activity and Children ##
    ############################################
        self.cf_tid_38 = line_item('Cash From (Repurchase of) Equity',
                              41,
                              parent=self.cf_tid_43)
        self.cf_tid_39 = line_item('     Increase in Capital Stock',
                              42,
                              parent=self.cf_tid_38)
        self.cf_tid_40 = line_item('     Decrease in Capital Stock',
                              43,
                              parent=self.cf_tid_38)
    #########################################
    ## Cash From Financing Children, Other ##
    #########################################
        self.cf_tid_32 = line_item('Dividends Paid',
                              35,
                              parent=self.cf_tid_43)
        self.cf_tid_41 = line_item('Other Financing Activities',
                              44,
                              parent=self.cf_tid_43)
        self.cf_tid_42 = line_item('Net Cash From Discontinued Operations (financing)',
                              45,
                              parent=self.cf_tid_43)
        if data:
            self.add_data(data)


class balance_sheet(financial_statement):
    ''' __init__ will create the necessary accounts for a balance sheet.
    ----------------------------------------------------------------------------
    No data must be added initially, use function add_data for this '''
    def __init__(self, data=None):
    ################
    ## All Assets ##
    ################
        self.bs_tid_41 = line_item('Total Assets', 40)
    ####################
    ## Current Assets ##
    ####################
        self.bs_tid_21 = line_item('Total Current Assets',
                                    20,
                                    parent=self.bs_tid_41)
        self.bs_tid_7 = line_item('Unbilled Revenues',
                                    6,
                                    parent=self.bs_tid_21)
    ##################################
    ## Cash, Equivalents & Children ##
    ##################################
        self.bs_tid_1 = line_item('Cash, Cash Equivalents & Short Term Investments',
                                    0,
                                    parent=self.bs_tid_21)
        self.bs_tid_2 = line_item('     Cash & Cash Equivalents',
                                    1,
                                    parent=self.bs_tid_1)

        self.bs_tid_3 = line_item('     Short Term Investments',
                                    2,
                                    parent=self.bs_tid_1)
    ############################
    ## Receivables & Children ##
    ############################
        self.bs_tid_4 = line_item('Accounts & Notes Receivable',
                                    3,
                                    parent=self.bs_tid_21)
        self.bs_tid_5 = line_item('     Accounts Receivable, Net',
                                    4,
                                    parent=self.bs_tid_4)
        self.bs_tid_6 = line_item('     Notes Receivable, Net',
                                    5,
                                    parent=self.bs_tid_4)
    ##########################
    ## Inventory & Children ##
    ##########################
        self.bs_tid_8 = line_item('Inventories',
                                    7,
                                    parent=self.bs_tid_21)
        self.bs_tid_9 = line_item('     Raw Materials',
                                    8,
                                    parent=self.bs_tid_8)
        self.bs_tid_10 = line_item('     Work In Process',
                                    9,
                                    parent=self.bs_tid_8)
        self.bs_tid_11 = line_item('     Finished Goods',
                                    10,
                                    parent=self.bs_tid_8)
        self.bs_tid_12 = line_item('     Other Inventory',
                                    11,
                                    parent=self.bs_tid_8)
    ######################
    ## Other & Children ##
    ######################
        self.bs_tid_13 = line_item('Other Short Term Assets',
                                    12,
                                    parent=self.bs_tid_21)
        self.bs_tid_14 = line_item('     Prepaid Expenses',
                                    13,
                                    parent=self.bs_tid_13)
        self.bs_tid_15 = line_item('     Derivative & Hedging Assets',
                                    14,
                                    parent=self.bs_tid_13)
        self.bs_tid_16 = line_item('     Assets Held-for-Sale',
                                    15,
                                    parent=self.bs_tid_13)
        self.bs_tid_17 = line_item('     Deferred Tax Assets',
                                    16,
                                    parent=self.bs_tid_13)
        self.bs_tid_18 = line_item('     Income Taxes Receivable',
                                    17,
                                    parent=self.bs_tid_13)
        self.bs_tid_19 = line_item('     Discontinued Operations',
                                    18,
                                    parent=self.bs_tid_13)
        self.bs_tid_20 = line_item('     Miscellaneous Short Term Assets',
                                    19,
                                    parent=self.bs_tid_13)
    ########################
    ## Non-Current Assets ##
    ########################
        self.bs_tid_40 = line_item('Total Noncurrent Assets',
                                    39,
                                    parent=self.bs_tid_41)
    ############
    ## PP & E ##
    ############
        self.bs_tid_22 = line_item('Property, Plant & Equipment, Net',
                                    21,
                                    parent=self.bs_tid_40)
        self.bs_tid_23 = line_item('     Property, Plant & Equipment',
                                    22,
                                    parent=self.bs_tid_22)
        self.bs_tid_24 = line_item('     Accumulated Depreciation',
                                    23,
                                    parent=self.bs_tid_22)
    ###############################
    ## LT Investments & Children ##
    ###############################
        self.bs_tid_25 = line_item('Long Term Investments & Receivables',
                                    24,
                                    parent=self.bs_tid_40)
        self.bs_tid_26 = line_item('     Long Term Investments',
                                    25,
                                    parent=self.bs_tid_25)
        self.bs_tid_27 = line_item('     Long Term Marketable Securities',
                                    26,
                                    parent=self.bs_tid_25)
        self.bs_tid_28 = line_item('     Long Term Receivables',
                                    27,
                                    parent=self.bs_tid_25)
    ######################
    ## Other & Children ##
    ######################
        self.bs_tid_29 = line_item('Other Long Term Assets',
                                    28,
                                    parent=self.bs_tid_40)
        self.bs_tid_30 = line_item('     Intangible Assets',
                                    29,
                                    parent=self.bs_tid_29)
        self.bs_tid_31 = line_item('     Goodwill',
                                    30,
                                    parent=self.bs_tid_29)
        self.bs_tid_32 = line_item('     Other Intangible Assets',
                                    31,
                                    parent=self.bs_tid_29)
        self.bs_tid_33 = line_item('     Prepaid Expense',
                                    32,
                                    parent=self.bs_tid_29)
        self.bs_tid_34 = line_item('     Deferred Tax Assets',
                                    33,
                                    parent=self.bs_tid_29)
        self.bs_tid_35 = line_item('     Derivative & Hedging Assets',
                                    34,
                                    parent=self.bs_tid_29)
        self.bs_tid_36 = line_item('     Prepaid Pension Costs',
                                    35,
                                    parent=self.bs_tid_29)
        self.bs_tid_37 = line_item('     Discontinued Operations',
                                    36,
                                    parent=self.bs_tid_29)
        self.bs_tid_38 = line_item('     Investments in Affiliates',
                                    37,
                                    parent=self.bs_tid_29)
        self.bs_tid_39 = line_item('     Miscellaneous Long Term Assets',
                                    38,
                                    parent=self.bs_tid_29)
    ################################
    ## All Liabilities and Equity ##
    ################################
        self.bs_tid_85 = line_item('Total Liabilities & Equity', 84)
    ##################
    ## Liabilities  ##
    ##################
        self.bs_tid_73 = line_item('Total Liabilities',
                                    72,
                                    parent=self.bs_tid_85)
    #########################
    ## Current Liabilities ##
    #########################
        self.bs_tid_57 = line_item('Total Current Liabilities',
                                    56,
                                    parent=self.bs_tid_73)
    #########################
    ## Payables & Children ##
    #########################
        self.bs_tid_42 = line_item('Payables & Accruals',
                                    41,
                                    parent=self.bs_tid_57)
        self.bs_tid_43 = line_item('     Accounts Payable',
                                    42,
                                    parent=self.bs_tid_42)
        self.bs_tid_44 = line_item('     Accrued Taxes',
                                    43,
                                    parent=self.bs_tid_42)
        self.bs_tid_45 = line_item('     Interest & Dividends Payable',
                                    44,
                                    parent=self.bs_tid_42)
        self.bs_tid_46 = line_item('     Other Payables & Accruals',
                                    45,
                                    parent=self.bs_tid_42)
    #####################
    ## Debt & Children ##
    #####################
        self.bs_tid_47 = line_item('Short Term Debt',
                                    46,
                                    parent=self.bs_tid_57)
        self.bs_tid_48 = line_item('     Short Term Borrowings',
                                    47,
                                    parent=self.bs_tid_47)
        self.bs_tid_49 = line_item('     Short Term Capital Leases',
                                    48,
                                    parent=self.bs_tid_47)
        self.bs_tid_50 = line_item('     Current Portion of Long Term Debt',
                                    49,
                                    parent=self.bs_tid_47)
    ######################
    ## Other & Children ##
    ######################
        self.bs_tid_51 = line_item('Other Short Term Liabilities',
                                    50,
                                    parent=self.bs_tid_57)
        self.bs_tid_52 = line_item('     Deferred Revenue',
                                    51,
                                    parent=self.bs_tid_51)
        self.bs_tid_53 = line_item('     Derivatives & Hedging',
                                    52,
                                    parent=self.bs_tid_51)
        self.bs_tid_54 = line_item('     Deferred Tax Liabilities',
                                    53,
                                    parent=self.bs_tid_51)
        self.bs_tid_55 = line_item('     Discontinued Operations',
                                    54,
                                    parent=self.bs_tid_51)
        self.bs_tid_56 = line_item('     Miscellaneous Short Term Liabilities',
                                    55,
                                    parent=self.bs_tid_51)
    #############################
    ## Non-Current Liabilities ##
    #############################
        self.bs_tid_72 = line_item('Total Noncurrent Liabilities',
                                    71,
                                    parent=self.bs_tid_73)
    #####################
    ## Debt & Children ##
    #####################
        self.bs_tid_58 = line_item('Long Term Debt',
                                    57,
                                    parent=self.bs_tid_72)
        self.bs_tid_59 = line_item('     Long Term Borrowings',
                                    58,
                                    parent=self.bs_tid_58)
        self.bs_tid_60 = line_item('     Long Term Capital Leases',
                                    59,
                                    parent=self.bs_tid_58)
    ######################
    ## Other & Children ##
    ######################
        self.bs_tid_61 = line_item('Other Long Term Liabilities',
                                    60,
                                    parent=self.bs_tid_72)
        self.bs_tid_62 = line_item('     Accrued Liabilities',
                                    61,
                                    parent=self.bs_tid_61)
        self.bs_tid_66 = line_item('     Deferred Compensation',
                                    65,
                                    parent=self.bs_tid_61)
        self.bs_tid_67 = line_item('     Deferred Revenue',
                                    66,
                                    parent=self.bs_tid_61)
        self.bs_tid_68 = line_item('     Deferred Tax Liabilities',
                                    67,
                                    parent=self.bs_tid_61)
        self.bs_tid_69 = line_item('     Derivatives & Hedging',
                                    68,
                                    parent=self.bs_tid_61)
        self.bs_tid_70 = line_item('     Discontinued Operations',
                                    69,
                                    parent=self.bs_tid_61)
        self.bs_tid_71 = line_item('     Miscellaneous Long Term Liabilities',
                                    70,
                                    parent=self.bs_tid_61)
    #########################
    ## Continued, Pensions ##
    #########################
        self.bs_tid_63 = line_item('     Pension Liabilities',
                                    62,
                                    parent=self.bs_tid_61)
        self.bs_tid_64 = line_item('       Pensions',
                                    63,
                                    parent=self.bs_tid_63)
        self.bs_tid_65 = line_item('       Other Post-Retirement Benefits',
                                    64,
                                    parent=self.bs_tid_63)
    #############
    ## Equity  ##
    #############
        self.bs_tid_84 = line_item('Total Equity',
                                    83,
                                    parent=self.bs_tid_85)
        self.bs_tid_83 = line_item('Minority Interest',
                                    82,
                                    parent=self.bs_tid_84)
    #####################################
    ## Equity Before Minority Interest ##
    #####################################
        self.bs_tid_82 = line_item('Equity Before Minority Interest',
                                    81,
                                    parent=self.bs_tid_84)
        self.bs_tid_74 = line_item('     Preferred Equity',
                                    73,
                                    parent=self.bs_tid_82)
        self.bs_tid_79 = line_item('     Treasury Stock',
                                    78,
                                    parent=self.bs_tid_82)
        self.bs_tid_80 = line_item('     Retained Earnings',
                                    79,
                                    parent=self.bs_tid_82)
        self.bs_tid_81 = line_item('     Other Equity',
                                    80,
                                    parent=self.bs_tid_82)
    ##############################
    ## Continued, Issued Equity ##
    ##############################
        self.bs_tid_75 = line_item('Share Capital & Additional Paid-In Capital',
                                    74,
                                    parent=self.bs_tid_82)
        self.bs_tid_76 = line_item('     Common Stock',
                                    75,
                                    parent=self.bs_tid_75)
        self.bs_tid_77 = line_item('     Additional Paid in Capital',
                                    76,
                                    parent=self.bs_tid_75)
        self.bs_tid_78 = line_item('     Other Share Capital',
                                    77,
                                    parent=self.bs_tid_75)
        if data:
            self.add_data(data)
