from sys import argv

dic = {}

def getEntries(word):
    try:
        entries = {}
        for entry in dic[word]:
            info = entry.split(',')
            locs = {}
            for loc in info[1:]:
                line,word = loc.split(':')
                locs[line] = word
            entries[info[0]] = locs
        return entries        
    except: 
        return None 
    
def printEntries(entries):
    for entry in entries:
        print "  File: {}".format(entry)
        for loc in entries[entry]:
            print "    Line: {}, Word {}".format(loc, entries[entry][loc])
    

if __name__ == '__main__':
    try:
        filename = argv[1]
    except:
        print "use: python query.py indexfile.txt"
        exit()

    with open(filename) as f:
        for line in f:
            entry = line.rstrip().split('\t')
            dic[entry[0]] = entry[1:]

    while True:
        try:
            print "Enter your query:",
            query = raw_input().rstrip().lower()
        except:
            break
        entries = getEntries(query)
        if entries is None:
            print "  {} not found".format(query)
        else:
            printEntries(entries)
