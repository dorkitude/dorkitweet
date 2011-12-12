Dorkitweet
==========

You can use this to send tweets via the command line, with URLs optionally
shortened by your [CloudApp](http://getcloudapp.com) account.

Dorkitweet is pretty rough around the edges, but I thought someone may find it useful.




Alfred
------

I pretty much only use Dorkitweet as a way to tweet via [Alfred](http://alfredapp.com).

Now, to send a tweet from my Mac, I just do this:

    1. press `command-space`
    2. type `tweet blah blah blah blah blah`
    3. press `Enter`

_kickinrad_, no?

FYI, here are my Alfred Extension settings to make it work:

 * http://drktd.com/C5eT
 * http://drktd.com/C4Nx


CLI Usage
---------

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

(setup.py will prompt you to register your own Application on Twitter.)