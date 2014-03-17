#!/usr/bin/env python
#import os
import sys


def usage():
    message = 'Usage: ' + sys.argv[0] + ' <input file> <hdfs home>\n' + \
              '     input file    : Name of the text file to be indexed\n' + \
              '     hdfs home     : Path your HDFS home directory'
    print(message)


def file_number(in_filename):
    outfile = None
    infile = None
    line_no = 1
    try:
        # open our input file and output file
        infile = open(in_filename, 'r')
        outfile = open('ln_' + in_filename, 'w')

        # copy the file over, but prepending line numbers, starting at 1
        for line in infile:
            outfile.write(str(line_no) + ' ' + line)
            line_no += 1

        return outfile

    except IOError as e:
        sys.exit('Error opening \'' + e.filename + '\': ' + e.strerror)
    finally:
        if infile:
            infile.close()
        if outfile:
            outfile.close()


if __name__ == '__main__':
    # print usage information/check arg count
    argc = len(sys.argv)
    if argc is not 3:
        usage()
        if argc is 1:
            sys.exit(0)
        else:
            sys.exit(1)

    # create a new file with line numbers
    datafile = file_number(sys.argv[1])
