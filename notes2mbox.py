#!/usr/bin/env python

import sqlite3
import argparse
import mailbox
import email.message
import email.header
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def convert(db_path, mbox_path, device_name):
    mbox = mailbox.mbox(mbox_path, create=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute("SELECT * FROM ZNOTE")
    for row in curs.fetchall():
        curs.execute("SELECT * FROM ZNOTEBODY WHERE Z_PK=?", (row['Z_PK'],))
        content = curs.fetchone()['ZCONTENT'].encode('utf8')
        msg = MIMEText(content, 'html', 'utf8')

        msg.set_unixfrom("From %s %s" % (device_name,
                                         shift_date(row['ZMODIFICATIONDATE']).ctime()))
        msg['From'] = device_name
        subject = row['ZTITLE']
        print subject
        print row['ZSUMMARY']
        try:
            subject.encode('ascii')
        except UnicodeEncodeError:
            try:
                subject = email.header.Header(subject.encode('GB2312'), 'GB2312')
            except UnicodeEncodeError:
                subject = email.header.Header(subject.encode('utf8'), 'UTF-8')
        msg['Subject'] = subject
        msg['X-Universally-Unique-Identifier'] = row['ZGUID']
        msg.set_charset('utf-8')
        msg['X-Uniform-Type-Identifier'] = 'com.apple.mail-note'
        msg['MIME-Version'] = "1.0 (Apple Message framework v1244.3)"
        msg['X-Mail-Created-Date'] = rfc_2822(shift_date(row['ZCREATIONDATE']))
        msg['Date'] = rfc_2822(shift_date(row['ZMODIFICATIONDATE']))
        msg['X-Mail-Generated-Subject'] = 'YES'

        mbox.add(msg)

def shift_date(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    dt = datetime(year=dt.year+31, month=dt.month, day=dt.day, hour=dt.hour,
                  minute=dt.minute, second=dt.second)
    return dt + timedelta(days=1)

def rfc_2822(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0800")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db', metavar='path/to/notes.sqlite')
    parser.add_argument('mbox')
    parser.add_argument('--device-name', required=True)
    args = parser.parse_args()
    convert(args.db, args.mbox, device_name=args.device_name)


if __name__ == '__main__':
    main()

