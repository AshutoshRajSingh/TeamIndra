import numpy as np

MONTH_LENGTH = 30

def aggregate_last_month_usage(usages: np.ndarray):
    return np.sum(usages[-MONTH_LENGTH:])

def aggregate_last_n_day_usage(usages: np.ndarray, n: int):
    return np.sum(usages[-n:])

# Contains mapping to state names that have a representational discrepancy between
# the dataset and the cea api
MANUAL_MAPPING = {
    'DNH': 'Dadra & Nagar Haveli',
    'HP': 'Himachal Pradesh',
    'J&K': 'UTs of J&K and Ladakh',
    'MP': 'Madhya Pradesh',
    'Pondy': 'Puducherry',
    'UP': 'Uttar Pradesh',
}
