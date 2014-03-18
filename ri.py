#!/usr/bin/env python
import sys
import subprocess as sp


def usage():
    message = 'Usage: ' + sys.argv[0] + ' <input file> <output file> <hdfs home>\n' + \
              '     input file    : Name of the text file to be indexed\n' + \
              '     output file   : Name of the output file to contain the index\n' + \
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
        return outfile.name

    except IOError as e:
        sys.exit('Error opening \'' + e.filename + '\': ' + e.strerror)

    finally:
        if infile:
            infile.close()
        if outfile:
            outfile.close()


def subp_cmd(cmd, err_msg):
    p = sp.Popen(cmd, shell=True, stderr=sp.PIPE)
    p.wait()
    if p.returncode is not 0:
        print(err_msg)
        for line in p.stderr:
            print(line)
        sys.exit(1)


if __name__ == '__main__':
    # print usage information/check arg count
    argc = len(sys.argv)
    if argc is not 4:
        usage()
        if argc is 1:
            sys.exit(0)
        else:
            sys.exit(1)

    hdfs_home = sys.argv[3]
    outfile = sys.argv[2]
    # create a new file with line numbers
    datafile = file_number(sys.argv[1])

    # copy the new file to the hdfs file system
    subp_cmd('hadoop fs -put ' + datafile + ' ' + hdfs_home,
             "An error occurred copying the input file to hdfs.\n")

    # run the jar file
    subp_cmd('hadoop jar blah',
             'An error occurred running the hadoop job:\n')

    # copy the output files
    subp_cmd('hadoop fs -get ', + hdfs_home + '/output/part-r-00000 ' + outfile,
             'An error occurred running the hadoop job:\n')

    # erase the input file from the hdfs system
    subp_cmd('hadoop fs -rm ' + hdfs_home + '/' + datafile,
             'An error occurred rming temp file from the hdfs filesystem:\n')

    # erase the output files from the hdfs system
    subp_cmd('hadoop fs -rmr ' + hdfs_home + '/output',
             'An error occurred rming temp file from the hdfs filesystem:\n')
