# MusicGen

Automatic music generator made during hackaton
in Amazon Software Development Poland.

## Numerical approach

`docker-compose run musicgen numeric generate -o <path_to_output_midi_file>`

## LSTM approach

### Training

To start training:

`docker-compose run musicgen lstm train start -n <unique_model_name> -p <dir_with_midi_files_to_learn>`

To continue training (started earlier):

`docker-compose run musicgen lstm train resume -n <model_name_used_previously>`

### Music generation

`docker-compose run musicgen lstm generate -n <name_of_trained_model> -o <path_to_output_midi_file>`
