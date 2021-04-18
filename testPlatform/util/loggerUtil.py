# -*- coding: utf-8 -*-
# 作者  gongxc   
# 日期 2020/8/21  10:46 
# 文件  loggerUtil
import logging
import logging.handlers

log_file = 'output.log'
fmt = '%(asctime)s - %(levelname)s - %(filename)s#%(funcName)s():%(lineno)s - %(name)s - %(message)s'

# 实例化handler
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)     # 为handler添加formatter
logger = logging.getLogger("main")  # 获取名为tst的logger
logger.addHandler(handler)          # 为logger添加handler
logger.setLevel(logging.DEBUG)      # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'


if __name__ == '__main__':
    logger.debug("first message debug")
    logger.info("first message info")
    logger.warning("first message warning")
    logger.error("first message error")
    logger.critical("first message critical")