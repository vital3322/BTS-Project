# -*- coding: utf-8 -*-
import re
import os

# arr_pattern list of "re.compile" patterns

def filter_pattern(arr_pattern, text):
    stack_trace_flag = 0
    temp_str = ' '
    cleaned_text = text
    temp_str = text
    
    pattern_a_lot_of_ERROR = re.compile('.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*')
    if pattern_a_lot_of_ERROR.search(temp_str):
        stack_trace_flag = 1
        temp_str = pattern_a_lot_of_ERROR.sub(' ', temp_str)
        cleaned_text = temp_str
            
    for i, pattern in enumerate(arr_pattern):
        if pattern.search(temp_str):
            if ( ((i > 8) and (i <= 19)) or (i == 27) or (i == 35) or (i == 40) ): #change i if number of stack-trace regex changes! 
                stack_trace_flag = 1
            temp_str = pattern.sub(' ', temp_str)
            cleaned_text = temp_str

    cleaned_text = os.linesep.join([s for s in cleaned_text.splitlines() if s]) #ct

    temp_str = " ".join(temp_str.split())
    return [temp_str, stack_trace_flag]

def filter_pattern(arr_pattern, text):

    stack_trace_flag = 0
    temp_str = ' '
    cleaned_text = ' '
    cleaned_text = text
    temp_str = text
    
    pattern_a_lot_of_ERROR = re.compile('.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*\\n.*ERROR.*')
    if pattern_a_lot_of_ERROR.search(temp_str):
        stack_trace_flag = 1
        temp_str = pattern_a_lot_of_ERROR.sub(' ', temp_str)
        cleaned_text = temp_str

                
    for i, pattern in enumerate(arr_pattern):
        if pattern.search(temp_str):
            if ( ((i > 8) and (i <= 19)) or (i == 27) or (i == 35) or (i == 40) ): #change i if number of stack-trace regex changes!
                stack_trace_flag = 1
            temp_str = pattern.sub(' ', temp_str)
            cleaned_text = temp_str

    cleaned_text = os.linesep.join([s for s in cleaned_text.splitlines() if s]) #ct

    temp_str = " ".join(temp_str.split())
    return [temp_str, stack_trace_flag]