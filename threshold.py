#!/usr/bin/env python
import argparse
import operator


# build a list of word counts, then sort it
def build_counts(wcfile):
    counts = []
    wcfile.seek(0)
    for line in wcfile:
        tokens = line.split('\t')
        counts.append(int(tokens[1]))
    counts.sort(reverse=True)
    return counts


# calculate a threshold of counts for the nth word
def threshold(num_words, wcfile):
    counts = build_counts(wcfile)
    return counts[num_words - 1]


if __name__ == '__main__':
    # Do some command line parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='Name of the text file to be processed')
    parser.add_argument('num_words', type=int, help='number of words to drop')
    args = parser.parse_args()

    # build stop word list and print it with threshold
    with open(args.infile) as infile:
        stopwords = {}
        thresh = threshold(args.num_words, infile)
        infile.seek(0)
        for line in infile:
            word, count = line.strip('\n').split('\t')
            if int(count) >= thresh:
                stopwords[word] = int(count)
        for item in sorted(stopwords.iteritems(), key=operator.itemgetter(1),
                           reverse=True):
            print(item)
        print('Count threshold: {}'.format(thresh))
