"""
Utilities for dealing with text.
"""

import re


def tokens(s):
    """
    Extract the set of tokens in a piece of text.
    """
    s = s.lower()
    s = _replace_urls(s)
    s = _replace_unicode(s)
    s = _replace_punctuation(s)
    return s.split()


def _replace_urls(s):
    return re.sub('https?://[^\\s]*', ' URL ', s)


def _replace_unicode(s):
    s = s.replace("“", "\"")
    s = s.replace("“", "\"")
    s = s.replace("“", "\"")
    s = s.replace("”", "\"")
    s = s.replace("‘", "'")
    s = s.replace("’", "'")
    s = s.replace("–", "-")
    s = s.replace("—", "-")
    s = s.replace("…", "...")

    # No-break space.
    s = s.replace(" ", " ")

    # Punctuation space.
    s = s.replace(" ", " ")

    # Zero-width space.
    s = s.replace("​", "")

    return s


def _replace_punctuation(s):
    return re.sub('("|\'|\\?|;|:|,|\\.|!|\\(|\\)|/|<|>|-|\\+|\\[|\\]|\\$|\\&)', ' ', s)
