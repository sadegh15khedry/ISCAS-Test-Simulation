import pandas as pd

def load_csv_file(path):
    file  = pd.read_csv(path, index_col=None)
    # file = file.to_csv(index=False)
    return file


