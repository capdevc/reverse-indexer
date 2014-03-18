#!/usr/bin/env bash
rm -rf output
cp ~/IdeaProjects/hadoop_index/src/ReverseIndexer.java .
./build.sh
hadoop jar ri.jar ReverseIndexer ln_pg100.txt output
