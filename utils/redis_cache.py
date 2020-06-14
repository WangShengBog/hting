# -*-coding: UTF-8 -*-
from datetime import datetime
from functools import wraps
import hashlib
import pickle
import logging

from redis import Redis

__author__ = 'bog'

logger = logging.getLogger(__name__)


class RedisCache(object):
    MAX_EXPIRES = 24 * 60 * 60
    SERIALIZER = pickle
    LOCKER = set()

    def __init__(self, name, host="localhost", port=6379, db=0, max_expires=MAX_EXPIRES):
        self.db = Redis(host=host, port=port, db=db)
        self.name = name
        self.max_expires = max_expires

    def _get_key(self, *keys):
        return ":".join([self.name] + list(keys))

    def _get_data(self, key):
        result = self.db.get(key)
        return None if result == b"None" else result

    def get(self, *keys):
        result = self._get_data(self._get_key(*keys))
        return self.SERIALIZER.loads(result) if result is not None else result

    def set(self, keys, value, ex=None):
        k = self._get_key(*keys)
        v = self.SERIALIZER.dumps(value)
        if ex is None:
            self.db.set(k, v)
        else:
            self.db.setex(k, v, ex)

    def delete(self, *keys):
        self.db.delete(self._get_key(*keys))

    @staticmethod
    def build_key(name, *args, **kwargs):
        m = hashlib.md5()
        m.update(name.encode("utf-8"))
        m.update(pickle.dumps(args))
        m.update(pickle.dumps(kwargs))
        return m.hexdigest()

    def cached(self, key, func, ex=None):
        if ex is None:
            ex = self.max_expires
        min_ttl = self.max_expires - ex
        key = ":".join([self.name, key])
        result = self._get_data(key)
        if result is None and key not in self.LOCKER:
            self.LOCKER.add(key)
            try:
                ttl = self.db.ttl(key)
                if ttl is None or ttl < min_ttl:
                    result = func()
                    if result is not None:
                        result = self.SERIALIZER.dumps(result)
                        try:
                            self.db.setex(key, self.max_expires, result)
                        except:
                            pass
            finally:
                self.LOCKER.remove(key)
        try:
            result = self.SERIALIZER.loads(result) if result is not None else None
        except:
            from traceback import format_exc
            logger.error(format_exc())
        return result
