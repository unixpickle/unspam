"""
Train a classifier.
"""

import itertools
import sys

import torch.nn as nn
import torch.optim as optim

from unspam.data import Dataset
from unspam.model import Model


def main():
    if len(sys.argv) != 4:
        sys.stderr.write('Usage: train.py <spam> <real> <output.pt>\n')
        sys.exit(1)

    spam_path, real_path, output_path = sys.argv[1:]

    dataset = Dataset(spam_path, real_path)
    words = dataset.top_words()
    train_inputs, train_labels = dataset.samples(words)
    test_inputs, test_labels = dataset.samples(words, train=False)

    model = Model(len(words))
    optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=0.02)
    loss_fn = nn.BCELoss()

    for i in itertools.count():
        optimizer.zero_grad()
        train_loss = loss_fn(model(train_inputs), train_labels)
        test_loss = loss_fn(model(test_inputs), test_labels)
        train_loss.backward()
        optimizer.step()
        if not i % 100:
            print('step %d: train=%f test=%f' % (i, train_loss.item(), test_loss.item()))


if __name__ == '__main__':
    main()
