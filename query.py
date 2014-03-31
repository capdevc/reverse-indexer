#!/usr/bin/env python
from sys import argv
from parsetree import *
import re
import argparse

class QueryHandler:
    def __init__(self, filename):
        self.dic = {}
        with open(filename) as f:
            for line in f:
                entry = line.rstrip().split('\t')
                self.dic[entry[0]] = entry[1:]

    def getEntries(self, word):
        entries = {}
        try:
            for entry in self.dic[word]:
                info = entry.split(',')
                locs = {}
                for loc in info[1:]:
                    line, word = loc.split(':')
                    if line in locs:
                        locs[line].append(word)
                    else:
                        locs[line] = [word]
                entries[info[0]] = locs
        except:
            pass
        return entries        
    
    def printEntries(self,entries):
        if not entries:
            print "  No entries"
        for entry in entries:
            print "  File: {}".format(entry)
            for loc in entries[entry]:
                print "    On Line: {}"\
                    .format(loc, entries[entry][loc])
    
    def readQueries(self):
        while True:
            try:
                print "Enter your query:",
                query = raw_input().rstrip().lower()
                query = re.sub(r'\band\b', 'AND', query)
                query = re.sub(r'\bnot\b', 'NOT', query)
                query = re.sub(r'\bor\b',  'OR',  query)
                pt = buildParseTree(query)
                print "searching for {}".format(str(pt))
                self.printEntries(self.parseTree(pt))
            except (MismatchedParensError, InvalidQueryError) as e:
                print "  " + str(e)
                continue
            except EOFError:
                break

    def parseTree(self,node):
        if isinstance(node,str):
            return self.parsePhrase(node)
        else:   
            entries = [self.parseTree(c) for c in node.children]
            locs = {}
            if node.isAnd():
                filelist = self.getCommonFiles(entries)
                for fn in filelist:
                    lines = self.getCommonLines(entries, fn)
                    for l in lines:
                        if fn not in locs:
                            locs[fn] = {}
                        locs[fn][l] = [-1]
            elif node.isOr():
                for e in entries:
                    for fn in e.keys():
                        for l in e[fn]:
                            if fn not in locs:
                                locs[fn] = {}
                            locs[fn][l] = [-1]
            elif node.isNot():
                entries = entries[0]
                universe = [self.getEntries(w) for w in self.dic.keys()]
                for e in universe:
                    for fn in e.keys():
                        if fn in entries.keys():
                            for l in e[fn]:
                                if l not in entries[fn]:
                                    if fn not in locs:
                                        locs[fn] = {}
                                    locs[fn][l] = [-1]
                        else:
                            for l in e[fn]:
                                if fn not in locs:
                                    locs[fn] = {}
                                locs[fn][l] = [-1]
            return locs
            
                
    def getCommonFiles(self, entryList):
        filelist = entryList[0].keys()
        for i in range(1,len(entryList)):
            filelist = [fn for fn in filelist if fn in entryList[i].keys()]
        return filelist

    def getCommonLines(self, entryList, fn):
        lines = []
        lines = entryList[0][fn].keys()
        for i in range(1,len(entryList)):
            lines = [l for l in lines if l in entryList[i][fn].keys()]
        return lines

    def parsePhrase(self, phrase):
        '''returns a list of tuples of the form (filename, linenum, startword)
        where the entire phrase appears, in order, starting at startword in
        line linenum in file filename'''
        phraseStarts = {}
        words = phrase.split()
        entries = [self.getEntries(word) for word in words]
        filelist = self.getCommonFiles(entries)
        for fn in filelist:
            lines = self.getCommonLines(entries, fn)
            for l in lines:
                for num in entries[0][fn][l]:
                    start = int(num)
                    phraseFound = True
                    for i in range(1, len(words)):
                        if str(start + i) not in entries[i][fn][l]:
                            phraseFound = False
                            break
                    if phraseFound:
                        if fn not in phraseStarts:
                            phraseStarts[fn] = {} 
                        if l not in phraseStarts[fn]:
                            phraseStarts[fn][l] = []
                        phraseStarts[fn][l].append(str(start))
        return phraseStarts

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('index_file', help='Index file to be queried')
    args = parser.parse_args()

    # run query
    qh = QueryHandler(args.index_file)
    qh.readQueries()
