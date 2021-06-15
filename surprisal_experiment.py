#!/usr/bin/env python3
import os
# The home dir on the node's scratch disk
USER = os.getenv('USER')
# This may need changing to e.g. /disk/scratch_fast depending on the cluster
SCRATCH_DISK = '/disk/scratch'
SCRATCH_HOME = f'{SCRATCH_DISK}/{USER}'
INPUT_HOME = f'{SCRATCH_HOME}/input'
OUTPUT_HOME = f'{SCRATCH_HOME}/output'

base_call = (f"time python main.py --cuda  --test --words --nopp"
             f"")


languages = ['mixed', 'english', 'dutch']
hidden_dims = [650]
seeds = [2,3,4]
files = ['english_gram.txt', 'english_ungram.txt', 'dutch_gram.txt', 'dutch_ungram.txt']
suffix = f""
second_suffix = f"_half"
epochs = 3

settings = [(language, dim, seed, file) for language in languages for dim in hidden_dims for seed in seeds for file in files]
nr_expts = len(settings)
print(nr_expts)

output_file = open("surprisal_experiment.txt", "w")

for language, dim, seed, file in settings:
    # Note that we don't set a seed for rep - a seed is selected at random
    # and recorded in the output data by the python script
    expt_call = (
        f"{base_call} "
        f"--data_dir \'{INPUT_HOME}/\' "
        f"--model_file \'{INPUT_HOME}/{language}/nhid{dim}_seed{seed}_epochs{epochs}{suffix}.pt\' "
        f"--vocab_file \'{INPUT_HOME}/{language}/vocab.txt\' "
        f"--testfname \'{INPUT_HOME}/grammaticality_test/english_gram.txt\' "
    )
    expt_call += f"> {OUTPUT_HOME}/surprisal/{language}/nhid{dim}_seed{seed}_epochs{epochs}{suffix}.log"

    print(expt_call, file=output_file)
    print(expt_call)
output_file.close()
