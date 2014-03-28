#!/usr/bin/env bash
rm -rf output
hadoop jar wc.jar org.apache.hadoop.examples.WordCount output ln_pg100.txt 2.txt
