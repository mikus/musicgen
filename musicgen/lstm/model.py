import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint


class Model:
    def __init__(self, input_shape, output_count, weights=None):
        self._model = Sequential()
        self._model.add(LSTM(
            512,
            input_shape=(input_shape[1], input_shape[2]),
            return_sequences=True
        ))
        self._model.add(Dropout(0.3))
        self._model.add(LSTM(256, return_sequences=True))
        self._model.add(Dropout(0.3))
        self._model.add(LSTM(256, return_sequences=False))
        self._model.add(Dense(256))
        self._model.add(Dropout(0.3))
        self._model.add(Dense(output_count))
        self._model.add(Activation('softmax'))
        self._model.compile(loss='categorical_crossentropy', optimizer=Adam())

        if weights is not None:
            self._model.load_weights(weights)

    def train(self, network_input, network_output, epochs, batch_size, weights_dir):
        filepath = weights_dir + "/weights-{epoch:02d}-{loss:.4f}.hdf5"
        checkpoint = ModelCheckpoint(
            filepath,
            monitor='loss',
            verbose=0,
            save_best_only=True,
            mode='min'
        )
        callbacks_list = [checkpoint]

        self._model.fit(network_input, network_output, epochs=epochs, batch_size=batch_size, callbacks=callbacks_list)

    def generate(self, input, count, output_to_input):
        output = []
        pattern = input
        for note_index in range(count):
            network_input = np.reshape(pattern, (1, len(pattern), 1))
            prediction = self._model.predict(network_input, verbose=0)
            index = np.argmax(prediction)
            output.append(index)
            pattern = pattern[1:len(pattern)]
            network_output_converted_to_input = np.reshape(output_to_input(index), (1, 1))
            pattern = np.append(pattern, network_output_converted_to_input, axis=0)

        return output
