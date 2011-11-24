
Dorkitweet
==========

You can use this to send tweets via the command line, with URLs optionally
shortened by your CloudApp account.


(Dorkitweet is definitely a work in progress, but I hope someone finds it useful!)


Alfred
------

Dorkitweet is very powerful when combined with [Alfred](http://alfredapp.com).

In fact, Alfred is the main reason I made this thing.

Now, to send a tweet from my Mac, I just do this:

 1. `command-space`
 2. type `tweet blah blah blah blah blah`
 3. press `Enter`

_kickinrad_, no?

FYI, here are my Alfred Extension settings:

 * http://drktd.com/C5eT
 * http://drktd.com/C4Nx



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
