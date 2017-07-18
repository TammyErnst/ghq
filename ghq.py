#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import argparse
from datetime import datetime
import dateparser
import re
import getpass
import os.path



# function returns a string representing the range from since (a string like "1 day ago" or "2 months") to now or Unbounded
def since_to_range_string(since):
    if since == None or (not isinstance(since, str) and not isinstance(since, unicode)):
        return "Unbounded"
    now = datetime.now()
    datefrom = dateparser.parse(since)
    return "from {:%Y-%m-%d %H:%M}".format(datefrom) + " to {:%Y-%m-%d %H:%M}".format(now)

# function returns the input title's JIRA ID (by looking for jira_key input) and '!!!' if no JIRA ID found
def find_jira_id(title, jira_key):
    if not isinstance(title, str) and not isinstance(title, unicode):
        return "!!!"
    if not isinstance(jira_key, str) and not isinstance(jira_key, unicode):
        return "!!!"
    match = re.search('(?:.* )?('+ jira_key +'-[0-9]+)(?: .*)?', title)    # JIRA ID is jira-key followed by hyphon and number
    if (match == None):   # no JIRA ID found
        return "!!!"
    else:                 # return the JIRA ID found
        return match.group(1)

# function tests find_jira_id function running one test case
def test_one_find_jira_id(title, jira_key, expected):
    if (find_jira_id(title, jira_key) == expected):
        return True
    msg = "test_one_find_jira_id with '" + str(title) + "' and '" + str(jira_key) + "' expected '" + str(expected)
    msg += "' and got '" + find_jira_id(title, jira_key) + "'"
    print msg
    return False

# function tests find_jira_id function running all tests
def test_all_find_jira_id():
    success = True
    success = success and test_one_find_jira_id("Hello World BY-1", "BY", "BY-1")
    success = success and test_one_find_jira_id("Hello World", "BY", "!!!")
    success = success and test_one_find_jira_id("Hello World BY", "BY", "!!!")
    success = success and test_one_find_jira_id("BY-123", "BY", "BY-123")
    success = success and test_one_find_jira_id("BY-321 Flying to the moon", "BY", "BY-321")
    success = success and test_one_find_jira_id("BY-321: Flying to the moon", "BY", "BY-321")
    success = success and test_one_find_jira_id("Issue HELP-42 It does not work", "HELP", "HELP-42")
    success = success and test_one_find_jira_id("Issue HELP-42 It does not work", "BY", "!!!")
    success = success and test_one_find_jira_id("Issue HELP-XXX It does not work", "HELP", "!!!")
    success = success and test_one_find_jira_id("Issue HELP-??? It does not work", "HELP", "!!!")
    success = success and test_one_find_jira_id("Issue HELP42 It does not work", "HELP", "!!!")
    success = success and test_one_find_jira_id("Issue HELP42 It does not work", 5, "!!!")
    return success

# function returns dictionary with added record of one more file of that type. takes a dictionary and a filename
def count_file(dict, filename):
    type = os.path.splitext(filename)[1][1:]    # split off file type and remove .
    dict[type] = dict.get(type, 0) + 1          # increase type's count by 1, or add a count of 1
    return dict

# function tests count_file function running one test case
def test_one_count_file(dict, filename, expected):
    if (count_file(dict, filename) == expected):
        return True
    msg = "test_one_count_file with '" + str(dict) + "' and '" + str(filename) + "' expected '"
    msg += str(expected) + "' and got '" + str(count_file(dict, filename)) + "'"
    print msg
    return False

# function tests count_file function running all tests
def test_all_count_file():
    success = True
    success = success and test_one_count_file({}, "hello-world.jar", {'jar': 1})
    success = success and test_one_count_file({'jar': 1}, "hello-world.jar", {'jar': 2})
    success = success and test_one_count_file({'jpg': 1}, "hello-world.jar", {'jar': 1, 'jpg': 1})
    success = success and test_one_count_file({'jar': 1, 'jpg': 1}, "wonder.jar", {'jar': 2, 'jpg': 1})
    success = success and test_one_count_file({'jar': 2, 'jpg': 1}, "wonder.zip", {'zip': 1, 'jar': 2, 'jpg': 1})
    success = success and test_one_count_file({'zip': 1, 'jar': 2, 'jpg': 1}, "bears.jpg", {'zip': 1, 'jar': 2, 'jpg': 2})
    return success

# function returns dictionary with added record of one more PR by that author with merged and total counts both kept
def count_author_prs(dict, author, merged):
    if merged:
        dict[author] = (dict.get(author, (0, 0))[0] + 1, dict.get(author, (0, 0))[1] + 1)
    else:
        dict[author] = (dict.get(author, (0, 0))[0], dict.get(author, (0, 0))[1] + 1)
    return dict

# function tests count_author_prs function running one test case
def test_one_count_author_prs(dict, author, merged, expected):
    if (count_author_prs(dict, author, merged) == expected):
        return True
    msg = "test_one_count_author_prs with '" + str(dict) + "' and '" + str(author) + "' and " + str(merged)
    msg += " expected '" + str(expected) + "' and got '" + str(count_author_prs(dict, author, merged)) + "'"
    print msg
    return False

