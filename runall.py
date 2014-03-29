#!/usr/bin/env python
import os
import shutil
import argparse
import uuid
from ntpath import basename
from tempfile import mkdtemp
from threshold import threshold
from wordcount import wordcount
from number import number
from reverseindex import reverseindex


if __name__ == '__main__':
    # Do some command line parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', help='Name of the output file')
    parser.add_argument('infile', nargs='+',
                        help='Names of the text files to be numbered')
    parser.add_argument('-r', '--ri', default='ri.jar',
                        help='Name of the indexer jar file (default: %(default)s)')
    parser.add_argument('-w', '--wc', default='wc.jar',
                        help='Name of the wordcount jar file (default: %(default)s)')
    parser.add_argument('-p', '--hadoop', default=None, metavar='PATH',
                        help='Path to the hadoop binary (default: "")')
    parser.add_argument('-s', '--stop', type=int, default=0,
                        help='Drop the STOP most common words (default: 0)')
    args = parser.parse_args()

    wc_filename = 'wc' + str(uuid.uuid4())

    wordcount(args.infile, wc_filename, args.wc, args.hadoop)

    thresh = 0
    with open(wc_filename, 'r') as wc_file:
        _, thresh = threshold(args.stop, wc_file)
    os.remove(wc_file)

    ln_infile = []
    tdir = mkdtemp()
    for filename in args.infile:
        ofilename = tdir + basename(filename)
        ln_infile.append(ofilename)
        with open(filename, 'r') as i, open(ofilename, 'w') as o:
            number(i, o)

    reverseindex(ln_infile, args.outfile, args.ri, thresh, args.hadoop)

    shutil.rmtree(tdir)
