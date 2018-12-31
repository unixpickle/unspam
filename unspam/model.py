"""
Classification models.
"""

import torch.nn as nn


class Model(nn.Module):
    """
    A text classification model.
    """

    def __init__(self, num_words):
        self.linear = nn.Linear(num_words, 1)

    def forward(self, x):
        return self.linear(x).view(-1)