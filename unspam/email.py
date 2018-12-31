"""
Utilities for dealing with emails.
"""

import email
from bs4 import BeautifulSoup


def fetch_message(conn, id):
    """
    Fetch a message from an IMAP connection.

    Args:
      conn: the connection.
      id: the message ID.

    Returns:
      A dict containing the following keys:
        subject: a str containing the subject line.
        body: a str containing the message body.
    """
    payload = _raw_data(conn.fetch(id, '(RFC822)')[1])
    msg = email.message_from_bytes(payload)
    if msg['Subject']:
        subject, enc = email.header.decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = _bytes_to_str(subject, enc)
    else:
        subject = ''
    body = _text_body(msg)
    return {'subject': subject, 'body': body}


def _raw_data(body_data):
    return next(x for x in body_data if isinstance(x, tuple))[1]


def _text_body(msg):
    content = _part_payload(msg, 'text/plain')
    if content:
        return content
    html_content = _part_payload(msg, 'text/html')
    if html_content:
        return _html_strings(html_content)
    return ''


def _part_payload(msg, content_type):
    for part in msg.walk():
        if part.get_content_disposition() == 'attachment' or part.is_multipart():
            continue
        if part.get_content_type() == content_type:
            payload = part.get_payload(decode=True)
            if isinstance(payload, bytes):
                payload = _bytes_to_str(payload, part.get_charsets()[0])
            return payload
    return None


def _html_strings(html_content):
    # https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    soup = BeautifulSoup(html_content, features='html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\r\n'.join(chunk for chunk in chunks if chunk)


def _bytes_to_str(data, enc):
    try:
        return str(data, enc)
    except:  # noqa: E722
        return str(data, 'cp437')
