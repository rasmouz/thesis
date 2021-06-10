import sys
from scipy import stats
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Computes the mean surprisal for V3 and Det1 and the p-value of a paired t-test')
parser.add_argument('--language', type=str, default=None,
                    choices=['english', 'dutch'],
                    help='If tested on one language only, specify the language')
parser.add_argument('--data_dir', type=str, default='./',
                    help='location of the surprisal data')
parser.add_argument('--plot', action='store_true',
                    help='plot the results')
args = parser.parse_args()

def mean_surprisal(file, indices):
    index=0
    surs_v3 = dict()
    surs_det1 = dict()
    with open(file) as techno:
        for line in techno:
            split = line.split()
            word_index = split[2]
            sentence_index = split[1]
            searched_word_index = indices[index]
            if split[2] == str(indices[index-1]+1 + (index==5)) and int(split[1])==index-1:
                if not unk:
                    surs_det1[int(split[1])+1] = float(split[4])
            if split[2] == str(indices[index]) and int(split[1])==index:
                if split[0]!='<unk>':
                    unk = False
                    surs_v3[int(split[1])+1] = float(split[4])
                else:
                    unk = True
                index += 1

            if index > 16:
                break
    return sum(list(surs_v3.values()))/len(surs_v3), \
            sum(list(surs_det1.values()))/len(surs_det1), \
            surs_v3, \
            surs_det1

english_indices = \
{
    0:10,
    1:10,
    2:11,
    3:10,
    4:10,
    5:11,
    6:10,
    7:10,
    8:10,
    9:11,
    10:11,
    11:10,
    12:10, #unk
    13:11,
    14:10,
    15:10,
    16:0
}

dutch_indices = \
{
    0:12,
    1:12, #unk
    2:12, #unk
    3:12, #unk
    4:14, #unk
    5:12,
    6:12, #unk
    7:12,
    8:12,
    9:12, #unk
    10:12, #unk
    11:12,
    12:12,
    13:12,
    14:14, #unk
    15:12,
    16:0
}

def print_results(language, folder, indices):
    grammatical = mean_surprisal(folder+language+'_gram_result.txt', indices)
    ungrammatical = mean_surprisal(folder+language+'_ungram_result.txt', [i-1 for i in indices])
    print(language+' results:')
    print("grammatical:   V3 {} Det1 {}".format(grammatical[0], grammatical[1]))
    print("ungrammatical: V3 {} Det1 {}".format(ungrammatical[0], ungrammatical[1]))
    print("p-values:      V3 {} Det1 {}".format(stats.ttest_rel(list(grammatical[2].values()),list(ungrammatical[2].values()))[1],
                                                stats.ttest_rel(list(grammatical[3].values()),list(ungrammatical[3].values()))[1]))
    if args.plot:
        plt.bar([i-.2 for i in range(len(grammatical[2]))],list(grammatical[2].values()), width=.4)
        plt.bar([i+.2 for i in range(len(ungrammatical[2]))],list(ungrammatical[2].values()), width=.4)
        plt.xticks([i for i in range(len(grammatical[2]))], list(grammatical[2].keys()))
        plt.ylabel('surprisal')
        plt.xlabel('sentence index')
        plt.title('V3 '+language)
        plt.savefig('V3'+language+'.pdf', format='pdf')
        plt.show()
        plt.bar([i-.2 for i in range(len(grammatical[3]))],list(grammatical[3].values()), width=.4)
        plt.bar([i+.2 for i in range(len(ungrammatical[3]))],list(ungrammatical[3].values()), width=.4)
        plt.xticks([i for i in range(len(grammatical[3]))], list(grammatical[3].keys()))
        plt.ylabel('surprisal')
        plt.xlabel('sentence index')
        plt.title('Det1 '+language)
        plt.savefig('Det1'+language+'.pdf', format='pdf')
        plt.show()

folder = args.data_dir
if args.language is None:
    print_results('english', folder, list(english_indices.values()))
    print('-'*65)
    print_results('dutch', folder, list(dutch_indices.values()))
else:
    if args.language == 'english':
        print_results(args.language, folder, list(english_indices.values()))
    elif args.language == 'dutch':
        print_results(args.language, folder, list(dutch_indices.values()))
