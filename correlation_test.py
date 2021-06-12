import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
from scipy import stats

parser = argparse.ArgumentParser(description='Computes the Spearman correlation between reading times and surprisals')
parser.add_argument('--language', type=str, default=None,
                    choices=['english', 'dutch'],
                    help='If tested on one language only, specify the language')
parser.add_argument('--rt_dir', type=str, default='./',
                    help='location of the reading time data')
parser.add_argument('--surprisal_dir', type=str, default='./',
                    help='location of the surprisal data')
parser.add_argument('--plot_gram_vs_ungram', action='store_true',
                    help='plot the grammatical results vs the ungrammatical results')
parser.add_argument('--plot_correlation', action='store_true',
                    help='plot the reading times vs the surprisals to visualize correlation')
parser.add_argument('--means', action='store_true',
                    help='print correlation between mean surprisals or reading times over all 16 test sentences')
parser.add_argument('--surprisal_suffix', type=str, default='',
                    help='suffix of surprisal files, such as `_bi` or `_mono`')
args = parser.parse_args()

def get_reading_times(file):
    data = pd.read_csv(file)
    if file[-6:] == "en.csv":
        not_used = [' targetpos', ' proficiency', ' itempos']
    else:
        not_used = [' targetpos', ' itempos']
    for i in not_used:
        del data[i]
    data_np = data.to_numpy()
    data_np[:,4] = data_np[:,4].astype(np.float)
    for i in range(len(data_np)):
        data_np[i][1] = int(data_np[i][1][2:])
    data_list = data_np.tolist()
    gram = [[] for i in range(16)]
    ungram = [[] for i in range(16)]
    for line in data_list:
        index = line[1] - 1
        if line[2] == 1:
            gram[index].append(list(line[3:]))
        elif line[2] == -1:
            ungram[index].append(list([line[3]]+line[5:]))
        else:
            raise Error("wrong grammaticality key")

    for i in range(len(gram)):
        gram[i] = np.array(gram[i]).mean(axis=0)
        ungram[i] = np.array(ungram[i]).mean(axis=0)
    return np.array(gram), np.array(ungram)

def get_surprisals(file, ignore_indices, grammatical=True):
    number_sentences = 16
    number_words = 8 if grammatical else 7
    surprisals = [[] for j in range(number_sentences)]

    with open(file) as f:
        first_line = f.readline()
        for line in f:
            split = line.split()
            try:
                sentence_index = int(split[1])
            except ValueError:
                continue
            surprisals[sentence_index].append(float(split[4]))
    for i in range(len(surprisals)):
        if ignore_indices[i+1] is not None:
            for ii in ignore_indices[i+1]:
                del surprisals[i][ii-1]
        if grammatical:
            surprisals[i] = surprisals[i][-9:-1]
        else:
            surprisals[i] = [surprisals[i][-9]]+surprisals[i][-7:-1]


    return np.array(surprisals)

def plot_gram_vs_ungram(title, gram, ungram):
    plt.bar([i-.2 for i in range(len(gram))],gram, width=.4, label='gram')
    plt.bar([.2]+[i+.2 for i in range(2,len(gram))],ungram, width=.4, label='ungram')
    labels = ['V1', 'V2', 'V3', 'NP1', 'NP2', 'PP1', 'PP2', 'PP3']
    plt.xticks([i for i in range(8)], labels)
    plt.legend(loc='lower right')
    plt.title(title)
    plt.show()

def plot_correlation(title, reading_times, surprisals, grammatical=True):
    plt.plot(reading_times.flatten(), surprisals.flatten(), '.')
    plt.title(title)
    plt.xlabel('surprisal')
    plt.ylabel('reading time')
    plt.show()
    if args.means:
        plt.scatter(reading_times.mean(axis=0), surprisals.mean(axis=0))
        #plt.plot(reading_times.mean(axis=0), surprisals.mean(axis=0), '.')
        if grammatical:
            labels = ['V1', 'V2', 'V3', 'NP1', 'NP2', 'PP1', 'PP2', 'PP3']
        else:
            labels = ['V1', 'V3', 'NP1', 'NP2', 'PP1', 'PP2', 'PP3']
        for i, txt in enumerate(labels):
            plt.annotate(txt, (reading_times.mean(axis=0)[i], surprisals.mean(axis=0)[i]))
        plt.title(title+' averaged over sentences')
        plt.xlabel('surprisal')
        plt.ylabel('reading time')
        plt.show()

ignore_en = {
    1: None,
    2: None,
    3: [-8],
    4: None,
    5: [-6],
    6: [-8],
    7: None,
    8: None,
    9: None,
    10: [-8],
    11: [-8, -1],
    12: [-1],
    13: None,
    14: [-8],
    15: None,
    16: None,
}

