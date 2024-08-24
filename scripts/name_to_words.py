"""
name to words: Takes in a name and returns a list of words in the name base off the characters
available in the name. Skips all words that I don't think should be considered.

Assumes all characters to be lower case.

# Charlie
# example: ['car']
"""

import string
from english_words import get_english_words_set
from typing import Optional
from collections import Counter
from functools import lru_cache

@lru_cache
def get_all_english_words_that_i_think_might_be_words() -> list[str]:
    starting_words = get_english_words_set(sources=['gcide'], lower=True)

    words = set()

    for w in starting_words:
        skip = False
        if len(w) == 1:
            skip = True

        for c in w:
            if c not in string.ascii_lowercase:
                skip = True

        if not skip:
            words.add(w)

    return sorted(words)

def can_make_word_from_name(word: str, name: str) -> Optional[Counter]:
    """
    If this returns None, we can't make the word from the name
    Otherwise returns a counter of remaining available characters from the name.
    """
    if len(word) > len(name):
        return False

    name_counter = Counter(name)

    for c in word:
        name_counter[c] -= 1
        if name_counter[c] < 0:
            return None

    return name_counter

def name_to_words_with_counter(name: str) -> list[tuple[str, Counter]]:
    name = name.lower()
    words = get_all_english_words_that_i_think_might_be_words()

    ret = []
    for word in words:
        if counter := can_make_word_from_name(word, name):
            ret.append((word, counter))

    return ret

def name_to_words(name: str) -> list[str]:
    return [a[0] for a in name_to_words_with_counter(name)]

def name_to_multi_words(name: str) -> list[str]:
    name = name.lower()
    ret = name_to_words_with_counter(name)

    while True:
        was_changed = False
        for idx, (word, counter) in enumerate(ret):
            leftovers = ''.join(counter.elements())
            if len(leftovers) > 1:
                for found, leftover_counter in name_to_words_with_counter(leftovers):
                    ret[idx] = tuple([word + ' ' + found, leftover_counter])
                    was_changed = True

        if not was_changed:
            break

    return [a[0] for a in ret]

def get_longest_n_words_from_name(name: str, n: int = 1) -> list[str]:
    """ Won't return name itself """
    words = name_to_words(name)

    try:
        words.remove(name)
    except ValueError:
        pass

    if words:
        return sorted(words, key = lambda x: len(x), reverse=True)[:n]
