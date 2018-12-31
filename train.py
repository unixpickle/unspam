"""
Train a classifier.
"""

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
    inputs, labels = dataset.samples(words)
    inputs = torch.fromarray(inputs)
    labels = torch.fromarray(labels)

    model = Model(len(words))
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.BCELoss()

    while True:
        optimizer.zero_grad()
        loss = loss_fn(torch.sigmoid(model(inputs)), labels)
        loss.backward()
        optimizer.step()
        print('loss=%f' % loss.item())


if __name__ == '__main__':
    main()
