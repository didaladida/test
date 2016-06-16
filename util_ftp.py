# -*- encoding:utf-8 -*-
import ftplib
import os
import sys
import socket
import logging
import logging.handlers


# create console handler
logger = logging.getLogger('main')
logger.propagate = False
# 必须设置logger的级别
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.DEBUG)
# create file handler
fileHandler = logging.handlers.RotatingFileHandler(
    'ftp.log', maxBytes=10**6, backupCount=3)
fileHandler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S')
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
# 添加
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)


HOST = '115.28.150.133'  # ftp服务器ip 默认端口
DIRN = 'public'  # 对应的远程目录
CWD = r'E:\python_project\test\ftp_back'  # 本地文件夹本分目录


def collect_files(x, retlist):
    retlist.append(x.split())


def main():
    try:
        f = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror), e:
        logger.error('ERROR:cannot reach "%s" ' % HOST)
        return
    logger.info('connected to host "%s" ' % HOST)

    try:
        f.login()
    except ftplib.error_perm:
        logger.error('cannot login anonymously')
        f.quit()
        return
    logger.info('login success "%s"' % HOST)
    try:
        # 把当前的工作目录设置为path
        f.cwd(DIRN)
    except ftplib.error_perm:
        logger.error('cannot cd to "%s"' % DIRN)
        f.quit()
        return
    logger.info('change dir to "%s"' % DIRN)
    # 获取文件夹下目录 与本地文件进行比较如果本地不存在或者版本比较旧
    # 则下载远程文件
    ftp_files = []
    local_files = [x.decode('gb2312') for x in os.listdir(CWD)]
    f.dir('', lambda X: ftp_files.append(X.split()))
    # print ftp_files
    thesame = True
    for line in ftp_files:
        filename = line[8].decode('utf-8')
        if filename not in local_files:
            thesame = False
            logger.info('downloading "%s"' % filename)
            try:
                func = open(os.path.join(CWD, filename), 'wb').write
                f.retrbinary('RETR %s' % filename.encode('utf-8'), func)
            except ftplib.error_perm:
                logger.error('cannot read file "%s"' % filename)
                os.unlink(filename)
    if thesame:
        logger.info(u'已经同步')
    f.quit()
    return

if __name__ == '__main__':
    main()
