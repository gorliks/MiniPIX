import time, sys
import logging
import json
import numpy as np
import os

def parse_command(command):
    # command = "key1=val1 key2=val2"
    try:
        parsed = dict((key, value) for key, value in [i.split('=') for i in command.split()])
    except:
        print('No keywords, using command as a string')
        parsed = str(command)
    return parsed


def convert_dictionary_string_to_dictionary(dictionary_string):
    return json.loads(dictionary_string)

def read_data_file(file_name):
    if os.path.isfile(file_name):
        data = np.loadtxt(  file_name  )
    else:
        data = None
    return data
