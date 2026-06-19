import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
S -> NP VP Conj S

NP -> N
NP -> Det N
NP -> Det Adj N
NP -> Det Adj Adj N
NP -> Det Adj Adj Adj N
NP -> Adj N
NP -> NP PP
NP -> NP Adv

VP -> V
VP -> V NP
VP -> V PP
VP -> V Adv
VP -> V NP PP
VP -> V PP PP
VP -> V NP PP PP
VP -> V Adv PP
VP -> V Adv NP
VP -> V Adv NP PP
VP -> VP Conj VP

PP -> P NP
PP -> P Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
        print(trees)
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    
    sentence = sentence.lower().rstrip()
    words = nltk.tokenize.word_tokenize(sentence)
    
    i = 0
    while i < len(words):
        if any(c.isalpha() for c in words[i]):
            i += 1
        else:
            words.pop(i)
    
    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []

    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            # Get all NP's descendants *excluding* itself
            descendants = list(subtree.subtrees())[1:]

            # Check if any of those descendants is also an NP
            has_nested_np = any(child.label() == "NP" for child in descendants)

            # If it has no nested NP, it's a chunk
            if not has_nested_np:
                chunks.append(subtree)

    return chunks


if __name__ == "__main__":
    main()