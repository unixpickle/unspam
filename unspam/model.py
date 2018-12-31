"""
Classification models.
"""

import torch
import torch.nn as nn


class Model(nn.Module):
    """
    A text classification model.
    """

    def __init__(self, num_words):
        super().__init__()
        self.linear = nn.Linear(num_words + 1, 1)

    def forward(self, x):
        return torch.sigmoid(self.linear(x).view(-1))
