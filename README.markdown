
Dorkitweet
==========

You can use this to send tweets via the command line, with URLs optionally
shortened by your CloudApp account.

This is very powerful when combined with [Alfred](http://alfredapp.com)!

(Dorkitweet is definitely a work in progress, but I hope someone finds it useful!)


Usage
-----

Send a tweet from the account "dorkitude":

    ./send_tweet.py dorkitude Hello there!  Learn more about wizards at http://dorkitude.com

Send a tweet and shorten the URLs:
    
    ./send_tweet.py --shorten_urls dorkitude The following URL will be shortened: http://learnpythonthehardway.org/book/ex47.html


Setup / Requirements
--------------------


Do this to get started:

    ./setup.py


Requirements:

 * MongoDB running on localhost at port 27017
 * a Twitter account
 * a CloudApp account

 (The app will also prompt you to make your own Twitter Application.)
