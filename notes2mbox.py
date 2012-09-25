#!/usr/bin/env python

import sqlite3
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('db', metavar='path/to/notes.sqlite')
    args = parser.parse_args()


if __name__ == '__main__':
    main()

