#!/usr/bin/env bash
# super simple build script since this is a pain to repeat
rm -f ri.jar
mkdir reverseindexer_classes
javac -classpath $HADOOP_HOME/hadoop-core-1.2.1.jar:$HADOOP_HOME/lib/commons-cli-1.2.jar -d reverseindexer_classes ReverseIndexer.java && jar -cvf ri.jar -C reverseindexer_classes .
rm -rf reverseindexer_classes
