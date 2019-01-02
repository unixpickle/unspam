# unspam

This is a small IMAP spam filter. It includes utilities to fetch emails from your inbox, train a classifier on the emails, and move emails based on the result of a classifier.

# Usage

First, install the dependencies:

```
pip install bs4 torch numpy
```

Next, fetch your emails and categorize them into two directories, `spam` and `real`. The `fetch_emails.py` script includes some examples:

```
python fetch_emails.py --username USER --password PASS --output-dir spam --mailbox Junk
python fetch_emails.py --username USER --password PASS --output-dir real --mailbox Inbox
```

Next, make sure the data is all correct. Remove any false positives/negatives. The emails are stored in a simple-to-read JSON format, so `cat`, `mv`, and `rm` should be enough for this.

Once we have a dataset, we can train a classifier. Do this with the `train.py` script:

```
python train.py spam/ real/
```

This will save a trained classifier to a file called "output.pt". You'll want to kill the program once the training and test loss seem to flatten out.

Finally, you can run a loop to move spam to the junk folder:

```
while (true) do python move_spam.py --username USER --password PASS; sleep 600; done
```

# How it works

The classifier itself uses logistic regression on top of bag-of-words features. In other words, it turns every email into a vector of word counts, and then feeds the vector into a linear model.
