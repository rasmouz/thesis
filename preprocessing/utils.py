from numpy.random import binomial

def create_mixed_corpus(first_language, second_language, output, bias_towards_english, size):

    count = 0
    outf = open(output,"w")
    with open(first_language,'rt') as e, open(second_language, 'rt') as d:
        for english_sent, dutch_sent in zip(e, d):
            if binomial(1,bias_towards_english):
                outf.write(english_sent)
            else:
                outf.write(dutch_sent)
            count += 1
            if count%100000==0:
                print(count)
            if count > size:
                break
    outf.close()
english = "corpora/english/"
dutch = "corpora/dutch/"
create_mixed_corpus(english + "train.txt", dutch + "train.txt", "train.txt", 0.5, 1622969)

english = "/Users/rasmouz/Documents/Thesis/corpora/new_english/"
dutch = "/Users/rasmouz/Documents/Thesis/corpora/dutch_mono/"
def corpus_stats(file):
    sentences = 0
    words = 0
    with open(file) as d:
        for line in d:
            sentences += 1
            words += len(line.split())
    print("sentences: {:5.0f}, words: {:5.0f}, words/sentence: {:5.2f}".format(sentences, words, words/sentences))
corpus_stats(dutch + "valid.txt")
corpus_stats(english + "train.txt")

def create_ungram(input_, output_):
    ungram = open(output_, "w")
    with open(input_) as f:
        for line in f:
            modify=" ".join([word for word in line.split() if word[0]!='['])
            #print(modify)
            ungram.write(modify+'\n')
    ungram.close()
dutch = "grammaticality_texts/dutch_test.txt"
english = "grammaticality_texts/english_test.txt"
create_ungram(dutch, "dutch_ungram.txt")
create_ungram(english, "english_ungram.txt")

def create_gram(input_, output_):
    gram = open(output_, "w")
    with open(input_) as f:
        for line in f:
            pre = []
            for word in line.split():
                if word[0]!='[':
                    pre.append(word)
                else:
                    pre.append(word[1:-1])
            modify=" ".join(pre)
            #print(modify)
            gram.write(modify+'\n')
    gram.close()
dutch = "grammaticality_texts/dutch_test.txt"
english = "grammaticality_texts/english_test.txt"
create_ungram(dutch, "dutch_gram.txt")
create_ungram(english, "english_gram.txt")
