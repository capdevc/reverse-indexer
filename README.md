#Hadoop Reverse Indexer
Alexander Saites, Cristian Capdevila

### Description
This is a hadoop reverse index generator. It takes a set of text files, and generates an index file mapping words to documents, line numbers and positions in lines. Here is some example output from the complete works of Shakespeare: 

	abaissiez       pg100.txt,38892:4
	abandon	pg100.txt,12798:4,12796:1,107651:7,86190:3
	abandond        pg100.txt,99731:4,46394:4,112983:2,115315:4,13202:6,2880:3
	abandoned       pg100.txt,10971:2,108892:2
	abase   pg100.txt,42831:3,91749:4
	abashd  pg100.txt,111540:4
	abate   pg100.txt,95740:0,99606:2,75465:2,98497:0,80391:0,108095:5,...
	abated  pg100.txt,18035:2,32062:4,61172:2
	abatement       pg100.txt,60224:7,115047:3,23020:2
	abatements      pg100.txt,27527:2
	abates  pg100.txt,104389:0
	
This output is read as: the word `abaissiez` is word number `4` of line `38892` of document `pg100.txt`. Appearances in multiple lines are separated by commas, and multiple documents are separated by tabs.

Additionally, we have included a program to perform queries on the output document. For example, given this line from Macbeth:

	MACBETH. [Aside.] Time, thou anticipatest my dread exploits.

which occurs as line `68,521` in the complete works, file `pg100.txt`, we can have this query session:

	Enter your query: exploits
	searching for exploits
	  File: pg100.txt
	    On Line: 112677
	    On Line: 39946
	    On Line: 110336
	    On Line: 35743
	    On Line: 14607
	    On Line: 68521
	    On Line: 42743
	Enter your query: dread exploits
	searching for dread exploits
	  File: pg100.txt
	    On Line: 68521
	Enter your query: aside and dread
	searching for (AND dread aside)
	  File: pg100.txt
	    On Line: 68521

The query parser also understand OR, NOT and parenthesises expressions:

	Enter your query: high exploits
	searching for high exploits
	  File: pg100.txt
	    On Line: 110336
	Enter your query: exploits AND (NOT high)
	searching for (AND (NOT high) exploits)
	  File: pg100.txt
	    On Line: 112677
	    On Line: 39946
	    On Line: 35743
	    On Line: 14607
	    On Line: 68521
	    On Line: 42743
	Enter your query: exploits AND (NOT (high OR dread))
	searching for (AND (NOT (OR dread high)) exploits)
	  File: pg100.txt
	    On Line: 35743
	    On Line: 112677
	    On Line: 42743
	    On Line: 39946
	    On Line: 14607

### Included Files
  
  1. **WordCount.java** - A lightly modified version of the WordCount.java included with the hadoop examples. It has been changed to accept multiple input files, and to produce a word counts taken cumulatively over all inputs.
  2. **ReverseIndex.java** - A hadoop program that takes multiple files and generates an output file indexing each appearing word into its file, line number and line position. It takes a theshold for word appearances as an option. If provided, words appearing more often than this threshold number are considered stop words and left out of the output.
  3. **LineRecWritable.java** - A custom class implementing the writable interface used to pass word information from the hadoop mapper phase to the reduce phase. Mapper output is of the form (Text, LineRecWritable).
  4. **wordcount.py** - A python script wrapper around hadoop to automate running the WordCount.java program.
  5. **threshold.py** - A python script to generate a word count to pass to ReverseIndex.java to use as a stop word threshold. It takes an output file from WordCount.java and a word ranking, `n`. It generates a count such that the top `n` words appear more frequently. It also displays a list of the words that will be blocked.
  6. **number.py** - A python script that adds line numbers to a text file. ReverseIndexer.java requires line numbers in order to work properly.
  7. **reverseindex.py** - A python wrapper around around hadoop that executes the ReverseIndex.java program.
  8. **runall.py** - A python script that will run all items 1-7 as needed.
  9. **query.py** - A python program to query the ReverseIndex.java output file.
  10. **parsetree.py** - Part of the query.py script.

All of the python files except `parsetree.py` can be run as stand alone programs and accept a `-h` option to display help.

### Instructions

The easiest way to use everything is to first compile the java files and create jars. The script we have been using to do so looks like this (wrapped lines are shown as indentation):

	#!/usr/bin/env bash
	# super simple build script since this is a pain to repeat

	rm -f wc.jar
	mkdir wordcount_classes
	javac -classpath 
	   $HADOOP_HOME/hadoop-core-1.2.1.jar:$HADOOP_HOME/lib/commons-cli-1.2.jar 
	   -d wordcount_classes WordCount.java
	jar -cvf wc.jar -C 	wordcount_classes .
	rm -rf wordcount_classes
	
	rm -f ri.jar
	mkdir reverseindexer_classes
	javac -classpath 
	   .:$HADOOP_HOME/hadoop-core-1.2.1.jar:$HADOOP_HOME/lib/commons-cli-1.2.jar
	   -d reverseindexer_classes ReverseIndexer.java 
	jar -cvf ri.jar -C 	reverseindexer_classes .
	rm -rf reverseindexer_classes

This assumes you have `$HADOOP_HOME` set to the hadoop home directory, and that the java files are in the current directory.

Then, assuming you have hadoop installed and configured properly, you can just use `runall.py` to generate the index file:

	usage: runall.py [-h] [-r RI] [-w WC] [-p PATH] [-s STOP]
	                 outfile infile [infile ...]
	
	positional arguments:
	  outfile               Name of the output file
	  infile                Names of the text files to be numbered
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -r RI, --ri RI        Name of the indexer jar file (default: ri.jar)
	  -w WC, --wc WC        Name of the wordcount jar file (default: wc.jar)
	  -p PATH, --hadoop PATH
	                        Path to the hadoop binary (default: "")
	  -s STOP, --stop STOP  Drop the STOP most common words (default: 0)

Alternatively, one can run the entire pipeline manually, using the included python scripts to first, generate a word count file, then generate a stop word threshold from that word count file. Then, add line numbers to the input text files and run the reverse indexer. Again, all scripts accept `-h` for instructions on how to use them.

One you have the index file, you can pass it as an argument to the `query.py` script to run queries. Queries elements are be single words or multi-word phrases, and can be combined with AND, OR, and NOT. These expressions can then be parenthesized to generate more complex queries.

### Design Decisions

The main design decision we made was how to generate stop words. The options were to either generate a custom set of stop words for our particular application (the complete works of Shakespeare), or to use some generic method that might not be quite as good, but would make the program more generally useable. The first option would have been much easier, but we also felt that the point of the assignment was to work with hadoop, not to decide what words in a shakespeare text are or aren't important.

The way we generate stop words is very simple. We just accept some integer, n, sort the words by appearance frequency, and drop the 1st through n-th word. This doesn't really give you a great stop word list, but it will work with any text. It also necessitates another pass of the text through hadoop in order to generate the aggregate word counts. The sorting and selection is then really done in python (inside `threshold.py`). If this were a serious production or research tool, there are much better algorithms to use.