from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import pickle
import json

#filename = "combineddutch.txt"
filename = "clean_dutch.txt"
n_most_common = 50000
clean_sent_filename = "clean_dutch.txt"  # assuming full file is too big for RAM
unked_filename = "unked_dutch.txt"
freq_dict = Counter()
obligatory_words = "obligatory_words.txt"

"""
# read in file
with open(filename, 'r') as f, open(clean_sent_filename, 'w') as out:
    for line_number, line in enumerate(f):
        # check if line is title, skip over next two lines
        if line.startswith("<doc id="):
            flag = True #the flag deletes the title (first line after markup starts)
            continue
        if flag:
            flag = False
            continue
        # skip over doc end markup and other HTML markup:
        if line.startswith("<"):
            continue
        if line.startswith("!"):
            continue
        if line.startswith("__"):
            continue
        if not line or line.strip()=="":
            continue
        # iterate once to build frequency dictionary and save cleaned file
        else:
            # split each line into a list of sentences
            sentences = sent_tokenize(line.strip())
            print(line_number, sentences)
            for sentence in sentences:
                # build lowercase frequency dictionary
                freq_dict.update(word_tokenize(sentence))
                out.write(sentence+'\n')



with open(clean_sent_filename, 'r') as f:
    for number, line in enumerate(f):
        words = word_tokenize(line)
        freq_dict.update(words)
        if number % 10**5==0:
            print(number)

print('done with collecting words')
count_dict = open("count_dict.json", "w")
json.dump(freq_dict, count_dict)
count_dict.close()
"""
obligatory_words_set = set()
with open(obligatory_words, 'r') as o:
    for number, line in enumerate(o):
        words = word_tokenize(line)
        for word in words:
            obligatory_words_set.add(word)

with open("count_dict.json", "r") as f:
    freq_dict = json.load(f)
freq_dict = Counter(freq_dict)

# make set of top n words for quick lookup
top_words = set(x[0] for x in freq_dict.most_common(n_most_common))
print('picked most common')
intersection = top_words.intersection(obligatory_words_set)
print('got intersection')
top_words = set(x[0] for x in freq_dict.most_common(n_most_common - (len(obligatory_words_set) - len(intersection))))
print('again picked most common')
top_words = top_words.union(obligatory_words_set)
print('got union')
print(freq_dict.most_common(100)) # just to show the top 100 terms
#write vocab to file to compare with model vocab:
print(len(top_words))

with open ("vocab_dutch.txt", "w") as out:
    out.write("\n".join(top_words))

#print vocab size
print('Vocab Size: {}'.format(len(top_words)))
# now filter file to change all but most common words to '<unk>'
print('unking!')
with open(clean_sent_filename, 'r') as f, open(unked_filename, 'w') as out:
    for n, line in enumerate(f):
        tokens = word_tokenize(line.strip())
        unked = [w if w in top_words else '<unk>' for w in tokens]
        # write if not too many unks
        if unked.count('<unk>')/len(unked) <= 0.05:
            out.write((' '.join(unked)+'\n'))
        if n % 100000 == 0:
            print(n)
print('done unking!')
#count N of unique words in the final unked file:
with open("unked_dutch.txt", "r") as file:
    lines = file.read().splitlines()

    uniques = set()
    for line in lines:
        uniques |= set(line.split())

    print(f"Unique words: {len(uniques)}")
