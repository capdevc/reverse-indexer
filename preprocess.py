#!/usr/bin/env python
import argparse


def preprocess(infile, outfile):
    line_no = 1
    for line in infile:
        outfile.write(str(line_no) + ' ' + line)
        line_no += 1


if __name__ == '__main__':
    # Do some command line parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='Name of the text file to be numbered')
    parser.add_argument('outfile', help='Name of the output file')
    args = parser.parse_args()

    with open(args.infile) as infile, open(args.outfile, 'w') as outfile:
        preprocess(infile, outfile)
