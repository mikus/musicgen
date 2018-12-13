import glob
import pickle
import itertools

import numpy as np
from music21 import converter, instrument, note, chord
from keras.utils import np_utils


class Data:
    def __init__(self, notes):
        self._notes = notes
        self._disctinct_notes = set(list(itertools.chain(*notes)))
        self._distinct_notes_count = len(self._disctinct_notes)
        self._pitchnames = None
        self._note_to_index = None
        self._index_to_note = None

    def store(self, path):
        with open(path, 'wb') as filepath:
            pickle.dump(self._notes, filepath)

    @property
    def distinct_notes_count(self):
        return self._distinct_notes_count

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as filepath:
            notes = pickle.load(filepath)
            return cls(notes)

    @classmethod
    def load_training_set(cls, training_data_path, max_files=0):
        notes = []
        parsed_files = 0

        for file in glob.glob("{}/**/*.mid*".format(training_data_path), recursive=True):
            subnotes = []
            notes.append(subnotes)
            try:
                midi = converter.parse(file)
            except:
                print('cannot parse file')
                continue

            print("Parsing %s" % file)

            notes_to_parse = None

            try:  # file has instrument parts
                s2 = instrument.partitionByInstrument(midi)
                #print(s2)
                #print(s2.parts)
                print(len(s2.parts))
                notes_to_parse = s2.parts[0].recurse()
            except:  # file has notes in a flat structure
                notes_to_parse = midi.flat.notes

            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    subnotes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    subnotes.append('.'.join(str(n) for n in element.normalOrder))

            parsed_files += 1
            if 0 < max_files <= parsed_files:
                break

        return cls(notes)

    @property
    def pitchnames(self):
        if self._pitchnames is None:
            self._pitchnames = sorted(set(item for item in self._disctinct_notes))
        return self._pitchnames

    @property
    def note_to_index(self):
        if self._note_to_index is None:
            self._note_to_index = dict((note, number) for number, note in enumerate(self.pitchnames))
        return self._note_to_index

    @property
    def index_to_note(self):
        if self._index_to_note is None:
            self._index_to_note = dict((number, note) for number, note in enumerate(self.pitchnames))
        return self._index_to_note

    def to_sequences(self, sequence_length=100, generate_output=False):
        """ Prepare the sequences used by the Neural Network """
        network_input = []
        network_output = []

        # create input sequences and the corresponding outputs
        for song_notes in self._notes:
            for i in range(0, len(song_notes) - sequence_length, 1):
                sequence_in = song_notes[i:i + sequence_length]
                network_input.append([self.note_to_index[char] for char in sequence_in])
                if generate_output:
                    sequence_out = song_notes[i + sequence_length]
                    network_output.append(self.note_to_index[sequence_out])

        n_patterns = len(network_input)

        # reshape the input into a format compatible with LSTM layers
        network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
        # normalize input
        network_input = network_input / float(self.distinct_notes_count)

        if generate_output:
            network_output = np_utils.to_categorical(network_output)
            return network_input, network_output
        else:
            return network_input

    def output_to_input(self, index):
        return index / float(self.distinct_notes_count)
