# -*- coding: utf-8 -*-
# 作者  gongxc   
# 日期 2020/8/20  17:32 
# 文件  redisUtil
import redis

redisInfo = {
    "host": 'r-2ze18cur7pi0rs0wih.redis.rds.aliyuncs.com',
    "password": 'r-2ze18cur7pi0rs0wih',
    "port": 6379,
    "db": 0
}


class RedisUtil:
    def __init__(self):
        if not hasattr(RedisUtil, 'pool'):
            RedisUtil.create_pool()
        self._connection = redis.Redis(connection_pool = RedisUtil.pool)


    @staticmethod
    def create_pool():
        RedisUtil.pool = redis.ConnectionPool(host=redisInfo['host'], password=redisInfo['password'],
                                            port=redisInfo['port'], db=redisInfo['db'])






    """
    string类型 {'key':'value'} redis操作
    """
    def set_data(self,key, value, time=None):
        # 非空即真非0即真
        if time:
            res = self._connection.setex(key, value, time)
        else:
            res = self._connection.set(key, value)
        return res


    def get_data(self, key):
        res = self._connection.get(key)
        if res !=None:
            return res.decode()
        else:
            return res

    def del_data(self, key):
        res = self._connection.delete(key)
        return res

    """
    hash类型，{'name':{'key':'value'}} redis操作
    """

    def set_hash_data(self, name, key, value):
        res = self._connection.hset(name, key, value)
        return res

    def get_hash_data(self, name, key=None):
        # 判断key是否我为空，不为空，获取指定name内的某个key的value; 为空则获取name对应的所有value
        if key:
            res = self._connection.hget(name, key)
        else:
            res = self._connection.hgetall(name)
        return res

    def del_hash_data(self, name, key=None):
        if key:
            res = self._connection.hdel(name, key)
        else:
            res = self._connection.delete(name)
        return res



if __name__ == '__main__':
    opr = RedisUtil()
    print(opr.get_data('1111'))
    res = opr.get_data('{0010157}:20200820:1:362:')
    print(res)


