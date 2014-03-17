#!/usr/bin/env python
import os
import sys


if __name__ == '__main__':
    infile = None
    outfile = None
    line_no = 1

    # open our input file for preprocessing
    in_filename = sys.argv[1]
    try:
        infile = open(in_filename, 'r')
        outfile = open('ln_' + in_filename, 'w')

        for line in infile:
            outfile.write(str(line_no) + ' ' + line)
            line_no += 1

    except IOError as e:
        sys.exit('Error opening \'' + e.filename + '\': ' + e.strerror)
    finally:
        if infile:
            infile.close()
        if outfile:
            outfile.close()

    out_filename = "ln_" + in_filename
