import redis
from settings import REDIS_SETTING

redisConnect = redis.Redis(REDIS_SETTING['host'], REDIS_SETTING['port'], REDIS_SETTING['db'], REDIS_SETTING['password'])


class RedisTool:
    @staticmethod
    def hexists(name, key):
        return redisConnect.hexists(name, key)

    @staticmethod
    def hget(name, key):
        return redisConnect.hget(name, key)

    @staticmethod
    def getset(name, value):
        return redisConnect.getset(name, value)

    @staticmethod
    def hdel(name, *keys):
        return redisConnect.hdel(name, *keys)

    @staticmethod
    def hgetall(name):
        return redisConnect.hgetall(name)

    @staticmethod
    def hkeys(name):
        return redisConnect.hkeys(name)

    @staticmethod
    def hlen(name):
        return redisConnect.hlen(name)

        # Set key to value within hash name Returns 1 if HSET created a new field, otherwise 0

    @staticmethod
    def hset(name, key, value):
        return redisConnect.hset(name, key, value)

    @staticmethod
    def setex(name, time, value):
        return redisConnect.setex(name, time, value)

    @staticmethod
    def get(name):
        return redisConnect.get(name)

    @staticmethod
    def exists(name):
        return redisConnect.exists(name)

    @staticmethod
    def set(name, value):
        return redisConnect.set(name, value)
