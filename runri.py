#!/usr/bin/env python
import sys
import argparse
import subprocess as sp


def subp_cmd(cmd, err_msg):
    p = sp.Popen(cmd, shell=True, stderr=sp.PIPE)
    p.wait()
    if p.returncode is not 0:
        print(err_msg)
        for line in p.stderr:
            print(line)
        sys.exit(1)


def runri(infiles, outfile, hdfs_home, jar, threshold, hadoop_path):
    # add the hadoop path if needed
    hadoop_cmd = 'hadoop '
    if hadoop_path:
        hadoop_cmd = '{}/hadoop'.format(hadoop_path)

    infstr = ' '.join(infiles)
    # build a string of inputfiles + hdfs path
    hdfs_infstr = ''
    for infile in infiles:
        infstr += ' {}/{}'.format(hdfs_home, infile)

    subp_cmd('{} fs -put {} {}'.format(hadoop_cmd, infstr, hdfs_home),
             'An error occurred copying the input files to hdfs.\n')

    # run the jar file
    cmd = '{} jar {} ReverseIndexer'.format(hadoop_cmd, jar)
    if threshold != 0:
        cmd += ' -D threshold={}'.format(threshold)
    cmd += ' {}/output {}'.format(hdfs_home, hdfs_infstr)
    subp_cmd(cmd, 'An error occurred running the hadoop job:\n')

    # copy the output files
    subp_cmd('{} fs -get {}/output/part-r-00000 {}'.format(hadoop_cmd, hdfs_home, outfile),
             'An error ocurred retrieving output file from hdfs')

    # erase the input file from the hdfs system
    subp_cmd('{} fs -rm {}'.format(hadoop_cmd, hdfs_infstr),
             'An error occurred rming temp file from the hdfs filesystem:\n')

    # erase the output files from the hdfs system
    subp_cmd('{} fs -rmr {}/output'.format(hadoop_cmd, hdfs_home),
             'An error occurred rming output file from the hdfs filesystem:\n')



if __name__ == '__main__':
    # Do some command line parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('hdfs_home', help='Path to hdfs home')
    parser.add_argument('outfile', help='Name of the output file')
    parser.add_argument('infile', nargs='+',
                        help='Names of the text files to be numbered')
    parser.add_argument('-j', '--jar', default='ri.jar',
                        help='Name of the jar file (default: %(default)s)')
    parser.add_argument('-p', '--hadoop', default=None, metavar='PATH',
                        help='Path to the hadoop binary (default: "")')
    parser.add_argument('-t', '--threshold', type=int, default=0,
                        help='Maximum appearances before a word is considered a stop word')
    args = parser.parse_args()

    runri(args.infile, args.outfile, args.hdfs_home, args.jar, args.threshold, args.hadoop)
