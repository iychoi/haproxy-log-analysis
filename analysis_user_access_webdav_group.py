#! /usr/bin/python

import os
import os.path
import sys
import datetime

from sets import Set


def parse_fields(line, begin, end):
    fields = line.split(" ")
    user = fields[6].strip()
    timestamp = fields[7].strip()[1:-1]

    # conv to python datetime obj
    datetimeobj = datetime.datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S.%f")

    if datetimeobj < begin or datetimeobj > end:
        return False, datetimeobj, user

    # drop port
    portidx = user.index(":")
    if portidx >= 0:
        user = user[:portidx]

    lastipidx = user.rindex(".")
    if lastipidx >= 0:
        user = user[:lastipidx]

    hasvalue = True
    if fields[8].strip() != "webdav":
        hasvalue = False

    return hasvalue, datetimeobj, user


def countSort(val):
    return val[1]


def analysis(log_file_path, begin, end):
    access_counter = {}

    with open(log_file_path, "r") as f:
        for line in f:
            has_value, timestamp, user = parse_fields(line, begin, end)
            
            if has_value:
                if user in access_counter:
                    access_counter[user]["count"] += 1
                else:
                    access_counter[user] = {
                        "count": 1
                    }

    access_counter_arr = []
    for user in access_counter:
        count = access_counter[user]["count"]
        access_counter_arr.append((user, count))

    access_counter_arr.sort(key=countSort, reverse=True)

    for counter in access_counter_arr:
        print "%s %d" % (counter[0], counter[1])


def main(argv):
    if len(argv) < 1:
        print "command : ./analysis_user_access.py logfile"
    else:
        log_file_path = argv[0]
        begin = datetime.datetime.strptime("01/Jan/2000:00:00:00", "%d/%b/%Y:%H:%M:%S")
        end = datetime.datetime.now()
        if len(argv) == 3:
            begin = datetime.datetime.strptime(argv[1], "%d/%b/%Y:%H:%M:%S")
            end = datetime.datetime.strptime(argv[2], "%d/%b/%Y:%H:%M:%S")

        analysis(log_file_path, begin, end)


if __name__ == "__main__":
    main(sys.argv[1:])
