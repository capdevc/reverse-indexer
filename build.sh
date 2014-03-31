#!/usr/bin/env bash
# super simple build script since this is a pain to repeat
rm -f wc.jar
mkdir wordcount_classes
javac -classpath $HADOOP_HOME/hadoop-core-1.2.1.jar:$HADOOP_HOME/lib/commons-cli-1.2.jar -d wordcount_classes WordCount.java && jar -cvf wc.jar -C wordcount_classes .
rm -rf wordcount_classes
rm -f ri.jar
# cp ~/IdeaProjects/hadoop_index/src/ReverseIndexer.java .
# cp ~/IdeaProjects/hadoop_index/src/LineRecWritable.java .
mkdir reverseindexer_classes
javac -classpath .:$HADOOP_HOME/hadoop-core-1.2.1.jar:$HADOOP_HOME/lib/commons-cli-1.2.jar -d reverseindexer_classes ReverseIndexer.java && jar -cvf ri.jar -C reverseindexer_classes .
rm -rf reverseindexer_classes
