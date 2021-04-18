from django.test import TestCase

from testPlatform.util.mysqlUtil import MysqlUtil
from testPlatform.util.redisUtil import RedisUtil
def test_one():
    redis = RedisUtil()
    print(redis.get_data('{0010157}:20200826:1:361:'))
   # print(redis.set_data('{0010157}:20200826:1:361:','1'))
    #print(redis.get_data('{001050}:20200820:1:362:'))
    #print(redis.set_data('{001059}:20200820:1:362:','10'))
    print(redis.get_data('{001050}:20200820:1:362:'))
    print(redis.get_data('{001059}:20200820:1:362:'))
    print(redis.get_data('{0010157}:20200826:1:361:'))
    print(redis.get_data('{001063}:20200822:1:359:'))
    #print(redis.set_data('{001059}:20200822:1:359:','20'))
    print(redis.get_data('{0311110321}:20200826:1:361:'))
    print(redis.set_data('{0311110321}:20200826:1:361:','0'))
    print(redis.get_data('{0311110321}:20200826:1:361:'))



def test_two():
    #print(MysqlUtil.queryone("select * from biz_user"))
    #print(MysqlUtil.queryall("select * from biz_user where mobile= %s",'13383365763'))
    result = MysqlUtil.execute("update biz_user set mobile = %s,open_id = %s,union_id=%s where mobile = %s",('', '', '', '13383365763'))
    print(result)
    if result==1:
        print('更新成功')
    else:
        print('未授权')

def count():
    redis = RedisUtil()
    #print(redis.set_data('user:buy:count', '100'))
    print(redis.get_data('user:buy:count'))

def get_count():
    redis = RedisUtil()
    print(redis.get_data('{0311110423}:20200830:1:361:'))
    print(redis.get_data('{0311110423}:20200830:1:362:'))
    print(redis.get_data('{0311110422}:20200830:1:361:'))
    print(redis.get_data('{0311110422}:20200830:1:362:'))

get_count()