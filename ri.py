#!/usr/bin/env python
import sys
import argparse
import ntpath
import subprocess as sp
from tempfile import NamedTemporaryFile


def subp_cmd(cmd, err_msg):
    p = sp.Popen(cmd, shell=True, stderr=sp.PIPE)
    p.wait()
    if p.returncode is not 0:
        print(err_msg)
        for line in p.stderr:
            print(line)
        sys.exit(1)


def preprocess(infile, prefile):
    line_no = 1
    for line in infile:
        prefile.write(str(line_no) + ' ' + line)
        line_no += 1


def run(args, infile):
    infilename = ntpath.basename(infile.name)
    outfile = args.outfile
    hdfs_home = args.hdfs_home
    jar = args.jar

    # copy the new file to the hdfs file system
    subp_cmd('hadoop fs -put {} {}'.format(infile.name, hdfs_home),
             'An error occurred copying the input file to hdfs.\n')

    # make sure that works
    #subp_cmd('hadoop fs -test -e {}/{}'.format(hdfs_home, infile),
             #'An error occurred copying the input file to hdfs.\n')

    # run the jar file
    subp_cmd('hadoop jar {} ReverseIndexer {}/{} {}/output'.format(jar, hdfs_home, infilename, hdfs_home),
             'An error occurred running the hadoop job:\n')

    # copy the output files
    subp_cmd('hadoop fs -get {}/output/part-r-00000 {}'.format(hdfs_home, outfile),
             'An error occurred retrieving the output from the hdfs:\n')

    # erase the input file from the hdfs system
    subp_cmd('hadoop fs -rm {}/{}'.format(hdfs_home, infilename),
             'An error occurred rming temp file from the hdfs filesystem:\n')

    # erase the output files from the hdfs system
    subp_cmd('hadoop fs -rmr {}/output'.format(hdfs_home),
             'An error occurred rming output file from the hdfs filesystem:\n')


if __name__ == '__main__':
    # Do some command line parsing
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    # the pre subcommand will just preprocess the file and save a copy
    parser_pre = subparsers.add_parser('pre', help='Number the lines in the input file and save')
    parser_pre.add_argument('infile', help='Name of the text file to be processed')
    parser_pre.add_argument('outfile', help='Name of the output file')
    parser_pre.set_defaults(nopre=False)
    # the run subcommand will do the whole run, including launching hadoop
    parser_run = subparsers.add_parser('run', help='Preprocess a text file and launch hadoop reverse indexer')
    parser_run.add_argument('infile', help='Name of the text file to be processed')
    parser_run.add_argument('outfile', help='Name of the output file')
    parser_run.add_argument('hdfs_home', help='Path to hdfs home')
    parser_run.add_argument('jar', nargs='?', default='ri.jar',
                            help='Name of the jar file (default: %(default)s)')
    parser_run.add_argument('-n', '--nopre', action='store_true',
                            help="Don't preprocess the input file")
    args = parser.parse_args()

    # open files
    try:
        infile = open(args.infile, 'r')
        prefile = None
        if not args.nopre:
            prefile = open(args.outfile, 'w') if args.subcommand == 'pre' else NamedTemporaryFile(mode='w')
            preprocess(infile, prefile)
        else:
            prefile = infile

        if args.subcommand == 'run':
            run(args, prefile)

    except IOError as e:
        sys.exit('Error opening \'' + e.filename + '\': ' + e.strerror)

    finally:
        if infile:
            infile.close()
        if prefile:
            prefile.close()
