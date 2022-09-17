import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

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

def generate_plot_image(n_days_past: np.ndarray, predictions: np.ndarray, title: str = ''):
    buff = BytesIO()

    n = len(n_days_past)
    n_pred = len(predictions)

    n_days = n + n_pred

    predictions = np.concatenate([n_days_past[-1].reshape(1), predictions])

    x = np.linspace(1, n_days + 1, n_days)
    
    plt.plot(x[:n], n_days_past, 'b.-', label='Usage data')
    plt.plot(x[n-1:], predictions, 'r.-', label='Prediction')

    plt.title(title)
    plt.grid(True)
    plt.legend()
    
    plt.savefig(buff, format='png')
    plt.clf()

    return buff

if __name__ == '__main__':
    generate_plot_image(np.array([10, 14, 16, 13, 11, 9, 10]), np.array([12, 12, 17, 21, 18]))