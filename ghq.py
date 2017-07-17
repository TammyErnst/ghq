#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import argparse


# parse arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-r", "--repo", help="GitHub Repository (ex:'h2oai/h2o-3') required", required=True)
args = argparser.parse_args()

print "*** GitHub repo " + args.repo + " ***"
