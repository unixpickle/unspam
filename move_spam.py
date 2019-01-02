"""
Move classified spam to the spam folder.
"""

import argparse
import imaplib
import sys

import numpy as np
import torch

from unspam.data import email_vector
from unspam.email import fetch_message, move_message
from unspam.model import Model


def main():
    args = arg_parser().parse_args()

    state = torch.load(args.model)
    words = state['words']
    model = Model(len(words))
    model.load_state_dict(state['model'])

    with imaplib.IMAP4_SSL(args.server, 993) as conn:
        conn.login(args.username, args.password)
        conn.select(args.in_mailbox)
        while remove_spam(args, conn, model, words):
            pass


def remove_spam(args, conn, model, words):
    _, ids = conn.search(None, 'ALL')
    for i, message_id in enumerate(ids[0].split(b' ')):
        message_id = str(message_id, 'utf-8')
        doc = fetch_message(conn, message_id)
        raw_vec = email_vector(words, doc)
        vec = torch.from_numpy(np.array([raw_vec], dtype=np.float32))
        pred = model(vec)[0].detach().numpy()
        if pred < 0.5 and len(doc['subject'] + doc['body']) > args.min_length:
            sys.stderr.write('Found spam: %s\n' % doc['subject'])
            move_message(conn, message_id, args.out_mailbox)
            return True
    return False


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', help='imap server', default='imap.ge.xfinity.com')
    parser.add_argument('--username', help='imap username', required=True)
    parser.add_argument('--password', help='imap password', required=True)
    parser.add_argument('--in-mailbox', help='input mailbox', default='Inbox')
    parser.add_argument('--out-mailbox', help='spam mailbox', default='Junk')
    parser.add_argument('--model', help='model path', default='output.pt')
    parser.add_argument('--min-length', help='minimum characters to scan email', default=60,
                        type=int)
    return parser


if __name__ == '__main__':
    main()
