
## Need to finish KPIs first

    def fs_profitability(self):
        profitability_df = pd.DataFrame()

        profitability = []
        for x in range(len(self.new_range)):
            r_o_a = metric("Return on Assets")
            r_o_a.calc_by_div(data.i_s.is_tid_55.data,                  # Net Income
                                 mean([data.b_s.bs_tid_41.data,         # Total Assets
                                       t_1_data.b_s.bs_tid_41.data]))   # Total Assets T-1
            profitability.append(r_o_a)

            op_roa = metric("Operating ROA")
            op_roa.calc_by_div(data.i_s.is_tid_19.data,                 # Operating Income
                              data.b_s.bs_tid_41.data)                  # Total Assets
            profitability.append(op_roa)

            r_o_tc = metric("Return on Total Capital")
            r_o_tc.calc_by_div({EBIT},
                              mean([data.b_s.bs_tid_41.data,         *# Total Capital
                                    t_1_data.b_s.bs_tid_41.data]))   *# Total Capital T-1
            profitability.append(r_o_tc)

            r_o_e = metric("Return on Equity")
            r_o_e.calc_by_div(data.i_s.is_tid_55.data,                  # Net Income
                             {average total equity})
            profitability.append(r_o_e)

            r_o_ce = metric("Return on Common Equity")
            r_o_ce.calc_by_div(sum(data.i_s.is_tid_55.data,             # Net Income
                                   -1 * {preferred dividends}),
                              {average common equity})
            profitability.append(r_o_ce)

            for y in range(len(profitability)):
                profitability_df.at[profitability[y].title, self.new_range[x]] = profitability[y].data

        self.profitability = profitability_df

#########################################
#########################################
#########################################
#########################################
#########################################


        solvency_ratios = []

        metric("Debt to Equity")
        .calc_by_div()
        solvency_ratios.append()

        metric("Debt to Capital")
        .calc_by_div()
        solvency_ratios.append()

        metric("Debt to Assets")
        .calc_by_div()
        solvency_ratios.append()

        metric("Financial Leverage")
        .calc_by_div()
        solvency_ratios.append()

        metric("Interest Coverage")
        .calc_by_div()
        solvency_ratios.append()

        metric("Fixed Charge Coverage")
        .calc_by_div()
        solvency_ratios.append()



        days_measures = []

        metric("Days of Sales Outstanding")
        .calc_by_div(365,
                     {Receivables Turnover})
        days_measures.append()

        metric("Days of Inventory Outstanding")
        .calc_by_div(365,
                     {Inventory Turnover})
        days_measures.append()

        metric("Number of Days of Payables")
        .calc_by_div(365,
                     {Payables Turnover})
        days_measures.append()





        metric("Defensive Interval")
        .calc_by_div(sum([data['Cash & Cash Equivalents'],
                         data['Accounts Receivable']]),
                     mean([data['{daily expenditures}'],
                          data_last_year['{daily expenditures}']]))

        metric("Cash Conversion Cycle")
        .calc_by_add([days sales outstanding,
                      days inventory on hand,
                      -1 * days payables])

# Add KPIs before calculations

#ratios_df = pd.DataFrame(index = self.line_items, columns = self.range)
