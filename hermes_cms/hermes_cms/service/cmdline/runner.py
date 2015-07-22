# /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse


"""
get job file
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--job', required=True)
    parser.parse_args()
