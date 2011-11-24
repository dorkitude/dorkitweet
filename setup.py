#!/usr/bin/python


# stdlib imports:
import argparse

# third-party imports:
import tweepy

# dorkitweet imports:
from models.base import NoDefaultExistsError
from models.twitter import TwitterApplication, TwitterAccount
from models.cloud_app import CloudAppAccount, CloudAppClient



def main():
    """

    This is what runs!

    """

    options = parse_args()
    app = get_application()

    if options.add_twitter:
        prompt_new_twitter_account(app)

    if options.cloud:
        # delete the default if it exists:
        try:
            CloudAppAccount.get_default().delete()
        except:
            pass

    cloud_app = get_cloud_app_client()


    print "\n Setup complete! \n"



def parse_args():
    parser = argparse.ArgumentParser(description="dorkitweet setup")

    parser.add_argument(
            "--add_twitter",
            dest="add_twitter",
            action="store_true",
            help="Use this to add a new Twitter account.")

    parser.add_argument(
            "--cloud",
            dest="cloud",
            action="store_true",
            help="Use this to (re)configure your CloudApp account.")

    return parser.parse_args()


def prompt_new_cloud_app_account():
    
    # Have the user give us their username/password
    print "---------------"
    print "I need to store your Cloudapp username/password for URL shortening."
    print "(FYI: These will be stored in the clear in your local mongoDB.)"

    username = string_prompt("Enter your Cloudapp username:")
    password = string_prompt("Enter your Cloudapp password:")

    account = CloudAppAccount({
            "username": username,
            "password": password,
            "default": True,
            })

    # This will confirm that auth works:
    test_client = CloudAppClient.get(account=account)

    # Save the account to mongo and return it:
    account.save()

    print ""
    print "CloudApp Account successfully stored!"
    print ""

    return account

def prompt_new_twitter_account(app):

    # Figure out the auth URL:
    auth = tweepy.OAuthHandler(
            str(app.storage["consumer_key"]),
            str(app.storage["consumer_secret"]))
    auth_url = auth.get_authorization_url()

    # Have the user auth the app and enter their PIN:
    print "---------------"
    print "Go to this URL and authorize the app!"
    print ""
    print auth_url
    print ""
    pin = string_prompt("Enter your PIN once you authorize the app:")

    # Get the access credentials from Twitter:
    auth.get_access_token(pin)

    # Figure out the twitterh andle:
    api = tweepy.API(auth)

    twitter_user = api.me()

    account = TwitterAccount({
            "access_key": auth.access_token.key,
            "access_secret": auth.access_token.secret,
            "id": twitter_user.id,
            "name": twitter_user.screen_name,
            "full_name": twitter_user.name,
            }).save()

    print account
    




def prompt_new_application(default=False):
    """

    Get and store the credentials for this twitter account.

    """

    # Twitter Application instructions
    print "------------------------"
    print "Looks like you haven't told me about a twitter application yet!"
    print "If you haven't done it already, go make a Twitter Application here:"
    print "    https://dev.twitter.com/apps"
    print ""
    raw_input("Press Enter once you have made an Application on Twitter...")
    print ""

    # Collect Twitter application details
    consumer_key = string_prompt("Paste your Consumer Key here and press enter:")
    print "Got it!"
    print ""
    consumer_secret = string_prompt("Paste your Consumer Secret here and press enter:")

    print "Got it!"
    print ""

    print "Your consumer key is:        {}".format(consumer_key)
    print "Your consumer secret is:     {}".format(consumer_secret)


    app = TwitterApplication({
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "default": default,
            }).save()

    print ""
    print "-------"
    print "Created a new TwitterApplication with consumer_key={}!".format(
        consumer_key)
    print "-------"
    print ""

 
def string_prompt(instructions):
    print instructions
    item = raw_input(">").strip()

    if not item:
        print "EEK! Try again!"
        item = string_prompt(instructions)

    return item

def get_cloud_app_client():
    """

    Gets the specified TwitterApplication instance (or prompts you to create it)

    :returns:  TwitterApplication.

    """

    try:
        client = CloudAppClient.get()
    except NoDefaultExistsError:
        account = prompt_new_cloud_app_account()
        client = CloudAppClient.get()


def get_application():
    """

    Gets the specified TwitterApplication instance (or prompts you to create it)

    :returns:  TwitterApplication.

    """

    # Do they 

    # Confirm there's not an TwitterApplication already configured.
    try:
        # `TwitterApplication.get` has to raise a NoApplicationError!
        return TwitterApplication.get_default()
        # If we made it to this line, that is bad:
    except NoDefaultExistsError:
        return prompt_new_application(default=True)





# Last line:  run!
main()
