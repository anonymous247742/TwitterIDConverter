#! python
# -*- coding: utf8 -*-
import sys, getopt, os, re
from datetime import datetime
try:
    import tweepy
except:
    print "Please install tweepy"
    sys.exit()

# Change this
consumer_key = "YOUR CONSUMER KEY"
consumer_secret = "YOUR CONSUMER SECRET"
access_token = "YOUR ACCESS TOKEN"
access_token_secret = "YOUR ACCESS TOKEN SECRET"

def main(argv):
    d = datetime.now()
    date = str(d.year) + '' + str(d.month) + '' + str(d.day) + '' + str(d.hour) + '' + str(d.minute) + '' + str(d.second)
    input_f = None

    try:
        opts, args = getopt.getopt(argv, "hf:", ["input-file=", "help"])
    except getopt.GetoptError:
        print 'Use --help for help'
        sys.exit(2)

    for opt, arg in opts:
        print opt
        if opt in ("-h", "--help"):
            print 'Change API key in this file\n'
            print 'Usage: %s <options> \n' % (os.path.basename(__file__))
            print '     -h, --help              this help'
            print '     -f, --input-file FILE   Use file for convert name to ID twitter'
            sys.exit()
        elif opt in ("-f", "--input-file"):
            input_f = arg

    if not input_f:
        print 'Use --help for help'
        sys.exit(2)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    try:
        f = open(input_f, 'r')
    except:
        print "Unable to open file"
        sys.exit()

    for line in f:
        try:
            account = re.match(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?@?([^\/\?\s]*)", line.strip())
            account = account.group(1)
            o = api.get_user(account)
            with open("IDs_%s.txt" % (date), "a") as log:
                log.write("https://twitter.com/%s - %s - %s followers - %s friends\n" % (account, o.id, o.followers_count, o.friends_count))
        except:
            if line:
                account = re.match(r"(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:#!\/)?@?([^\/\?\s]*)", line.strip())
                account = account.group(1)
                print "Error with : %s account\n" % (account)
            else:
                print "Error\n"


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\nQuit by keyboard interrupt sequence!')
