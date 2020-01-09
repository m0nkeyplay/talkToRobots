#!/usr/bin/python3
#   2020/01/09 
#   eric@themonkeyplayground.com
#   Read robots.txt files from one or a list of sites

import os
import re
import random
import requests
import argparse
import signal
import urllib

#   CTRL+C handler - from https:/gist.github.com/mikerr/6389549
def handler(signum, frame):
    print("\n^^^^^^Task aborted by user.  Some cleanup may be necessary.")
    exit(0)

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--starturl", required=False, help="Starting URL if checking just one.")
ap.add_argument("-f", "--file", required=False, help="File of FQDNs to check.")
args = vars(ap.parse_args())

logName = 'robotRandom'+str(random.randint(100,500))+'.txt'

def make_robot(url):
    fqdn = fqdn = urllib.parse.urlsplit(url.strip())
    if 'http' in fqdn.scheme and fqdn.netloc is not '':
        return fqdn.scheme+"://"+fqdn.netloc+"/robots.txt"
    elif not fqdn.scheme and not fqdn.netloc:
        return 'http://'+fqdn.path+'/robots.txt'
    else:
        print("We can't make a URL from %s.  Exiting."%url)
        exit(0)


def talk_to_robots(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print("Robot @ %s says:"%url)
            log.write("\nRobot @ %s says:\n"%url)
            print(r.text)
            log.write(r.text)
        else:
            print("No robots to speak to @ %s.")
            log.write("\nNo robots to speak to @ %s.\n")
    except:
        print("Unable to connect to %s"%url)
        log.write("Unable to connect to %s\n"%url)


if __name__ == '__main__':
    if args["starturl"]:
        print("Checking for robots @ %s"%args["starturl"].strip())
        talk_to_robots(make_robot(args["starturl"].strip()))
    elif args["file"]:
        if not os.path.isfile(args["file"]):
            print("We can't find the file you would like to check.")
            exit()
        else:
            log = open(logName,'w')
            with open(args["file"]) as urlFile:
                for line in urlFile:
                    talk_to_robots(make_robot(line))
            print("Data written to %s"%logName)
            log.close()
                    
