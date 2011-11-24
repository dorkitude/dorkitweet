# stdlib imports:
import sys
# third-party imports:
import pymongo
from dorkitude_utils.classproperty import classproperty
from dorkitude_utils.string_utils import camel_to_snake
from dstruct import DStruct
# our imports:
pass


connection = pymongo.Connection("localhost", 27017)
db = getattr(connection, "dorkitweet") 


class BaseModel(object):
    """
    """

    @classproperty
    def collection_name(cls):
        return camel_to_snake(cls.__name__)

    @classproperty
    def collection(cls):
        return getattr(db, cls.collection_name)

    def __init__(self, document=None):

        if not document:
            document = {}

        if "_saved" not in document:
            document["_saved"] = False

        self.storage = document

    def after_save(self):
        pass

    def before_save(self):
        pass

    def __repr__(self):
        return repr(self.storage)

    @classproperty
    def required_attributes(cls):
        return []

    def confirm_required_attributes(self):
        for key in self.__class__.required_attributes:
            if key not in self.storage:
                raise MissingRequiredAttributeError(self, key)

    def delete(self):
        self.__class__.collection.remove(
            self.storage["_id"],
            safe=True)

    def save(self):
        self.before_save()

        # make sure everything's in place
        self.confirm_required_attributes()

        # set the _saved param:
        self.storage["_saved"] = True

        # save it to mongo:
        self.__class__.collection.save(to_save=self.storage, safe=True)

        self.after_save()
        return self

    @classmethod
    def select_one(cls, criteria=None, demand_existence=False):
        if not criteria:
            criteria = {}
        
        cursor = cls.collection.find(criteria)

        if cursor.count() > 0:
            return cls(cursor[0])
        else:
            if demand_existence:
                raise EmptySelectError(cls, criteria)
            else:
                return None

    @classmethod
    def select(cls, criteria=None):
        if not criteria:
            criteria = {}

        collection = getattr(db, cls.collection_name)
        cursor = collection.find(criteria)
        return [cls(document) for document in cursor]

    @classmethod
    def get_all(cls):
        return cls.select({})


class ModelWithDefaultMixin(object):
    """
    """

    @classmethod
    def get_default(cls):

        criteria = {"default": True}

        apps = cls.select(criteria)

        if len(apps) is 0:
            raise NoDefaultExistsError(cls)
        elif len(apps) is 1:
            return apps[0]
        else:
            raise TooManyDefaultsExistError(cls)


class NoDefaultExistsError(Exception):
    def __init__(self, clazz):
        msg = "Run setup.py to configure a {}.".format(clazz.__name__)
        super(self.__class__, self).__init__(msg)


class TooManyDefaultsExistError(Exception):
    def __init__(self, clazz):
        msg = "DB state is effed: {}.".format(clazz.__name__)
        super(self.__class__, self).__init__(msg)


class EmptySelectError(Exception):
    def __init__(self, clazz, criteria):
        msg = "Couldn't find a {} with this criteria: {}"
        msg = msg.format(clazz, criteria)
        super(self.__class__, self).__init__(msg)

