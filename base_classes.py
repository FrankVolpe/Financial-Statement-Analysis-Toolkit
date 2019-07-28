import pandas as pd
from statistics import *

###############
## Line Item ##
###############

class line_item:
    '''When searching for the value of the line item, use data() function '''
    def __init__(self, title, line_position=None, parent=None, populated=False):
    # Set values for class
        self.line_position = line_position
        self.parent = parent
        self.children = []
        self.title = title
        self.populated = populated
    # Add line item to children of parent line item
        if parent:
            self.parent.add_child(self)

    def add_child(self, child):
        ''' Function to add children to line item '''
        self.children.append(child)

    @property
    def data(self):
        ''' Since the data pulled from SimFin are the assigned values
        (not the calculated or chosen ones), this ensures calculated
        line items are populated correctly '''
        if len(self.children) == 0:
            self.populated = True
            return self.value
        else:
            children_sum = sum([child.value for child in self.children])
            if self.value == 0:
                self.value = children_sum
                if self.value == 0:
                    self.populated = True
                return self.value
            if self.value == children_sum and self.value != 0:
                self.populated = False
                return self.value
            else:
                self.populated = True
                return self.value

###############################
## Basic Financial Statement ##
###############################

class financial_statement:
    def __init__(self):
        pass

    def create_reference(self):
        ''' Returns dict, {line_reference : line_item object} '''
        attributes = self.__dict__
        att_keys = list(attributes.keys())
        reference = {}
        for x in range(len(att_keys)):
            try:
                reference[attributes[att_keys[x]].line_position] = attributes[att_keys[x]]
            except AttributeError:
                continue
        return reference

    def set_default(self):
        reference = self.create_reference()
        #ref_keys = list(reference.keys())
        for x in range(len(reference)):
            reference[x].value = 0

    def add_data(self, data):
        ''' Proper data format is simfin API output '''
        reference = self.create_reference()
        value_data = []
        for x in range(len(data['values'])):
            if data['values'][x]['valueAssigned'] == None:
                value_data.append(0)
            else:
                value_data.append(int(data['values'][x]['valueAssigned']))
        for x in range(len(value_data)):
            reference[x].value = value_data[x]

    def display(self, omit=False):
        ''' Displays Pandas series of the financial statement in question
        if omit is set to anything other than false, line items == 0 will
        not be displayed '''
        reference = self.create_reference()
        titles = []
        values = []
        if omit == False:
            for x in range(len(reference)):
                titles.append(reference[x].title)
                values.append(reference[x].data)
        else:
            for x in range(len(reference)):
                if reference[x].data != 0:
                    titles.append(reference[x].title)
                    values.append(reference[x].data)
        return pd.Series(values, index=titles)

###########################################
## Class for ratios/supplemental metrics ##
###########################################

class metric:
    def __init__(self, title, display_pref=None):
        self.title = title
        display_pref = display_pref

    def calc_by_div(self, numerator, denominator):
        try:
            self.numerator = numerator
            self.denominator = denominator
            self.data = numerator.data / denominator.data
        except ZeroDivisionError:
            self.data = float('NaN')

    def calc_by_add(self, inputs):
        self.inputs = inputs
        self.data = 0
        for x in range(len(inputs)):
            self.data += inputs[x].data

    def generate_report(self):
        index = []
        values = []
        if self.inputs:
            for x in range(len(self.inputs)):
                index.append(self.inputs[x].title)
                values.append(self.inputs[x].data)
            index.append(self[x].title)
            values.append(self[x].data)
        else:
            objects = [self.numerator, self.denominator, self]
            for x in range(len(objects)):
                index.append(objects[x].title)
                values.append(objects[x].data)
        return pd.Series(values, index=index)

######################
## Useful Functions ##
######################

def new_metric_add(destination, position, title, period, input):
    '''input new metric and append to list '''
    new_metric = metric(title)
    new_metric.period = period
    new_metric.calc_by_add(input)
    try:
        destination[position][period] = new_metric
    except KeyError:
        destination[position] = {period : new_metric}


def new_metric_div(destination, position, title, period, num, denom):
    '''input new metric and append to list '''
    new_metric = metric(title)
    new_metric.period = period
    new_metric.calc_by_div(num, denom)
    try:
        destination[position][period] = new_metric
    except KeyError:
        destination[position] = {period : new_metric}

def mean_li(param_at_T, param_at_T_1):
    ''' input: two line_item parameters
    output: new line item of mean '''
    new_param = line_item("Average " + param_at_T.title)
    new_param.value = mean([param_at_T.data, param_at_T_1.data])
    return new_param

def negate_li(lineitem):
    ''' input: line_item object
    output: same line_item with value * -1
    also compatible with metric objects '''
    new_param = line_item(lineitem.title)
    new_param.value = lineitem.data * -1
    return new_param

def combine_li(lineitem_1, lineitem_2):
    ''' input: two line_item objects
    output: line_item, combined title & value
    also compatible with metric objects '''
    new_param = line_item(lineitem_1.title + ' and ' + lineitem_2.title)
    new_param.value = lineitem_1.data + lineitem_2.data
    return new_param
