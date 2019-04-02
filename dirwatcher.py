#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Dirwatcher program.
Long Running Program that monitors a directory for certain files and a magic
word in the directory.
The program will continue to run unless sent a signal to terminate.
All other errors will be handled with exceptions and logged and
the program will continue running.

"""


__author__ = 'dougenas'

import argparse
import logging
import signal
import time
import os

exit_flag = True
checked_files = []

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(message)s')
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def signal_handler(signum, frame):
    global exit_flag
    sigs = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received OS Signal: {}'.format(sigs[signum]))
    if signum == signal.SIGINT or signum == signal.SIGTERM:
        exit_flag = False


def find_magic_word(dir, text):
    # print(os.listdir(path))

    global checked_files
    abspath = os.path.abspath(dir)
    files = os.listdir(abspath)

    text_files = [f for f in files]
    for file in text_files:
        if file.endswith(".txt") and file not in checked_files:
            logger.info('New file found: {}'.format(file))
            checked_files.append(file)
        if file.endswith(".txt"):
            file_path = os.path.join(abspath, file)
            if search_file(file_path, text):
                break
        for file in checked_files:
            if file not in files:
                logger.info('File deleted: {}'.format(file))
                checked_files.remove(file)

def search_file(file, text):
    logger.info("Searching {} for instances of {}".format(file, text))

    with open(file) as doc:
        content = doc.readlines()
        for i, line in enumerate(content):
            if text in line:
                logger.info("Match found for {} found on line {} in {}".format(text, i + 1, file))
        


def create_parser():
    """"creates argument parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--int', help='Polling interval for program')
    parser.add_argument('-m', '--magic', help='Magic text to be found in files')
    parser.add_argument('-p', '--path', help='Directory to be searched')
    return parser


def main():
    start_time = time.time()
    parser = create_parser()
    args = parser.parse_args()

    path = args.path
    text = args.magic
    int = args.int

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # enter function for finding magic word
    while exit_flag:
        try:
            find_magic_word(path, text)
        except Exception:
            logger.exception("exception on main")
        time.sleep(float(int))
        logger.info("Program uptime: {} seconds".format(time.time() - start_time))


if __name__ == "__main__":
    main()
