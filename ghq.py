#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import argparse
from datetime import datetime
import dateparser



# function returns a string representing the range from since (a string like "1 day ago" or "2 months") to now or Unbounded
def since_to_range_string(since):
    if since == None:
        return "Unbounded"
    now = datetime.now()
    datefrom = dateparser.parse(since)
    print datefrom
    return "from {:%Y-%m-%d %H:%M}".format(datefrom) + " to {:%Y-%m-%d %H:%M}".format(now)



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
