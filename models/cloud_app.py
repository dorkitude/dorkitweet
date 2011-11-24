import re

from .base import BaseModel, ModelWithDefaultMixin
from pycloudapp.cloud import Cloud


class CloudAppAccount(BaseModel, ModelWithDefaultMixin):
    required_attributes = ["username", "password"]


class CloudAppClient(object):

    @classmethod
    def get(cls, account=None):
        if not account:
            account = CloudAppAccount.get_default()

        obj = cls(account)

        return obj

    def __init__(self, account):
        self.account = account

        self.api = Cloud()

        try:
            self.api.auth(
                    self.account.storage["username"],
                    self.account.storage["password"])
        except Exception, e:
            raise CloudAppAuthException(account)

    def shorten_urls(self, words):
        ret = []

        for word in words:
            if re.match("^https?:\/\/\w+\.\w+", word):
                print "\nshortening URL: {}".format(word)
                bookmark = self.api.create_bookmark("", word)
                word = bookmark["url"]
                print "\nshortened to: {}".format(word)

            ret.append(word)

        return ret
 

class CloudAppAuthException(Exception):
    def __init__(self, account):
        msg = ""
        msg += "\nThe account credentials you provided are invalid!"
        msg += "\n    username = {}".format(account.storage["username"])
        msg += "\nRun './setup.py --cloud' to reconfigure your account."

        super(CloudAppAuthException, self).__init__(msg)
