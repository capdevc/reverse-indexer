import re

RIGHTASS = ['AND', 'OR']
LEFTASS = ['NOT']
MODIFIERS = ['AND', 'OR', 'NOT']
PRECEDENCE = dict(zip(MODIFIERS,[2,1,3]))
RESERVE = ['(', ')'] + MODIFIERS
class ParseTree:
    '''container for parse trees for AND/OR/NOT'''
    def __init__(self, mod, children=None):
        self.children = children
        self.mod = mod

    def isNot(self):
        return self.mod == 'NOT'
    def isAnd(self):
        return self.mod == 'AND'
    def isOr(self):
        return self.mod == 'OR'

    def __str__(self):
        if self.children:
            chstr = ' '.join([c.__str__() for c in self.children])
            return "("+self.mod+" "+chstr+")"
        else:
            return "("+self.mod+")"

def tokenize(query):
    #split parens and split whitespace
    tokens = [t for t in re.split('(\W)', query) if t.split()]

    #recombine split words that aren't reserved
    i = 0; j = len(tokens)
    while i < j-1:
        if tokens[i] not in RESERVE and tokens[i+1] not in RESERVE:
            if tokens[i][-1] != '-' and tokens[i+1] != '-':
                tokens[i] += ' ' + tokens[i+1]
            else:
                tokens[i] += tokens[i+1]
            del tokens[i+1]
            i -= 1; j -= 1
        i += 1
    return tokens

class MismatchedParensError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "mismatched parentheses"

class InvalidQueryError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "your query cannot be parsed"

def popop(opstack, argstack):
    try:
        operator = opstack.pop()
        if operator == 'AND' or operator == 'OR':
            p = ParseTree(operator, children = [argstack.pop(), argstack.pop()])
        elif operator == 'NOT':
            p = ParseTree(operator, children=[argstack.pop()])
        else:
            assert(False)
    except:
        raise InvalidQueryError()
    argstack.append(p)

def buildParseTree(query):
    '''using the Shunting-Yard Algorithm'''
    #initialize
    opstack = []
    argstack = []
    tokens = tokenize(query)
    foundNot = False #foundNot is used to make sure NOT is uniary/right-ass.

    for t in tokens:
        if t not in RESERVE:
            foundNot = False
            argstack.append(t)

        elif t in MODIFIERS:
            if foundNot:
                raise InvalidQueryError()
            elif t == 'NOT':
                foundNot = True

            while opstack and (opstack[-1] in MODIFIERS) and (\
                (t in LEFTASS and PRECEDENCE[t] == PRECEDENCE[opstack[-1]]) or\
                PRECEDENCE[t] < PRECEDENCE[opstack[-1]]):
                    popop(opstack, argstack)
            opstack.append(t)

        elif t == '(':
            opstack.append(t)
        elif t == ')':
            while opstack and opstack[-1] != '(':
                popop(opstack, argstack)
            try:
                opstack.pop()
            except:
                raise InvalidQueryError()

        else:
            assert(False)

    #unwind the stack
    while opstack:
        if opstack[-1] in ['(', ')']:
            raise MismatchedParensError()
        popop(opstack, argstack)

    #stack should be single tree
    if len(argstack) != 1:
        raise InvalidQueryError()

    return argstack[0]
