import pandas as pd

def load_csv_file(path):
    file  = pd.read_csv(path)
    return file


