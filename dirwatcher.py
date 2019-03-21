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