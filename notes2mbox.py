#!/usr/bin/env python

import sqlite3
import argparse
import mailbox
import email.message
import email.header
from datetime import datetime, timedelta

def convert(db_path, mbox_path, device_name):
    mbox = mailbox.mbox(mbox_path, create=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute("SELECT * FROM ZNOTE")
    for row in curs.fetchall():
        msg = email.message.Message()
        dt = datetime.fromtimestamp(row['ZMODIFICATIONDATE'])
        modtime = datetime(year=dt.year+31, month=dt.month, day=dt.day,
                           hour=dt.hour, minute=dt.minute, second=dt.second)
        modtime += timedelta(days=1)
        msg.set_unixfrom("From %s %s" % (device_name, modtime.ctime()))
        msg['From'] = device_name
        subject = row['ZTITLE']
        print subject
        try:
            subject.encode('ascii')
        except UnicodeEncodeError:
            try:
                subject = email.header.Header(subject.encode('GB2312'), 'GB2312')
            except UnicodeEncodeError:
                subject = email.header.Header(subject.encode('utf8'), 'UTF-8')
        msg['Subject'] = subject
        msg.set_charset('base64')
        mbox.add(msg)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db', metavar='path/to/notes.sqlite')
    parser.add_argument('mbox')
    parser.add_argument('--device-name', required=True)
    args = parser.parse_args()
    convert(args.db, args.mbox, device_name=args.device_name)


if __name__ == '__main__':
    main()

