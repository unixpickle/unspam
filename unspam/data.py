"""
Tools for using email data.
"""

from collections import Counter
import json
import os

import numpy as np

from .tokens import tokens


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
        pairs = sorted(list(self.token_counts()), key=lambda x: x[1])
        return [x[0] for x in pairs[:n]]

    def samples(self, words):
        inputs = []
        labels = [0.0] * len(self.spam.emails) + [1.0] * len(self.real.emails)
        for email in self.spam.emails + self.real.emails:
            toks = set(_email_tokens(email))
            in_vec = [1.0 if word in toks else 0.0 for word in words]
            inputs.append(in_vec)
        return np.array(inputs, dtype=np.float32), np.array(labels, dtype=np.float32)


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
