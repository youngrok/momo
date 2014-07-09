from bson.objectid import ObjectId
import math


class ObjectNotFound(Exception):
    pass

class ModelException(Exception):
    pass

class Model(dict):
    collection = None

    @classmethod
    def find_by_id(cls, object_id):
        try:
            return cls(cls.collection.find_one(by_id(object_id)))
        except:
            raise ObjectNotFound('%s not found.' % cls.__name__)

    @classmethod
    def find_one(cls, spec={}, *args, **kwargs):
        obj = cls.collection.find_one(spec, *args, **kwargs)
        if obj:
            return cls(obj)
        else:
            raise ObjectNotFound('%s not found.' % cls.__name__)

    @classmethod
    def find_raw(cls, spec={}, *args, **kwargs):
        return cls.collection.find(spec, *args, **kwargs)

    @classmethod
    def find(cls, spec={}, *args, **kwargs):
        result = []
        for obj in cls.collection.find(spec, *args, **kwargs):
            result.append(cls(obj))
        return result

    @classmethod
    def create(cls, data):
        _id = cls.collection.insert(data)
        obj = cls.collection.find_one({'_id':_id})
        return cls(obj)

    @classmethod
    def get_or_create(cls, data):
        if cls.find(data).count():
            return cls.find_one(data)

        _id = cls.collection.insert(data)
        obj = cls.collection.find_one({'_id':_id})
        return cls(obj)

    def save(self):
        self.collection.save(self)

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value;

def by_id(object_id):
    return {'_id':ObjectId(object_id)}

def distance(source, target):
    dis = math.sqrt(math.pow((source['latitude']-target['latitude']), 2)+math.pow((source['longitude']-target['longitude']), 2))
    return round(dis*1110) / 10.0