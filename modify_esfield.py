#!/data/xiaoju/tools/anaconda/bin/python
# -*- encoding:utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch import ConnectionError
from elasticsearch import NotFoundError
from elasticsearch.helpers import BulkIndexError
import codecs
import sys
from elasticsearch import helpers
import random

import time
import MySQLdb
import logging
import logging.handlers

totalcnt = 0
totalall = 0

es_logger = logging.getLogger('elasticsearch')
es_logger.propagate = False
es_logger.setLevel(logging.INFO)
es_logger_handler = logging.handlers.RotatingFileHandler('top-camps-base.log', maxBytes=0.5*10**9, backupCount=3)

es_logger.addHandler(es_logger_handler)

es_tracer = logging.getLogger('elasticsearch.trace')
es_tracer.propagate = False
es_tracer.setLevel(logging.DEBUG)
es_tracer_handler=logging.handlers.RotatingFileHandler('top-camps-full.log', maxBytes=0.5*10**9, backupCount=3)
es_tracer.addHandler(es_tracer_handler)

logger = logging.getLogger('mainLog')
logger.propagate = False
logger.setLevel(logging.DEBUG)
# create file handler
fileHandler = logging.handlers.RotatingFileHandler('top-camps.log', maxBytes=10**6, backupCount=3)
fileHandler.setLevel(logging.INFO)
# create console handler
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)


def info_parse(line):
    """
    :param line:原始文件中待写入的数据部分
    :return: 返回拼接好的es 字典
    """
    """
    :param line:
    :return:
    """
    row = line.strip().split('\t')
    raw_cscore = int(row[0])
    cscore = float(row[1])
    score = {}
    score['raw_cscore'] = raw_cscore
    score['cscore'] = cscore
    return score


def batch_update(infile, num, host_port='localhost:9200'):
    """
    :param infile:更新的文件,按城市，line格式： poiid\tcscore\traw_score
    :param num: 一次批量操作数量，默认500，超过500需要改es设置，网上有人说超过500会出错

    :param host_port: host and port
    :return: none
    """
    # 文件名
    global totalcnt,totalall
    indexname = "didi_poi_1"
    typename = "didi_score"
    logger.info("start: %s" % infile)
    logger.info("indexname: %s" % indexname)
    logger.info("type: %s" % typename)
    time_start = time.clock()
    print 'start insert ...'
    print 'modify file name : %s' % infile
    print 'indexname :  %s' % indexname
    print 'typename: %s' % typename
    
    try:
        es = Elasticsearch([host_port])
        # 成功写入计数
        suc_cnt = 0
        # 总计数
        cnt = 0
        with codecs.open(infile, 'r', 'utf-8') as infp:
            infos = []
            for line in infp:
                if not line.strip():
                    continue
                # 通过过滤规则
                cnt += 1
                row = line.strip().split('\t', 1)
                poiid = row[0]
                # 测试：写入不存在id，使用时注释掉
                # if random.random() > 0.999:
                #    print poiid
                #    poiid += '**'

                info = {}
                info['_op_type'] = 'update'
                info['_index'] = indexname
                info['_type'] = typename
                info['_id'] = poiid
                doc = info_parse(row[1])
                info['doc'] = doc
                # 加入操作集合
                infos.append(info)
                if len(infos) == num:
                    try:
                        # stats_only 显示成功数量，出错不报告，msg =(num_suc,num_fail)
                        msg = helpers.bulk(es, infos, raise_on_error=False, stats_only=True)
                        suc_cnt += msg[0]
                        del infos[0:len(infos)]
                    except BulkIndexError as e:
                        print e
                        print msg
                        pass

            # 不足部分
            if len(infos) > 0:
                try:
                    # stats_only 显示成功数量，出错不报告，msg =(num_suc,num_fail)
                    msg = helpers.bulk(es, infos, raise_on_error=False, stats_only=True)
                    suc_cnt += msg[0]
                    del infos[0:len(infos)]
                except BulkIndexError as e:
                    print e
                    print msg
                    pass

            print 'insert complete'
            print " "*10
            print suc_cnt, cnt

            logger.info("all: %d\tsuc: %d" %(cnt,suc_cnt))

            if cnt!=suc_cnt:
                print "*"*20
                logger.info("failed: %d" % (cnt-suc_cnt))
                print "warning  city %d" % id
                print "*"*20
            print " "*10
    except ConnectionError:
        logger.error('ConnectionError \n exit \n')
        exit(-1)
    except Exception as e:
        print e
        exit(-1)
    time_end = time.clock()
    time_gap = time_end - time_start
    logger.info("spend time sec: %.6f" % time_gap)

if __name__ == "__main__":
    
    #logger.basicConfig(filename='update_es.log',level=logger.DEBUG,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
    # 修改城市号
    batch_update("cal_3_score_10000", 500)

    print 'total suc:%d' % totalcnt 
    logger.info("total suc: %d \t totalZ: %d" % (totalcnt,totalall))
    print 'total: %d' % totalall

