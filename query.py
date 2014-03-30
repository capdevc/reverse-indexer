from sys import argv

class QueryHandler:
    def __init__(self, filename):
        self.dic = {}
        with open(filename) as f:
            for line in f:
                entry = line.rstrip().split('\t')
                self.dic[entry[0]] = entry[1:]

    def getEntries(self,word):
        try:
            entries = {}
            for entry in self.dic[word]:
                info = entry.split(',')
                locs = {}
                for loc in info[1:]:
                    line,word = loc.split(':')
                    if line in locs:
                        locs[line].append(word)
                    else:
                        locs[line] = [word]
                entries[info[0]] = locs
            return entries        
        except: 
            return None 
    
    def printEntries(self,entries):
        for entry in entries:
            print "  File: {}".format(entry)
            for loc in entries[entry]:
                if len(entries[entry][loc]) == 1:
                    print "    Line: {}, Word {}"\
                        .format(loc, entries[entry][loc][0])
                else:
                    print "    Line: {}, Words {}"\
                        .format(loc, ','.join(entries[entry][loc]))
    
    def readQueries(self):
        while True:
            try:
                print "Enter your query:",
                query = raw_input().rstrip().lower()
            except:
                break

            entries = self.getEntries(query)
            if entries is None:
                print "  {} not found".format(query)
            else:
                self.printEntries(entries)

    def parsePhrase(self, phrase):
        '''returns a list of tuples of the form (filename, linenum, startword)
        where the entire phrase appears, in order, starting at startword in 
        line linenum in file filename'''
        words = phrase.split()
        entries = [self.getEntries(word) for word in words]
        [self.printEntries(e) for e in entries]
        filelist = entries[0].keys()
        phraseStarts = []
        for i in range(1,len(entries)):
            filelist = [fn for fn in filelist if fn in entries[i].keys()]
        for fn in filelist:
            lines = entries[0][fn].keys()
            for i in range(1,len(words)):
                lines = [l for l in lines if l in entries[i][fn].keys()]
            for l in lines:
                for num in entries[0][fn][l]:
                    start = int(num)
                    phraseFound = True
                    for i in range(1,len(words)):
                        if str(start + i) not in entries[i][fn][l]:
                            phraseFound = False
                            break
                    if phraseFound:
                        phraseStarts.append((fn, l, start))
        return phraseStarts

if __name__ == '__main__':
    try:
        filename = argv[1]
    except:
        print "use: python query.py indexfile.txt"
        exit()
    qh = QueryHandler(filename)
#    qh.readQueries()
    print qh.parsePhrase('casing cask')