ignore_nl = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: [-6],
    6: None,
    7: None,
    8: None,
    9: None,
    10: None,
    11: None,
    12: None,
    13: None,
    14: None,
    15: None,
    16: None,
}

if args.language in ['english', None]:
    sur_en_gram = get_surprisals(args.surprisal_dir+"/english_gram_result"+args.surprisal_suffix+".txt", ignore_en)
    sur_en_ungram = get_surprisals(args.surprisal_dir+"/english_ungram_result"+args.surprisal_suffix+".txt", ignore_en, grammatical=False)
    rt_en_gram, rt_en_ungram = get_reading_times(args.rt_dir+"RTdata_nl_en.csv")
    spearman_gram = stats.spearmanr(sur_en_gram.flatten(), rt_en_gram.flatten())
    spearman_ungram = stats.spearmanr(sur_en_ungram.flatten(), rt_en_ungram.flatten())
    print('English Results:')
    print('grammatical:   correlation {:5.3f} p-value {:.2e}'.format(spearman_gram[0], spearman_gram[1]))
    print('ungrammatical: correlation {:5.3f} p-value {:.2e}'.format(spearman_ungram[0], spearman_ungram[1]))
    if args.means:
        spearman_gram = stats.spearmanr(sur_en_gram.mean(axis=0), rt_en_gram.mean(axis=0))
        spearman_ungram = stats.spearmanr(sur_en_ungram.mean(axis=0), rt_en_ungram.mean(axis=0))
        print('grammatical mean  : correlation {:5.3f} p-value {:.2e}'.format(spearman_gram[0], spearman_gram[1]))
        print('ungrammatical mean: correlation {:5.3f} p-value {:.2e}'.format(spearman_ungram[0], spearman_ungram[1]))
    print('-'*99)
if args.language in ['dutch', None]:
    sur_nl_gram = get_surprisals(args.surprisal_dir+"/dutch_gram_result"+args.surprisal_suffix+".txt", ignore_nl)
    sur_nl_ungram = get_surprisals(args.surprisal_dir+"/dutch_ungram_result"+args.surprisal_suffix+".txt", ignore_nl, grammatical=False)
    rt_nl_gram, rt_nl_ungram = get_reading_times(args.rt_dir+"RTdata_nl_nl.csv")
    spearman_gram = stats.spearmanr(sur_nl_gram.flatten(), rt_nl_gram.flatten())
    spearman_ungram = stats.spearmanr(sur_nl_ungram.flatten(), rt_nl_ungram.flatten())
    print('Dutch Results:')
    print('grammatical:   correlation {:5.3f} p-value {:.2e}'.format(spearman_gram[0], spearman_gram[1]))
    print('ungrammatical: correlation {:5.3f} p-value {:.2e}'.format(spearman_ungram[0], spearman_ungram[1]))
    if args.means:
        spearman_gram = stats.spearmanr(sur_nl_gram.mean(axis=0), rt_nl_gram.mean(axis=0))
        spearman_ungram = stats.spearmanr(sur_nl_ungram.mean(axis=0), rt_nl_ungram.mean(axis=0))
        print('grammatical mean  : correlation {:5.3f} p-value {:.2e}'.format(spearman_gram[0], spearman_gram[1]))
        print('ungrammatical mean: correlation {:5.3f} p-value {:.2e}'.format(spearman_ungram[0], spearman_ungram[1]))
    print('-'*99)

if args.plot_gram_vs_ungram is True:
    if args.language in ['english', None]:
        plot_gram_vs_ungram('English Surprisals', sur_en_gram.mean(axis=0), sur_en_ungram.mean(axis=0))
        plot_gram_vs_ungram('English Reading Times', rt_en_gram.mean(axis=0), rt_en_ungram.mean(axis=0))
    if args.language in ['dutch', None]:
        plot_gram_vs_ungram('Dutch Surprisals', sur_nl_gram.mean(axis=0), sur_nl_ungram.mean(axis=0))
        plot_gram_vs_ungram('Dutch Reading Times', rt_nl_gram.mean(axis=0), rt_nl_ungram.mean(axis=0))

if args.plot_correlation is True:
    if args.language in ['english', None]:
        plot_correlation('English grammatical', sur_en_gram, rt_en_gram)
        plot_correlation('English ungrammatical', sur_en_ungram, rt_en_ungram, grammatical=False)
    if args.language in ['dutch', None]:
        plot_correlation('Dutch grammatical', sur_nl_gram, rt_nl_gram)
        plot_correlation('Dutch ungrammatical', sur_nl_ungram, rt_nl_ungram, grammatical=False)
