"""
Fetch the contents of an email folder.

Examples:

    $ python fetch_emails.py --username USER --password PASS --output-dir spam --mailbox Junk
    $ python fetch_emails.py --username USER --password PASS --output-dir real --mailbox Inbox

"""

import argparse
import hashlib
import imaplib
import json
import os
import sys

from unspam.email import fetch_message


def main():
    args = arg_parser().parse_args()
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    with imaplib.IMAP4_SSL(args.server, 993) as conn:
        conn.login(args.username, args.password)
        _, data = conn.select(args.mailbox)
        num_messages = int(data[0])
        _, ids = conn.search(None, 'ALL')
        for i, message_id in enumerate(ids[0].split(b' ')):
            message_id = str(message_id, 'utf-8')
            sys.stderr.write('Fetching message %d of %d: %s\n' % (i, num_messages, message_id))
            doc = fetch_message(conn, message_id)
            data = bytes(json.dumps(doc), 'utf-8')
            filename = os.path.join(args.output_dir, content_filename(data) + '.json')
            if not os.path.exists(filename):
                with open(filename, 'wb+') as out_file:
                    out_file.write(data)


def content_filename(data):
    h = hashlib.sha1()
    h.update(data)
    return h.hexdigest()


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', help='imap server', default='imap.ge.xfinity.com')
    parser.add_argument('--username', help='imap username', required=True)
    parser.add_argument('--password', help='imap password', required=True)
    parser.add_argument('--output-dir', help='output directory', default='real')
    parser.add_argument('--mailbox', help='mailbox to dump', default='Inbox')
    return parser


if __name__ == '__main__':
    main()
