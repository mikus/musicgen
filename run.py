#!/usr/bin/env python3

import click

from musicgen.numeric import generate as numeric_generate
from musicgen.lstm.utils import (
    start_training,
    resume_training,
    generate as lstm_generate,
    populate_paths,
    choose_best_weights
)


@click.group()
def cli():
    pass


#### pure numerical approach ####

@cli.group()
def numeric():
    pass


@numeric.command()
@click.option('-o', '--output', help='where the generated samples should be stored', required=True,
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, resolve_path=True))
def generate(output):
    numeric_generate(output)


#### RNN approach ####

@cli.group()
def lstm():
    pass


@lstm.group()
def train():
    pass


@train.command()
@click.option('-n', '--name', help='Unique name for current training', required=True,
              type=str)
@click.option('-p', '--patterns-path', help='Path to the training samples', required=True,
              type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True))
@click.option('-m', '--max-patterns', help='Max number of patterns to train', default=0,
              type=int)
def start(name, patterns_path, max_patterns):
    notes_path, weights_dir = populate_paths(name, True)
    start_training(notes_path, weights_dir, patterns_path, max_patterns)


@train.command()
@click.option('-n', '--name', help='Unique name for current training', required=True,
              type=str)
def resume(name):
    notes_path, weights_dir = populate_paths(name, False)
    resume_training(notes_path, weights_dir)


@lstm.command()
@click.option('-n', '--name', help='Model name to use for generation', required=True,
              type=str)
@click.option('-o', '--output', help='where the generated samples should be stored', required=True,
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, resolve_path=True))
@click.option('-s', '--samples', help='Number of samples to generate', default=240)
def generate(output, name, samples):
    notes_path, weights_dir = populate_paths(name, False)
    weights_path = choose_best_weights(weights_dir)
    print('Weights from {} are used to generate samples'.format(weights_path))
    lstm_generate(samples, output, notes_path, weights_path)


if __name__ == '__main__':
    cli()

