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
import datetime
import os

exit_flag = False
logger = logging.getLogger(__name__)


def signal_handler(signum):
    """Logs SIGINT and SIGTERM signals"""
    global exit_flag
    sigs = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received OS Signal: {}'.format(sigs[signum]))
    if signum == signal.SIGINT or signum == signal.SIGTERM:
        exit_flag = True


def create_parser():
    """"creates argument parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', help='File extension of file to search through')
    parser.add_argument('-i', '--int', help='Polling interval for program')
    parser.add_argument('-m', '--magic', help='Magic text to be found in files')
    parser.add_argument('-p', '--path', help='Directory to be searched')
    return parser

def main():
    parser = create_parser().parse_args()
    args = parser.parse_args()

    path = args.path
    text = args.magic

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    #enter function for finding magic word


if __name__ == "__main__":
    main()