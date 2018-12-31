"""
Fetch the contents of the spam folder.
"""

import imaplib
import sys

import numpy as np
import torch

from unspam.data import email_vector
from unspam.email import fetch_message
from unspam.model import Model


MIN_LENGTH = 60


def main():
    if len(sys.argv) != 4:
        sys.stderr.write('Usage: fetch_spam.py <username> <password> <model>\n')
        sys.exit(1)

    username, password, model_path = sys.argv[1:]

    state = torch.load(model_path)
    words = state['words']
    model = Model(len(words))
    model.load_state_dict(state['model'])

    with imaplib.IMAP4_SSL('imap.ge.xfinity.com', 993) as conn:
        conn.login(username, password)
        conn.select('INBOX')
        _, ids = conn.search(None, 'ALL')
        for i, message_id in enumerate(ids[0].split(b' ')):
            message_id = str(message_id, 'utf-8')
            doc = fetch_message(conn, message_id)
            raw_vec = email_vector(words, doc)
            vec = torch.from_numpy(np.array([raw_vec], dtype=np.float32))
            pred = model(vec)[0].detach().numpy()
            if pred < 0.5 and len(doc['subject'] + doc['body']) > MIN_LENGTH:
                sys.stderr.write('Found spam: %s\n' % doc['subject'])


if __name__ == '__main__':
    main()
