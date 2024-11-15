import pandas as pd
import re
import os
import random
import csv

def load_csv_file(path):
    is_file = os.path.isfile(path)
    file = None
    
    if(is_file):
        file  = pd.read_csv(path, index_col=None)
    return file


def save_list_to_csv(list_data, file_path):
    df = pd.DataFrame(list_data)
    df.to_csv(file_path, index=False, header=False)


def generate_input_file(circuit, path):
    list_of_inputs = []
    headings = ['time']
    for connection in circuit.input_connections:
        headings.append(connection.name)
    list_of_inputs.append(headings)
    
    for i in range(5):
        time = i * 10
        row = [time]
        for i in range(len(headings) - 1):
            value = None
            random_number = random.randint(0, 3)
            if (random_number == 0):
               value = 0 
            elif (random_number == 1):
               value = 1
            elif (random_number == 2):
               value = 'U'
            elif (random_number == 3):
               value =  'Z'

            row.append(value)
        list_of_inputs.append(row)
    
    # print(list_of_inputs)
    save_list_to_csv(list_of_inputs, path)
    
