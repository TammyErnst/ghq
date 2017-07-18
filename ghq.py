#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import argparse
from datetime import datetime
import dateparser
import re



# function returns a string representing the range from since (a string like "1 day ago" or "2 months") to now or Unbounded
def since_to_range_string(since):
    if since == None:
        return "Unbounded"
    now = datetime.now()
    datefrom = dateparser.parse(since)
    print datefrom
    return "from {:%Y-%m-%d %H:%M}".format(datefrom) + " to {:%Y-%m-%d %H:%M}".format(now)

# function returns the input title's JIRA ID (by looking for jira_key input) and '!!!' if no JIRA ID found
def find_jira_id(title, jira_key):
    match = re.search('(?:.* )?('+ jira_key +'-[0-9]+)(?: .*)?', title)    # JIRA ID is jira-key followed by hyphon and number
    if (match == None):   # no JIRA ID fouond
        return "!!!"
    else:                 # return the JIRA ID found
        return match.group(1)

# function tests find_jira_id function running one test case
def test_one_find_jira_id(title, jira_key, expected):
    if (find_jira_id(title, jira_key) == expected):
        return True
    print "test_one_find_jira_id with '" + title + "' and '" + jira_key + "' expected '" + expected + "' and got '" + find_jira_id(title, jira_key) + "'"
    return False

# function tests find_jira_id function running all tests
def test_all_find_jira_id():
    success = True
    # success = success and test_one_find_jira_id("Hello World", "JIRA", "nonesense")
    success = success and test_one_find_jira_id("Hello World BY-1", "BY", "BY-1")
    success = success and test_one_find_jira_id("BY-123", "BY", "BY-123")
    success = success and test_one_find_jira_id("BY-321 Flying to the moon", "BY", "BY-321")
    return success




# parse arguments
argparser = argparse.ArgumentParser(description="GitHub query for Pull Requests and stats")
argparser.add_argument("-r", "--repo", help="GitHub Repository (ex:'h2oai/h2o-3') required", required=True)
argparser.add_argument("-j", "--jira_key", help="JIRA key expected in PR titles (ex:'PUBDEV') required", required=True)
argparser.add_argument("-s", "--since", help="period of time to query over (exs:'3 days', '2 months ago') defaults to no time bound")
argparser.add_argument("-t", "--test", help="Run unit tests and do not connect to GitHub", action="store_true")
args = argparser.parse_args()


# validate argument since
if ( args.since != None and dateparser.parse(args.since) == None):
    print "Argument since value '" + args.since + "' could not be parsed.  Try '1 day ago' or '2 months'"
    sys.exit()


# output title line
print "*** GitHub repo " + args.repo + " (" + since_to_range_string(args.since) + ") ***"

print "JIRA Key is " + args.jira_key

if (args.test):
    print "test_all_find_jira_id() returned " + str(test_all_find_jira_id())

