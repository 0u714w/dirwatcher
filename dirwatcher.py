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

stay_running = True
files_logged = []
found_magic_text = {}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(message)s')
file_handler = logging.FileHandler("dirwatcher.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def signal_handler(signum, frame):
    global stay_running
    sigs = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received OS Signal: {}'.format(sigs[signum]))

    stay_running = False


def find_magic_word(directory, magic_text, ext):
    """Watches a given directory for instances of a magic text"""
    global files_logged
    global found_magic_text

    try:
        text_files = [f for f in os.listdir(directory) if not f.startswith('.')]
    except:
        logger.info('Directory {} does not exists'.format(directory))
    else:
        abspath = os.path.abspath(directory)
        files = os.listdir(abspath)
        for file in text_files:
            if file.endswith(ext) and file not in files_logged:
                logger.info('New file found: {}'.format(file))
                files_logged.append(file)
            if file.endswith(ext):
                full_path = os.path.join(abspath, file)
                if search_single_file(full_path, magic_text):
                    break
        for file in files_logged:
            if file not in files:
                logger.info('File deleted: {}'.format(file))
                files_logged.remove(file)
                found_magic_text[file] = 0


                  

def search_single_file(full_pathname, magic_text):
    """Seatches a signle file for a line containing magic text"""
    with open(full_pathname) as doc:
        content = doc.readlines()
        for line_number, line in enumerate(content):
            if magic_text in line:
                if full_pathname not in found_magic_text.keys():
                    found_magic_text[full_pathname] = line_number
                if (line_number >= found_magic_text[full_pathname]) and full_pathname in found_magic_text.keys():
                    logger.info("Match found for {} found on line {} in {}".format(magic_text, line_number + 1, full_pathname))
                    found_magic_text[full_pathname] += 1


def create_parser():
    """"creates argument parser"""
    parser = argparse.ArgumentParser(description='Watches a directory for files containing magic text')
    parser.add_argument('-i', '--int', help='Polling interval for program')
    parser.add_argument('-e', '--ext', help='Extension of file to search for', default=".txt")
    parser.add_argument('path', help='Directory to be searched', default= ".")
    parser.add_argument('magic', help='Magic text to be found in files')
    return parser


def main():
    start_time = time.time()
    parser = create_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # enter function for finding magic word
    logger.info("Watching directory {} for files ending with {} containing magic text {}".format(args.path, args.ext, args.magic))
    while stay_running:
        try:
            find_magic_word(args.path, args.magic, args.ext)
        except Exception:
            logger.exception("exception on main")
        time.sleep(float(args.int))
        logger.info("Program uptime: {} seconds".format(time.time() - start_time))


if __name__ == "__main__":
    main()
