"""
Tools for using email data.
"""

from collections import Counter
import json
import os

import numpy as np
import torch

from .tokens import tokens


def email_vector(words, email):
    """
    Convert an email to a vector.

    Args:
      words: a list of words.
      email: the email dict.

    Returns:
      A list of floats.
    """
    word2index = {w: i for i, w in enumerate(words)}
    vec = [0.0] * (len(words) + 1)
    for tok in _email_tokens(email):
        if tok in word2index:
            vec[word2index[tok] + 1] += 1.0
        else:
            vec[0] += 1.0
    return vec


class Dataset:
    """
    A dataset for training a spam filter.
    """

    def __init__(self, spam_folder, real_folder):
        self.spam = EmailSet(spam_folder)
        self.real = EmailSet(real_folder)

    def token_counts(self):
        res = self.spam.token_counts()
        res.update(self.real.token_counts())
        return res

    def top_words(self, n=2000):
        pairs = sorted(list(self.token_counts().items()), key=lambda x: x[1], reverse=True)
        return [x[0] for x in pairs[:n]]

    def samples(self, words, train=True, test=True):
        assert train or test, 'no dataset selected'
        inputs = []
        labels = [0.0] * len(self.spam.emails) + [1.0] * len(self.real.emails)
        for email in self.spam.emails + self.real.emails:
            inputs.append(email_vector(words, email))
        if train != test:
            inputs = [x for i, x in enumerate(inputs) if (i % 4 != 0) == train]
            labels = [x for i, x in enumerate(labels) if (i % 4 != 0) == train]
        return (torch.from_numpy(np.array(inputs, dtype=np.float32)),
                torch.from_numpy(np.array(labels, dtype=np.float32)))


class EmailSet:
    """
    A collection of emails.
    """

    def __init__(self, dir_path):
        self.emails = []
        listing = [f for f in os.listdir(dir_path) if f.endswith('.json')]
        for filename in listing:
            with open(os.path.join(dir_path, filename), 'r') as f:
                self.emails.append(json.load(f))

    def token_counts(self):
        counter = Counter()
        for email in self.emails:
            for token in _email_tokens(email):
                counter[token] += 1
        return counter


def _email_tokens(email):
    return tokens(email['subject'] + ' ' + email['body'])