# function tests count_author_prs function running all tests
def test_all_count_author_prs():
    success = True
    success = success and test_one_count_author_prs({}, "Nelson Mandela", False, {'Nelson Mandela': (0, 1)})
    success = success and test_one_count_author_prs({}, "Nelson Mandela", True, {'Nelson Mandela': (1, 1)})
    success = success and test_one_count_author_prs({'Nelson Mandela': (1, 1)}, "Mother Goose", False, {'Mother Goose': (0, 1), 'Nelson Mandela': (1, 1)})
    success = success and test_one_count_author_prs({'ab': (1, 1)}, "ab", False, {'ab': (1, 2)})
    success = success and test_one_count_author_prs({'ab': (1, 3)}, "ab", True, {'ab': (2, 4)})
    success = success and test_one_count_author_prs({'bc': (2, 3), 'ab': (3, 4), 'cd': (0, 5)}, "ab", False, {'bc': (2, 3), 'ab': (3, 5), 'cd': (0, 5)})
    success = success and test_one_count_author_prs({'bc': (2, 3), 'ab': (3, 4), 'cd': (0, 5)}, "ab", True, {'bc': (2, 3), 'ab': (4, 5), 'cd': (0, 5)})
    return success

# function to sort count_author_prs by merged count desc, total count desc, and author
def sort_authorstats_by_counts(authorstats):
    return dict(sorted(authorstats.items(), key=lambda x: (-x[1][0], -x[1][1], x[0])))

# function tests sort_authorstats_by_counts function running one test case
def test_one_sort_authorstats_by_counts(dict, expected):
    if (sort_authorstats_by_counts(dict) == expected):
        return True
    msg = "test_one_sort_authorstats_by_counts with '" + str(dict)
    msg += " expected '" + str(expected) + "' and got '" + str(sort_authorstats_by_counts(dict)) + "'"
    print msg
    return False

# function tests sort_authorstats_by_counts function running all tests
def test_all_sort_authorstats_by_counts():
    success = True
    success = success and test_one_sort_authorstats_by_counts({}, {})
    success = success and test_one_sort_authorstats_by_counts({'ab': (1, 1)}, {'ab': (1, 1)})
    success = success and test_one_sort_authorstats_by_counts({'bc': (2, 3), 'ab': (3, 5), 'cd': (0, 5)}, {'ab': (3, 5), 'bc': (2, 3),'cd': (0, 5)})
    success = success and test_one_sort_authorstats_by_counts({'bc': (2, 3), 'ab': (2, 3), 'cd': (0, 5)}, {'ab': (2, 3), 'bc': (2, 3), 'cd': (0, 5)})
    success = success and test_one_sort_authorstats_by_counts({'bc': (2, 3), 'ab': (2, 3), 'cd': (2, 5)}, {'cd': (2, 5), 'ab': (2, 3), 'bc': (2, 3)})
    success = success and test_one_sort_authorstats_by_counts({'bc': (3, 3), 'ab': (2, 3), 'cd': (0, 5)}, {'bc': (3, 3), 'ab': (2, 3), 'cd': (0, 5)})
    return success




# parse arguments
argparser = argparse.ArgumentParser(description="GitHub query for Pull Requests and stats")
argparser.add_argument("-r", "--repo", type=str, help="GitHub Repository (ex:'h2oai/h2o-3') required", required=True)
argparser.add_argument("-j", "--jira_key", type=str, help="JIRA key expected in PR titles (ex:'PUBDEV') required", required=True)
argparser.add_argument("-s", "--since", type=str, help="period of time to query over (exs:'3 days', '2 months ago') defaults to no time bound")
argparser.add_argument("-t", "--test", help="Run unit tests and do not connect to GitHub", action="store_true")
args = argparser.parse_args()


# validate argument since
if (args.since != None and dateparser.parse(args.since) == None):
    print "Argument since value '" + args.since + "' could not be parsed.  Try '1 day ago' or '2 months'"
    sys.exit()

# output title line
print "*** GitHub repo " + args.repo + " (" + since_to_range_string(args.since) + ") ***"


if (args.test):    # if testing requested on the command line, run the tests and exit
    print "test_all_find_jira_id() returned " + str(test_all_find_jira_id())
    print "test_all_count_file() returned " + str(test_all_count_file())
    print "test_all_count_author_prs() returned " + str(test_all_count_author_prs())
    print "test_all_sort_authorstats_by_counts() returned " + str(test_all_sort_authorstats_by_counts())
    sys.exit()

# read in GitHub credentials
if sys.stdin.isatty():    # prompt when input device is tty
   print "Enter GitHub credentials"
   print >> sys.stderr, "GitHub Username: "    # stderr in case output is being redirected
   githubusername = raw_input()
   githubpassword = getpass.getpass("GitHub Password: ")
else:
   githubusername = sys.stdin.readline().rstrip()
   githubpassword = sys.stdin.readline().rstrip()

# connect to GitHub and the repo
#githubsession = Github(githubusername, githubpassword)
#repo = githubsession.get_repo(args.repo)

# create dictionary of Pull Request authors
authorstats = {}

# request the Pull Requests and loop through them



