import json
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm
import random
from random import sample

unked_filename = "unked_dutch.txt"
vocab = "vocab_dutch.txt"
obligatory_words = "obligatory_words.txt"
important_sentences = "important_sentences.txt"
subsampled_sents = "subsampled_sentences.txt"
final = "train_final.txt"
testvalid = "testvalid.txt"

top_words = set()
with open(vocab, 'r') as v:
    for line in v:
        word = line.strip()
        top_words.add(word)
print(len(top_words))

obligatory_words_dict = dict()
with open(obligatory_words, 'r') as o:
    for number, line in enumerate(o):
        words = word_tokenize(line)
        for word in words:
            obligatory_words_dict[word] = 0
#print(obligatory_words_dict)
obligatory_words = list(obligatory_words_dict.keys())
"""
with open(unked_filename, 'r') as f:
    for number, line in enumerate(f):
        words = word_tokenize(line)
        for word in words:
            if word in obligatory_words:
                obligatory_words_dict[word] += 1
        if number % 10**5 == 0:
            print(number, line)
print(obligatory_words_dict)
"""
important_words = []
with open("count_dict.json", "r") as f:
    dic = json.load(f)
for word in obligatory_words:
    try:
        if dic[word] < 1000:
            important_words.append(word)
    except KeyError as e:
        print('Not in data: ', e)

"""
with open(unked_filename, 'r') as unk, open(important_sentences, 'w') as imp:
    for number, line in enumerate(unk):
        words = word_tokenize(line)
        for word in words:
            if word in important_words:
                imp.write(line)
                continue

"""

train_size = 1622969
valid_size = 202871
total_size = train_size + (2 * valid_size)
important_size = 8762
collect = total_size - important_size
unked_size = 6287158

with open(unked_filename, 'r') as unk, open(subsampled_sents, 'w') as sub:
    indices = sample(range(unked_size), collect)
    indices.sort()
    i = 0
    for n,line in enumerate(unk):
        try:
            if n == indices[i]:
                sub.write(line)
                i += 1
        except IndexError:
            print(i, indices[i-1],len(indices))
        if n % 100000 == 0:
            print(n)
imp = open(important_sentences, 'r')
important_sentences_list = imp.readlines()
sub = open(subsampled_sents, 'r')
subsampled_list = sub.readlines()
random.shuffle(subsampled_list)
train = subsampled_list[:train_size - important_size]
valid = subsampled_list[train_size - important_size:-valid_size]
test = subsampled_list[-valid_size:]
train = train + important_sentences_list
random.shuffle(train)
for i, l in enumerate(train):
    if l.strip() == '':
        del train[i]
with open ("train.txt", "w") as out:
    out.write("".join(train))
with open ("valid.txt", "w") as out:
    out.write("".join(valid))
with open ("test.txt", "w") as out:
    out.write("".join(test))

"""
with ( open(subsampled_sents, 'r') as sub,
      open(train_final, 'w') as train,
      open(testvalid, 'w' as rest):
    final_size = 1622969
    important_size = 8762
    collect = final_size - important_size
    subsize = 1622969 + (2 * 202871) - important_size
    indices = sample(range(subsize), collect)
    indices.sort()
    i = 0; j = 0
    for n,line in enumerate(sub):
        if n == indices[i]:
            train.write(line)
            i += 1
        else:
            testvalid.write(line)
        if n % 100000 == 0:
            print(n)
"""
