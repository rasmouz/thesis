import sys
from scipy import stats
folder = sys.argv[1]

def mean_surprisal(file, indices):
    index=0
    surs = []
    surs_det = []
    with open(file) as techno:
        for line in techno:
            split = line.split()
            word_index = split[2]
            sentence_index = split[1]
            searched_word_index = indices[index]
            if split[2] == str(indices[index-1]+1 + (index==5)) and int(split[1])==index-1:
                if not unk:
                    #print('det',split[1], split[0], split[4], 'yes')
                    surs_det.append(split[4])
                else:
                    #print('det',split[1], split[0], split[4], 'no')
                    pass
            if split[2] == str(indices[index]) and int(split[1])==index:
                if split[0]!='<unk>':
                    unk = False
                    #print(split[1], split[0], split[4], 'yes')
                    surs.append(split[4])
                else:
                    unk = True
                    #print(split[1], split[0], split[4], 'no')
                index += 1

            if index > 16:
                break
    return sum([float(sur) for sur in surs])/len(surs), \
            sum([float(sur) for sur in surs_det])/len(surs_det), \
            [float(sur) for sur in surs], \
            [float(sur) for sur in surs_det]

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
    4:14, #also 15
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

eg = mean_surprisal(folder+'english_gram_result.txt', [i for i in list(english_indices.values())])
eu = mean_surprisal(folder+'english_ungram_result.txt', [i-1 for i in list(english_indices.values())])
dg = mean_surprisal(folder+'dutch_gram_result.txt', [i for i in list(dutch_indices.values())])
du = mean_surprisal(folder+'dutch_ungram_result.txt', [i-1 for i in list(dutch_indices.values())])
print("english grammatical:  V3 {} Det1 {}".format(eg[0], eg[1]))
print("english ungrammatical: V3 {} Det1 {}".format(eu[0], eu[1]))
print("english p-values: V3 {} Det1 {}".format(stats.ttest_rel(eg[2],eu[2])[1], stats.ttest_rel(eg[3],eu[3])[1]))
print('-'*65)
print("dutch grammatical:  V3 {} Det1 {}".format(dg[0], dg[1]))
print("dutch ungrammatical: V3 {} Det1 {}".format(du[0], du[1]))
print("dutch p-values: V3 {} Det1 {}".format(stats.ttest_rel(dg[2],du[2])[1], stats.ttest_rel(dg[3],du[3])[1]))
