"""
Fetch the contents of the spam folder.
"""

import imaplib
import json
import os
import sys

from unspam.email import fetch_message


OUTPUT_DIR = 'spam'


def main():
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: fetch_spam.py <username> <password>\n')
        sys.exit(1)
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    username = sys.argv[1]
    password = sys.argv[2]
    with imaplib.IMAP4_SSL('imap.ge.xfinity.com', 993) as conn:
        conn.login(username, password)
        _, data = conn.select('Junk')
        num_messages = int(data[0])
        _, ids = conn.search(None, 'ALL')
        for i, message_id in enumerate(ids[0].split(b' ')):
            message_id = str(message_id, 'utf-8')
            sys.stderr.write('Fetching message %d of %d: %s\n' % (i, num_messages, message_id))
            doc = fetch_message(conn, message_id)
            with open(os.path.join(OUTPUT_DIR, message_id + '.json'), 'w+') as out_file:
                json.dump(doc, out_file)


if __name__ == '__main__':
    main()
