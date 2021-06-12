#!/usr/bin/env python3
"""Script for generating experiments.txt based on the MNIST script at:
https://github.com/cdt-data-science/cluster-scripts"""
import os

# The home dir on the node's scratch disk
USER = os.getenv('USER')
# This may need changing to e.g. /disk/scratch_fast depending on the cluster
SCRATCH_DISK = '/disk/scratch'
SCRATCH_HOME = f'{SCRATCH_DISK}/{USER}'
INPUT_HOME = f'{SCRATCH_HOME}/input'
OUTPUT_HOME = f'{SCRATCH_HOME}/output'

base_call = (f"time python main.py --batch_size '128' --epochs '1' --tied --cuda  "
             "--epochs '10' --trainfname 'train.txt'")

languages = ['mixed']
hidden_dims = [650]
seeds = [1,2,3]

settings = [(language, dim, seed) for language in languages for dim in hidden_dims for seed in seeds]
nr_expts = len(settings)

nr_servers = 10
avg_expt_time = 6*60  # mins
print(f'Total experiments = {nr_expts}')
print(f'Estimated time = {(nr_expts / nr_servers * avg_expt_time)/60} hrs')

output_file = open("experiment.txt", "w")

for language, dim, seed in settings:
    # Note that we don't set a seed for rep - a seed is selected at random
    # and recorded in the output data by the python script
    if language == 'english' or 'dutch':
        expt_call = (
            f"{base_call} "
            f"--data_dir \'{INPUT_HOME}/{language}\' "
            f"--model_file \'{OUTPUT_HOME}/{language}/nhid{dim}_seed{seed}.pt\' "
            f"--vocab_file \'{INPUT_HOME}/{language}/vocab.txt\' "
            f"--nhid \'{dim}\' "
            f"--emsize \'{dim}\' "
            f"--seed \'{seed}\' "
            f"> {OUTPUT_HOME}/{language}/nhid{dim}_seed{seed}.log"
        )
    elif language == 'mixed':
        expt_call = (
            f"{base_call} "
            f"--data_dir \'{INPUT_HOME}/\' "
            f"--validfname \'dutch/valid.txt\' "
            f"--validfname2 \'english/valid.txt\' "
            f"--trainfname \'mixed/train.txt\' "
            f"--model_file \'{OUTPUT_HOME}/{language}/nhid{dim}_seed{seed}.pt\' "
            f"--vocab_file \'{INPUT_HOME}/{language}/vocab.txt\' "
            f"--nhid \'{dim}\' "
            f"--emsize \'{dim}\' "
            f"--seed \'{seed}\' "
            f"> {OUTPUT_HOME}/{language}/nhid{dim}_seed{seed}.log"
        )
    else:
        raise ValueError('Woopsie Daisie')
    print(expt_call, file=output_file)
output_file.close()
