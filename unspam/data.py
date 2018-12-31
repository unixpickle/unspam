"""
Tools for using email data.
"""

from collections import Counter
import json
import os

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