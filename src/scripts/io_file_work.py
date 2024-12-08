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

def load_fault_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)  # Parses CSV as list of dictionaries
        return list(reader)


def save_test_vectors(test_vectors, test_vectors_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(test_vectors_path), exist_ok=True)
    
    # Extract all unique connections for CSV headers
    connections = sorted({tv['connection'] for vector in test_vectors for tv in vector})
    headers = ['id'] + connections  # Add 'id' column as the first header
    
    # Create a list of dictionaries with connection values for each vector
    rows = []
    for i, vector in enumerate(test_vectors, start=1):
        row = {conn: None for conn in connections}  # Initialize row with None for all connections
        row['id'] = i  # Assign a unique id to each vector
        for tv in vector:
            row[tv['connection']] = tv['value']    # Fill in the value for each connection
        rows.append(row)
    
    # Write to CSV
    with open(test_vectors_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write headers
        writer.writerows(rows)  # Write rows

    print(f"Test vectors saved to {test_vectors_path}")


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
    
