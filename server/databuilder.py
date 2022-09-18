import pandas as pd
import datetime

STATE_LIST = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
    'Chhattisgarh', 'DNH', 'Delhi', 'Goa', 'Gujarat', 'HP', 'Haryana',
    'J&K', 'Jharkhand', 'Karnataka', 'Kerala', 'MP', 'Maharashtra',
    'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Pondy',
    'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
    'UP', 'Uttarakhand', 'West Bengal'
]

def date_parser(inp: str):
    return datetime.datetime.strptime(inp, "%d/%m/%Y %H:%M:%S").timestamp()

class DataBuilder:
    def __init__(self, csv_path) -> None:

        self.mean = 105.00054901960785
        self.std = 116.42528513552918

        self.df = pd.read_csv(csv_path)
        
        dates = self.df['Dates'].map(date_parser)
        self.df['Dates'] = dates

        self.grouped = self.df.groupby(self.df['States'])

    def build_data(self, state_name, n_past=50):
        if state_name not in STATE_LIST:
            raise ValueError('Invalid State provided')

        group = self.grouped.get_group(state_name)

        time = group['Dates']
        usage = group['Usage']

        assert(time.is_monotonic)

        return time.to_numpy()[-n_past:], usage.to_numpy()[-n_past:]
