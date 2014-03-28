#!/usr/bin/env bash
rm -rf output
hadoop jar ri.jar ReverseIndexer output ln_pg100.txt 2.txt
