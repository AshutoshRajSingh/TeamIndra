import tensorflow as tf

from databuilder import DataBuilder

# To make pylance stop screaming
keras = tf.keras

class ModelHandler:
    def __init__(self, model_path) -> None:
        self.model = keras.models.load_model(model_path)
        self.data_builder = DataBuilder('./data/long_data_.csv')
    def make_predictions(self, state_name):
        _, usage = self.data_builder.build_data(state_name)
        state_series_x = usage.reshape(1, len(usage))

        state_series_x = (state_series_x - self.data_builder.mean) / self.data_builder.std

        pred = self.model.predict(state_series_x)
        return pred * self.data_builder.std + self.data_builder.mean
