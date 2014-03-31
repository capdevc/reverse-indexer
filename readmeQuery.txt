The query system reads in a index file and allows the user to search through
the index for the lines on which certain words or phrases appear. To do so,
run 

    >> python query.py indexfile.txt

You will then be presented with a prompt asking you to enter a query. The 
script will search the index for files and lines where that word or phrase 
appears. It then prints those files and line numbers to the screen.


Search Options:
    
    --Single Word--
    If you search for a single word, the script returns locations where that
    word appears.

    --Multi-word Phrase--
    If you search for multiple words seperated by spaces, the script returns
    files and lines where those words appear, in order, on that line.

    --Modifiers--
    You may use 'and', 'or', or 'not' to modify your query. When you do so, the
    program will show how your query is parsed, in prefix notation. For
    instance, "word1 and word2" is parsed as "(AND word1 word2)".

        --AND--
        The AND modifier returns locations where the arguments on the left and
        the arguments on the right are found in the same file on the same line.
        This is less strict the phrase searching, which requires the words to
        appear consecutively in order. The arguments on the left and right can
        be phrases, if so desired, in which case the individual phrases stil
        must appear consecutively in order, but the two phrases together simply
        must appear on the same line, not necessarily consecutively or in order.
        
        For instance, if the following line appeared in the text:
        
            "The quick brown fox jumped over the lazy dog."

        and you searched for "lazy dog and brown fox", it would be interpreted
        as "(AND 'lazy dog' 'brown fox')", and it would return the above line.
        However, "lazy dog and quick fox" would not return that line, since
        the words "quick fox" do not appear consecutively.

        --OR--
        The OR modifier returns locations where either the left or right
        argument (or both) appear. In the above example, "quick or slow" would
        return the above line.

        --NOT--
        The NOT modifier returns all locations in the corpus where the argument
        does not appear. This is most useful in conjunction with the other
        operators. For instance, you could search "quick and not brown", and
        the line above would not be returned, since "brown" is in the line.

        Note that since NOT operates in terms of the entire corpus, so it can
        return a large amount of data; most of the time, this is not bad, but if
        you used, for instance "not word1 and not word2", it will be interpreted
        as (AND (NOT word1) (NOT word2)), which will require "anding" a large
        number of entries. Instead, I recommend using "not (word1 and word2)",
        which will give the same results, but operate much faster, since the 
        AND operation will only be required to process a small amount of data.

    --Parentheses--
    You can also group your arguments by using parentheses. For instance, the 
    query 
        word1 and not word2 and word3 
    will be interpreted as 
        (AND (AND word3 (NOT word2)) word1). 
    But, if grouped as 
        word1 and not (word2 and word3),
    it would instead be processed as 
        (AND (NOT (AND word3 word2)) word1).

    For the most part, the interpreter attempts to verify that your query makes
    sense, but you can do some weird things with parentheses if you mistype and
    the interperter will try to make some sense of it.

    For instance, 
        word1 (and word2)
    is interpreted as
        (AND word1 word2),
    even though it is not a valid query. 

    As such, the script reports how it interpreted your query, and it reports if
    it failed to understand your query.

    For instance, 
        word1 not and word2
    reports:
        "your query cannot be parsed"
    since "not and" cannot be interpreted.
