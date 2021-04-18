# -*- coding: utf-8 -*-
# 作者  gongxc   
# 日期 2020/8/21  11:01 
# 文件  mysqlUtil
import traceback
import pymysql
from testPlatform.util.loggerUtil import logger


class MysqlUtil:
    @staticmethod
    def _connect_mysql():
        try:
            load_dict = {
                          "host": "xiaoxinqa.mysql.polardb.rds.aliyuncs.com",
                          "user": "xiaoxin_qa_devep",
                          "password": "!1qaz@2wsx",
                          "db": "c_user_center",
                          "charset": "utf8",
                          "port": 3306
                        }
            return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **load_dict)
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("cannot create mysql connect")

    @classmethod
    def queryone(cls,sql, param=None):
        """
        返回结果集的第一条数据
        :param sql: sql语句
        :param param: string|tuple|list
        :return: 字典列表 [{}]
        """
        con = cls._connect_mysql()
        cur = con.cursor()

        row = None
        try:
            cur.execute(sql, param)
            row = cur.fetchone()
        except Exception as e:
            con.rollback()
            logger.error(traceback.format_exc())
            logger.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return cls._simple_value(row)

    @classmethod
    def queryall(cls,sql, param=None):
        """
        返回所有查询到的内容 (分页要在sql里写好)
        :param sql: sql语句
        :param param: tuple|list
        :return: 字典列表 [{},{},{}...] or [,,,]
        """
        con = cls._connect_mysql()
        cur = con.cursor()

        rows = None
        try:
            cur.execute(sql, param)
            rows = cur.fetchall()
        except Exception as e:
            con.rollback()
            logger.error(traceback.format_exc())
            logger.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return cls._simple_list(rows)

    @classmethod
    def insertmany(cls,sql, arrays=None):
        """
        批量插入数据
        :param sql: sql语句
        :param arrays: list|tuple [(),(),()...]
        :return: 入库数量
        """
        con = cls._connect_mysql()
        cur = con.cursor()

        cnt = 0
        try:
            cnt = cur.executemany(sql, arrays)
            con.commit()
        except Exception as e:
            con.rollback()
            logger.error(traceback.format_exc())
            logger.error("[sql]:{} [param]:{}".format(sql, arrays))

        cur.close()
        con.close()
        return cnt

    @classmethod
    def insertone(cls,sql, param=None):
        """
        插入一条数据
        :param sql: sql语句
        :param param: string|tuple
        :return: id
        """
        con = cls._connect_mysql()
        cur = con.cursor()

        lastrowid = 0
        try:
            cur.execute(sql, param)
            con.commit()
            lastrowid = cur.lastrowid
        except Exception as e:
            con.rollback()
            logger.error(traceback.format_exc())
            logger.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return lastrowid

    @classmethod
    def execute(cls,sql, param=None):
        """
        执行sql语句:修改或删除
        :param sql: sql语句
        :param param: string|list
        :return: 影响数量
        """
        con = cls._connect_mysql()
        cur = con.cursor()

        cnt = 0
        try:
            cnt = cur.execute(sql, param)
            con.commit()
        except Exception as e:
            con.rollback()
            logger.error(traceback.format_exc())
            logger.error("[sql]:{} [param]:{}".format(sql, param))

        cur.close()
        con.close()
        return cnt

    @staticmethod
    def _simple_list(rows):
        """
        结果集只有一列的情况, 直接使用数据返回
        :param rows: [{'id': 1}, {'id': 2}, {'id': 3}]
        :return: [1, 2, 3]
        """
        if not rows:
            return rows

        if len(rows[0].keys()) == 1:
            simple_list = []
            # print(rows[0].keys())
            key = list(rows[0].keys())[0]
            for row in rows:
                simple_list.append(row[key])
            return simple_list
        return rows

    @staticmethod
    def _simple_value(row):
        """
        结果集只有一行, 一列的情况, 直接返回数据
        :param row: {'count(*)': 3}
        :return: 3
        """
        if not row:
            return None

        if len(row.keys()) == 1:
            # print(row.keys())
            key = list(row.keys())[0]
            return row[key]
        return row