#!/usr/bin/python


# stdlib imports:
import argparse

# third-party imports:
import tweepy
import pymongo

# dorkitweet imports:
from models.twitter import TwitterAccount, Tweet
import url_shortener


def main():
    options = parse_args()

    tweet = Tweet.create(
            body_words=options.tweet_body,
            account=TwitterAccount.get_by_name(
                    options.account_name, 
                    demand_existence=True),
            shorten_urls=options.shorten_urls)

    print "\nAbout to send! {}".format(tweet)
    tweet.send()
    print "\nSent!"

    print "\n\n{}".format(tweet)

    #elif len(args) is 1:
        #tweet = command_line_args[0]
        #account = Account.get_by_name(name)
    #else:
        #raise TooManyArgumentsError(args)


def parse_args():
    parser = argparse.ArgumentParser(description="dorkitweet setup")
    parser.add_argument(
            "account_name",
            type=str,
            help="The handle of the Twitter account for this tweet.")

    parser.add_argument(
            "tweet_body",
            type=str,
            nargs="*",
            help="The body of the Tweet.")

    parser.add_argument(
            "--shorten_urls",
            dest="shorten_urls",
            action="store_true",
            help="")

    parser.add_argument(
            "--long_urls",
            dest="shorten_urls",
            action="store_false",
            help="")

    return parser.parse_args()




class MissingArgumentError(Exception):
    pass


class TooManyArgumentsError(Exception):
    def __init__(self, args):
        msg = "Too many arguments: {}".format(args)
        super(self.__class__, self).__init__(msg)





main()
