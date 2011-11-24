# stdlib imports:
pass
# third-party imports:
import tweepy
# our imports:
from base import BaseModel, ModelWithDefaultMixin
from dorkitude_utils.classproperty import classproperty
from .cloud_app import CloudAppClient

class TwitterApplication(BaseModel, ModelWithDefaultMixin):
    """
    """
    required_attributes = ["consumer_key", "consumer_secret"]


class TwitterAccount(BaseModel):

    required_attributes = [
            "id",
            "name",
            "full_name",
            "access_key",
            "access_secret"]

    @property
    def application(self):
        return TwitterApplication.get_default()

    @classmethod
    def get_by_name(cls, name, demand_existence=False):
        criteria = {"name": name}
        return cls.select_one(criteria, demand_existence=demand_existence)

    def before_save(self):

        if self.__class__.get_by_name(self.storage["name"]):
            raise self.__class__.AccountAlreadyExists(self)


    class AccountAlreadyExists(Exception):
        pass


class Tweet(BaseModel):

    @classproperty
    def cloud_app_client(cls):
        if not hasattr(cls, "_cloud_app_client"):
            cls._cloud_app_client = CloudAppClient.get()
        return cls._cloud_app_client

    @property
    def account(self):
        return TwitterAccount.get_by_name(self.storage["account_name"])

    @classmethod
    def create(cls, account, body_words=None, body=None, shorten_urls=True):
        """

        :param body:  String.
        :param account:  TwitterAccount.
        :param shorten_urls:  Boolean.

        """

        if not body_words:
            if body:
                body_words = body.split(" ")
            else:
                raise Exception("You must provide body or body_words")

        if shorten_urls:
            body_words = cls.cloud_app_client.shorten_urls(body_words)

        body = " ".join(body_words)

        tweet = cls({
            "body": body,
            "account_name": account.storage["name"],
            "sent": False,
            })

        tweet.save()
        return tweet

    def send(self):
        """
        Send this tweet!
        """
        # Figure out the twitterh andle:
        auth = tweepy.OAuthHandler(
                str(self.account.application.storage["consumer_key"]),
                str(self.account.application.storage["consumer_secret"]))

        auth.set_access_token(
                self.account.storage["access_key"], 
                self.account.storage["access_secret"])

        api = tweepy.API(auth)
        sent = api.update_status(self.storage["body"])

        self.storage["sent"] = True
        self.storage["id"] = sent.id
        self.storage["final_text"] = sent.text
        self.storage["created_at"] = sent.created_at
        self.save()

        return self
