# Derived from Peter Norvig

import argparse
import string
import json
from collections import Counter
import re

WORDS = Counter(re.findall(r'\w+', open('./app/dict.txt', 'r').read().lower()))
TOTAL = sum(WORDS.values())


def generate(query):
    # Will build up to ld = 3 strings
    possible = {query: 0}  # Maps string to ld metric

    for ld in range(2):
        for w in [y for y in possible if possible[y] == ld]:
            for x in string.lowercase:
                # Add to end (part of insert case)
                possible[w + x] = ld + 1
                for pos in range(len(w)):
                    # Substitution
                    subs = w[:pos] + x + w[pos + 1:]
                    if subs not in possible:
                        possible[subs] = ld + 1

                    # Insertion
                    insert = w[:pos] + x + w[pos:]
                    if insert not in possible:
                        possible[insert] = ld + 1

                    # Deletion
                    delete = w[:pos] + w[pos + 1:]
                    if delete not in possible:
                        possible[delete] = ld + 1

    # Return only valid words & their probabilities

    return {k: 1.0 / float(possible[k]) * float(WORDS[k]) / float(TOTAL) for k in possible if k in WORDS and possible[k] != 0}

def check(string_input):
    # Spell check the input
    tokens = re.findall(r'\w+', string_input.lower())
    corrections = []
    for tk in tokens:
        if tk not in WORDS:
            candidates = generate(tk)
            max_prob = max(candidates.values())
            keys = [k for k in candidates if candidates[k] == max_prob]
            corrections += keys
    return 'Did you mean: ' + str(corrections) + '?'