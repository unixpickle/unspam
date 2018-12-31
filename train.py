"""
Train a classifier.
"""

import itertools
import sys

import torch
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
            false_negs = count_false_negatives(model(test_inputs), test_labels)
            print('step %d: train=%f test=%f false_neg=%d' %
                  (i, train_loss.item(), test_loss.item(), false_negs))
            save(output_path, model, words)


def count_false_negatives(outputs, labels):
    spams = (outputs < 0.5).type(torch.FloatTensor)
    return torch.sum(spams * labels)


def save(output_path, model, words):
    state = {
        'model': model.state_dict(),
        'words': words,
    }
    torch.save(state, output_path)


if __name__ == '__main__':
    main()
