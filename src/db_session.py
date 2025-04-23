import pandas as pd

session = None

def get_session():
    global session
    if session is None:
        # session = duckdb.read_csv("focus_sample_100000.csv", header = False, sep = ",")
        session = pd.read_csv("sample_data/focus_sample_100000.csv", low_memory=False)
    return session

