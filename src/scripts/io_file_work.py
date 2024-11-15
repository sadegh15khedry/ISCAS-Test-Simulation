import pandas as pd

def load_csv_file(path):
    file  = pd.read_csv(path, index_col=None)
    # file = file.to_csv(index=False)
    return file

def extract_input_lines(ascas_file):
    with open(ascas_file, 'r') as f:
        lines = f.readlines()

    input_lines = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 4 and parts[1] == 'inpt':
            input_lines.append(parts[0])

    return input_lines
def generate_input_file():
    print("Generating input file")      
# Example usage:
# ascas_file = 'c432.ascas'
# input_lines = extract_input_lines(ascas_file)
# print(input_lines)


