# -*- coding: utf-8 -*-
# 作者  gongxc   
# 日期 2020/6/16  17:30 
# 文件  common
import datetime

from testPlatform.models import ProjectInfo, TestCaseInfo


def delete_project(id):
    try:
        ProjectInfo.objects.filter(id=id).delete()
        return 'ok'
    except Exception:
        return 'error'


def run_case(id):
    try:
        TestCaseInfo.objects.filter(id=id).update(update_time=datetime.datetime.now(),case_status='1')
        return 'ok'
    except Exception:
        return 'error'

def get_ajax_msg(msg, success):
    """
    ajax提示信息
    :param msg: str：msg
    :param success: str：
    :return:
    """
    return success if msg is 'ok' else msg
