#!/usr/bin/env python
# coding: utf-8 
import sys
from Queue import Queue
from datetime import *
from os.path import getsize
from ftplibex import DirEntry
from ftplibex import DirScanner
import ftplib
import paramiko
import os
import re
import threading
import time
import logging
import Logger

files_cnt = 0
consumer_cnt = 8
logger = None

'''
**********************************************************************
* class_name   : CSFTP
* description  : SFTP Wrapper
* author       : Chris Zhang
**********************************************************************
'''

class CSFTP:
    # 构造函数.
    def __init__(self, sftp_info,file_regex):
        try:
            logger.log(logging.ERROR, 'file_regex: ' + file_regex)
            self.file_regex = file_regex
            self.connect(sftp_info['ip'], sftp_info['port'])
            self.login(sftp_info['user'], sftp_info['passwd'], '')
        except Exception, msg:
            logger.log(logging.ERROR, 'fail to connect/login : %s' % ( msg[0] ))
            self.sftp = None
            self.t = None

    def connect(self, host='', port=''):
        if host:
            self.host = host
        if port:
            self.port = port
        # paramiko 是 python的 ssh 连接库.
        self.t = paramiko.Transport((self.host, self.port))

    def login(self, user='', passwd='', acct=''):
        self.t.connect( username = user, password = passwd )
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

    def is_ok(self):
        return self.sftp != None
    
    def cwd(self, path):
        try:
            self.sftp.chdir( path )
            return True
        except Exception, msg:
            logger.log(logging.ERROR, 'fail to execute cwd : %s' % ( msg[0] ))
            return False

    def nlst(self):
        dir_attrs = self.sftp.listdir_attr()
        d = DirScanner()
        for attr in dir_attrs:
            att = unicode(attr).encode('utf-8')
            d.addline( str(att) )

        files = []
        for key, value in d.items():
            files.append(key)        
        return files

    '''
    def is_filesize_equal(self, remote_name, local_name ):
        if os.path.isfile( local_name ):
            remote_size = self.size( remote_name )
            local_size = os.stat( local_name ).st_size
            
            if remote_size == local_size : 
                return True
            else:
                return False
        else:
            return False
    '''
    
    def pwd(self):
        cwd = self.sftp.getcwd()
        if type(cwd) is unicode:
            cwd = cwd.encode('utf-8')
        return cwd

    '''
    def size(self, file):
        fr = self.sftp.file(file, 'rb')
        file_size = self.sftp.stat(file).st_size 
        fr.close()
        return file_size
    '''

    def retrbinary(self, remote_name, local_name=''):
        try:
            if local_name == "":
                logger.log(logging.ERROR,  "local file name is null!" )
                return False
            elif ( os.path.isfile( local_name ) is not True ) and os.path.isdir( local_name ):
                logger.log(logging.ERROR,  "localdir is not valid format!" )
                pass
                
            self.sftp.get( remote_name, local_name )
            return True
        except Exception, msg:
            logger.log(logging.ERROR, msg[0])
            return False

    def __del__(self):
        if self.sftp is not None:
            self.sftp.close()
        if self.t is not None:
            self.t.close()

'''
**********************************************************************
* class_name   : CFTP
* description  : FTP Wrapper
* author       : Chris Zhang
**********************************************************************
'''
class CFTP:
    def __init__(self, ftp_info):
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(ftp_info['ip'], ftp_info['port'], 30)
        except Exception, msg:
            logger.log(logging.ERROR,  'fail to connect to(%s:%s) : errcode(%s),errmsg(%s)' % ( ftp_info['ip'], ftp_info['port'], msg[0],msg[1] ))
            self.ftp = None
            return

        try:
            self.ftp.login(ftp_info['user'], ftp_info['passwd'])
        except Exception, msg:
            logger.log(logging.ERROR,  'fail to login : %s' % ( msg[0] ))
            self.ftp.close()
            self.ftp = None

    def is_ok(self):
        return self.ftp != None
    
    def cwd(self, d):
        try:
            self.ftp.cwd(d)
            return True
        except Exception, msg:
            logger.log(logging.ERROR, 'fail to execute cwd : %s' % ( msg[0] ))
            return False

    def nlst(self):
        try:
            return self.ftp.nlst()
        except:
            return []

    def pwd(self):
        return self.ftp.pwd()

    def retrbinary(self, command, callback):
        try:
            self.ftp.retrbinary(command, callback)
            return True
        except Exception, msg:
            logger.log(logging.ERROR, msg[0])
            logger.log(logging.ERROR, msg[1])
            return False

    '''  
    def size(self, f):
        return self.ftp.size(f)
    '''

    def __del__(self):
        if self.ftp != None:
            self.ftp.close()
            self.ftp = None

'''
**********************************************************************
* class_name   : CTimeUtil
* description  : time process class
* author       : Chris Zhang
**********************************************************************
'''
class CTimeUtil:
    '''
    func_name    : getndaysfromtoday
    description  : get day when is the day before n days
    param_in     : n is plus or negative
    return_value : if successful, return the day with format "yyyy-MM-dd"; else return ""
    author       : Chris Zhang
    '''
    @staticmethod
    def getndaysfromtoday(n = 0):
        try:
            # current date
            curr_date = '%d-%02d-%02d' % (datetime.now().year,
                                          datetime.now().month,
                                          datetime.now().day)
            offset = n * 86400 # n days
            d = time.localtime(time.mktime(time.strptime(curr_date, '%Y-%m-%d')) + offset)
            return '%d-%02d-%02d' % (d[0], d[1], d[2])
        except:
            return ''

    @staticmethod
    def getndaysfromlocalday(localday,n):
        try:
            offset = n * 86400 # n days
            d = time.localtime(time.mktime(time.strptime(localday, '%Y-%m-%d')) + offset)
            return '%d-%02d-%02d' % (d[0], d[1], d[2])
        except:
            return ''
        
    @staticmethod
    def timestr_to_secs(s):
        return time.mktime(time.strptime(s, '%Y%m%d%H%M%S'))

    @staticmethod
    def secs_to_str(secs, fmt = '%Y-%m-%d %H:%M:%S'):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(secs))

    
    def timestr_to_nrangesecs(s = time.strftime('%Y%m%d%H%M%S'), n = 0):
        global logger
        try:
            t1 = float(CTimeUtil.timestr_to_secs(s))
            t2 = t1 + float(n * 3600)
            if t1 < t2:
                return [t1, t2]
            else:
                return [t2, t1]
        except Exception, msg:
            logger.log(logging.ERROR, msg[0])
            return [0.0, 0.0]                  

'''
**********************************************************************
* class_name   : CProducerThread
* description  : traverse all the files to download, put them into queue
* author       : Chris Zhang
**********************************************************************
'''
class CProducerThread(threading.Thread):
    def __init__(self, name, nds_info, queue):
        threading.Thread.__init__(self)
        self.info   = nds_info
        self.data   = queue
        self.name   = name
        self.downloadRecordMap = {}

    # 线程入口
    def run(self):
        logger.log(logging.INFO, 'Start' )            
        if self.info['ftp']['downloadtype'].lower()=='sftp':
            self.ftp = CSFTP(self.info['ftp'],self.info['data_type']['File_Regex'])
        elif self.info['ftp']['downloadtype'].lower()=='ftp':
            self.ftp = CFTP(self.info['ftp'])
        else:
            logger.log(logging.ERROR,  'downloadtype invalid! ' )
            return
        self.connectServer()
        self.lookup_files()

    # 连接服务器
    def connectServer(self):
        try_cnt = 0
        while (self.ftp.is_ok() == False and try_cnt < 3):
            if self.info['ftp']['downloadtype'].lower()=='sftp':
                self.ftp = CSFTP(self.info['ftp'],self.info['data_type']['File_Regex'])
            elif self.info['ftp']['downloadtype'].lower()=='ftp':
                self.ftp = CFTP(self.info['ftp'])
            try_cnt += 1
            if self.ftp.is_ok() == True:
                logger.log(logging.INFO,  self.info['ftp']['downloadtype'] + ' is able finally' )
                break

        if(try_cnt > 3):
            logger.log(logging.ERROR, "Fail to connect server!")

    def __del__(self):
        logger.log(logging.INFO, 'End')

    '''
    func_name    : lookup_files
    description  : retrieve all the files which are needed to download
    param_in     : 
    return_value : 
    author       : Chris Zhang
    '''    
    def lookup_files(self):
        
        logger.log(logging.INFO,  'lookup_files' )

        # 如果 ftp 没有连接上， 进行连接
        if self.ftp.is_ok() == False:
            logger.log(logging.ERROR, 'Fail to connect to server')
            self.connectServer()

        if self.ftp.cwd(self.info['rdir']) == False:
            logger.log(logging.ERROR, 'Fail to change to dir : %s' % ( self.info['rdir'] ) )
            return

        try:
            #process Fm/Cm data
            if self.info['datatype'] == 0:
                return self.process_fmcm()
            elif self.info['datatype'] == 2:
                return self.process_cmccnorthmr()
            else:
                return self.process_cdtmr()

        except Exception, msg:
            logger.log(logging.ERROR,  'lookup_files : %s' % ( msg[0] ))
            pass

    def  process_cmccnorthmr(self):
        global files_cnt
        for day in self.ftp.nlst():
            logger.log(logging.INFO,  'process_cmccnorthmr day:%s!' % (day))
            if self.day_is_valid(day)  == False:
                logger.log(logging.WARNING,  'Invalid day : %s' % ( day ) )
                continue
            #check whether file counts is more than maxfiles or not
            if self.info['maxfiles'] > 0:
                if files_cnt >= self.info['maxfiles']:
                    logger.log(logging.INFO,  'The files is up to maxfiles!')
                    return
            if self.process_cmccnorthmrday(day) == -2:
                return -2           

    def process_cdtmr(self):
        global files_cnt
        for day in self.ftp.nlst():
            logger.log(logging.INFO,  'process cdt/mr day:%s!' % (day))
            if self.day_is_valid(day) == False:
                logger.log(logging.WARNING,  'Invalid day : %s' % ( day ) )
                continue

            #check whether file counts is more than maxfiles or not
            if self.info['maxfiles'] > 0:
                if files_cnt >= self.info['maxfiles']:
                    logger.log(logging.INFO,  'The files is up to maxfiles!')
                    return
            if self.process_day(day) == -2:
                return -2

    def process_fmcm(self):
        global files_cnt
        logger.log(logging.ERROR,  'begin nlst file name ')
        for file in self.ftp.nlst():
            logger.log(logging.ERROR,  'Remote file name : %s' % ( file ))
            if self.is_needtodownload_file(file) == False:
                logger.log(logging.ERROR,  'Invalid file : %s' % ( file ) )
                continue

            if self.info['maxfiles'] > 0:
                if files_cnt >= self.info['maxfiles']:
                    logger.log(logging.INFO,  'The files is up to maxfiles!')
                    return -2

            IPdir = self.info['backdir'] + os.sep + self.info['ftp']['ip'] + "_" + str(self.info['ftp']['port'])
            Item = [self.ftp.pwd(), file]

            if self.is_existPartFile(Item) == True:
                logger.log(logging.ERROR,  'is_existPartFile : %s' % ( file ))
                continue
            if self.is_downloaded(Item, IPdir) == True:
                logger.log(logging.ERROR,  'is_downloaded : %s' % ( file ))
                continue
            else:
                #logger.log(logging.INFO,  'Add file to queue : %s' % ( file ) )
                self.append_queue(file)
                files_cnt += 1
        return 0

    def day_is_valid(self, day):
        return ( day in self.info['valid_day'] )

    '''
    func_name    : process_day
    description  : process date dir
    param_in     : day - date dir name
    return_value : 0  success;
                   -1 failed to change dir to type dir;
                   -2 failed to leave type dir 
    author       : Chris Zhang
    '''
    def process_cmccnorthmrday(self, day):
        global files_cnt
        cwd = self.ftp.pwd()
        cwd = unicode(self.ftp.pwd(), 'utf-8').encode( self.info['data_type']['Encoding'] )
        logger.log(logging.INFO, 'process_cmccnorthmrday: --> %s' % ( cwd ) )
        if self.ftp.cwd(day) == False:
            logger.log(logging.ERROR,  'process_cmccnorthmrday: fail to change to dir : %s' % ( day ) )
            return -1
        try:
            for filename in self.ftp.nlst():
                #处理单个中移北向MR文件
                re = self.ProcessACDTMRFile(filename)
                if (re == -2):
                   return -2
                logger.log(logging.INFO, 'process_cmccnorthmrday: <-- ..' )

        except Exception, msg:
            logger.log(logging.ERROR,  'process_cmccnorthmrday : %s' % ( msg[0] ) )
            pass
        if self.ftp.cwd('..') == False:
            logger.log(logging.ERROR,  'fail to change to dir : ..')
            return -2
        return 0         
        
    def process_day(self, day):
        global files_cnt
        cwd = self.ftp.pwd()
        cwd = unicode(self.ftp.pwd(), 'utf-8').encode( self.info['data_type']['Encoding'] )
        logger.log(logging.INFO, 'process_day: --> %s' % ( cwd ) )

        if self.ftp.cwd(day) == False:
            logger.log(logging.ERROR,  'process_day: fail to change to dir : %s' % ( day ) )
            return -1

        try:
            for filetype in self.ftp.nlst():
                logger.log(logging.INFO,  'process_day: test Dir --> %s' % ( filetype) )
                if self.is_valid_CDTMRDirType(filetype) == False:
                    continue
                logger.log(logging.INFO,  'process_day: process Dir --> %s' % ( filetype) )
                if self.ftp.cwd(filetype) == False:
                    logger.log(logging.ERROR,  'process_day: fail to change to filetype dir : %s' % ( filetype ) )
                    return -1
                for subdirname in self.ftp.nlst():
                    logger.log(logging.INFO,  'process_day: test cdt/mr sub date Dir --> %s' % ( subdirname) )
                    if self.is_valid_CDTMRSUBDateDir(subdirname) == False:
                        continue
                    logger.log(logging.INFO,  'process_day: process cdt/mr sub date Dir --> %s' % ( subdirname) )                    
                    if self.ftp.cwd(subdirname) == False:
                        logger.log(logging.ERROR,  'process_day: fail to change to subdir : %s' % ( subdirname ) )
                        return -1
                    for filename in self.ftp.nlst():
                        re = self.ProcessACDTMRFile(filename)
                        if (re == -2):
                            return -2
                    logger.log(logging.INFO, 'process_day: <-- ..' )
                    if self.ftp.cwd('..') == False:
                        logger.log(logging.ERROR,  'fail to change to: .. from subdir')
                        return -2
                logger.log(logging.INFO, 'process_day: <-- ..' )
                if self.ftp.cwd('..') == False:
                    logger.log(logging.ERROR,  'fail to change to dir : ..')
                    return -2

        except Exception, msg:
            logger.log(logging.ERROR,  'process_day : %s' % ( msg[0] ) )
            pass
        logger.log(logging.INFO, '<-- ..' )
        if self.ftp.cwd('..') == False:
            logger.log(logging.ERROR,  'process_day: fail to change to dir : ..')
            return -2

        return 0



    def is_valid_CDTMRSUBDateDir(self,fname):
        logger.log(logging.DEBUG,  'is_valid_CDTMRSUBDateDir chekc file : %s' % ( fname ) )
        try:
            #2014-12-21_12-23-21
            pattern_str = '^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$'
            pattern = re.compile(pattern_str)
            isMatched = pattern.match(fname)
            return ( isMatched != None )
        except Exception, msg:
            return False
    def ProcessACDTMRFile(self,fname):
        global files_cnt
        if self.is_valid_file(fname) == False:
            logger.log(logging.ERROR,  'process_day: Invalid file : %s' % ( fname ) )
            return -1
        if self.info['maxfiles'] > 0:
            if files_cnt >= self.info['maxfiles']:
                logger.log(logging.INFO,  'The files is up to maxfiles!')
                return -2
        IPdir = self.info['backdir'] + os.sep + self.info['ftp']['ip'] + "_" + str(self.info['ftp']['port'])
        Item = [self.ftp.pwd(), fname]
        if self.is_existPartFile(Item) == True:
            return 1
        if self.is_downloaded(Item, IPdir) == True:
            return 2
        else:
            self.append_queue(fname)
            files_cnt += 1
        return 0

    '''
    func_name    : is_valid_CDTMRDirType
    description  : CDT/MDT/MR/north MR 
    0 CM/PM
    1 CDT/MR/MDT 
    2 NorthMR
    param_in     : fname - filename
    return_value : true - match; false - unmatch
    author       : Chris Zhang
    ''' 
    def is_valid_CMCCNORTHMRDirType(self,fname):
        try:
            pattern_str = '^[0-9]+$'
            pattern = re.compile(pattern_str)
            isMatched = pattern.match(fname)
            return ( isMatched != None )
        except Exception, msg:
            return False    
    def is_valid_CDTMRDirType(self,fname):
        try:
            pattern_str = '^(MR|MDT|CDT)$'
            pattern = re.compile(pattern_str)
            isMatched = pattern.match(fname)
            return ( isMatched != None )
        except Exception, msg:
            return False
        

    '''
    func_name    : is_valid_file
    description  : file format is right or not  
    param_in     : fname 
    return_value : true - match; false - unmatch
    author       : Chris Zhang
    ''' 
    def is_valid_file(self,fname):
        try:
            pattern_str = self.info['data_type']['File_Regex']
            pattern = re.compile(pattern_str)
            isMatched = pattern.match(fname)
            return ( isMatched != None )
        except Exception, msg:
            return False
    
    def is_needtodownload_file(self,fname):
        try:
            file_regex = self.info['data_type']['File_Regex']
            date_regex = self.info['data_type']['Date_Regex'] # 时间戳格式为 201502041200
            date_format = self.info['data_type']['Date_Format']
            validDay = self.info['data_type']['valid_day']

            pattern = re.compile(file_regex)
            isMatched = pattern.match(fname)            
            if(isMatched == None):
                logger.log(logging.ERROR,  'isMatched none ' +fname + ' regex ' + file_regex  )
                return False

            if(date_regex == ''):                
                return True
            if re.search(date_regex, fname) is not None:
                datelist = re.findall(date_regex, fname)
                strdate = datelist[len(datelist)-1]
            else:
                logger.log(logging.ERROR,  'isMatched list none ' +fname )
                return False

            #filedate = "%s-%s-%s" % (strdate[0:4],strdate[4:6],strdate[6:8])

            day = time.strptime(strdate, date_format)
            logger.log(logging.INFO,  '%s  day' % day )
            d = '%d-%02d-%02d' % (day[0], day[1], day[2])
            return ( d in validDay )
        except Exception, msg:
            logger.log(logging.ERROR,  'EXCEPTION happen in is_needtodownload_file' )
            return False

    '''
    func_name    : append_queue
    description  : append file name to queue
    param_in     : fname 
    return_value : 
    author       : Chris Zhang
    ''' 
    def append_queue(self, fname):
        logger.log(logging.INFO,  'append_queue:%s'%(fname) )
        try:
            if self.info['datatype'] == 0:
                fdir = self.info['rdir']
            elif self.info['datatype'] == 2:
                curr_dir = self.ftp.pwd().split('/')
                if self.info['rdir'] != '':
                    fdir = '%s/%s' % ( self.info['rdir'], curr_dir[-1] )
                else:
                    fdir = '%s' % ( curr_dir[-1] )
            else:
                curr_dir = self.ftp.pwd().split('/')
                if self.info['rdir'] != '':
                    fdir = '%s/%s/%s/%s' % ( self.info['rdir'],curr_dir[-3], curr_dir[-2],  curr_dir[-1] )
                else:
                    fdir = '%s/%s/%s' % (curr_dir[-3],curr_dir[-2], curr_dir[-1] )
            self.data.put([fdir, fname])
        except Exception, msg:
            logger.log(logging.ERROR,  'append_queue : ' % (msg[0]))

    '''
    func_name    : is_existPartFile
    description  : whether the file exist in tmp_index directory or not
    param_in     : item - downloaded file path and filename
                 : IPdir- record the downloaded files
    return_value : True: downloaded, False: not
    '''
    def is_existPartFile(self, item):
        flag = False
        if self.info['datatype'] == 0:
            dfile = '%s/%s' % (self.info['ldir'], item[1])
        elif self.info['datatype'] == 2:
            splitFmt = '&'
            dirlevel = item[0].split('/')
            date = dirlevel[len(dirlevel)-1]
            dfile = '%s/%s%s%s' % (self.info['ldir'], date,splitFmt,item[1] )
            
        else:
            splitFmt = '&'
            dirlevel = item[0].split('/')
            date = dirlevel[len(dirlevel)-3]
            filetype = dirlevel[len(dirlevel)-2]
            subdatedir = dirlevel[len(dirlevel)-1]
            dfile = '%s/%s%s%s%s%s%s%s' % (self.info['ldir'], date, splitFmt, filetype, splitFmt, subdatedir, splitFmt,item[1] )

        #if the current file exists or not, if exist, do not download
        if ( os.path.exists( dfile ) == True ):
            logger.log(logging.INFO,  '%s has been existed in local dir' % dfile )
            flag = True
        logger.log(logging.INFO, 'check file, is_existPartFile, file path:%s ->%d'%( dfile,flag))
        return flag


    def is_downloaded(self, item, IPdir):
        flag = False
        path_name = item[0] + '/' + item[1] + os.linesep
        if self.info['datatype'] == 0:
            File_Standard = self.info['data_type']['File_Standard']
            backfname = IPdir + os.sep + File_Standard + ".txt"
        elif self.info['datatype'] == 2:
            dirname = item[0].split('/')
            date = dirname[len(dirname)-1]
            backfname = IPdir + os.sep + date + ".txt"
            path_name = item[0] + '/' + item[1] + os.linesep
        else:
            dirname = item[0].split('/')
            date = dirname[len(dirname)-3]
            backfname = IPdir + os.sep + date + ".txt"
            path_name = item[0] + '/' + item[1] + os.linesep
        if(os.path.exists(backfname) == False):
            return flag
        dataFile = open(backfname, "r")
        logger.log(logging.ERROR,  'is_downloaded backlog ' + backfname)
        try:
            if backfname in self.downloadRecordMap:
                lines = self.downloadRecordMap[backfname]
            else:
                lines = dataFile.readlines()#增加一个map来保存读取的内容，不用每个文件都读取csv文件。
                self.downloadRecordMap[backfname] = lines
            if path_name in lines:
                flag = True
        except Exception, msg:
            logger.log(logging.ERROR,  'failed to open file %s ' % (IPdir + os.sep + dirname + ".txt") )
            logger.log(logging.ERROR,  'is_downloaded : %s' % ( msg[0] ))
        finally:
            dataFile.close()
            logger.log(logging.INFO, 'check file, is_downloaded, file path:%s ->%d'%( path_name,flag))            
            return flag

'''
**********************************************************************
* class_name   : CConsumerThread
* description  : download files to the local path
* author       : Chris Zhang
**********************************************************************
'''
class CConsumerThread(threading.Thread):
    def __init__(self, name, nds_info, queue):
        threading.Thread.__init__(self)
        self.info   = nds_info
        self.data   = queue
        self.name   = name

    def run(self):
        global files_cnt
        logger.log(logging.INFO,  'Start' )

        if self.info['ftp']['downloadtype'].lower()=='sftp':
            self.ftp = CSFTP(self.info['ftp'],self.info['data_type']['File_Regex'])
        elif self.info['ftp']['downloadtype'].lower()=='ftp':
            self.ftp = CFTP(self.info['ftp'])
        else:
            logger.log(logging.ERROR, self.info['ftp']['downloadtype'] + ' invalid! ' )
            return
        self.connectServer()  

        while True:
            item = self.data.get()
            try:
                self.testConnect()
                logger.log(logging.INFO, 'do work begin')
                self.do_work(item)
            except Exception,msg:
                logger.log(logging.INFO, 'do work exception')
            self.data.task_done()

        logger.log(logging.INFO, 'End')

    def testConnect(self):
        try:
            self.ftp.pwd()
        except Exception, msg:
            logger.log(logging.ERROR, msg[0])
            self.ftp = None
            self.connectServer()
    def connectServer(self):
        try_cnt = 0
        while (self.ftp.is_ok() == False and try_cnt < 3):
            if self.info['ftp']['downloadtype'].lower()=='sftp':
                self.ftp = CSFTP(self.info['ftp'],self.info['data_type']['File_Regex'])
            elif self.info['ftp']['downloadtype'].lower()=='ftp':
                self.ftp = CFTP(self.info['ftp'])
            try_cnt += 1
            if self.ftp.is_ok() == True:
                logger.log(logging.INFO,  self.info['ftp']['downloadtype'] + ' is able finally' )
                break
        if try_cnt > 3:
                logger.log(logging.ERROR,  'Fail to connect the server' )

    def __del__(self):
        logger.log(logging.INFO, 'End')

    '''
    func_name    : del_file
    description  : delete files or directories
    param_in     : f - filename or dir name
    return_value : 
    author       : Chris Zhang
    ''' 
    def del_file(self, f):
        try:
            if not os.path.exists(f):
                return True

            if os.path.isdir(f):
                os.rmdir(f)
            else:
                os.remove(f)
            return True
        except:
            return False

    '''
    func_name    : do_work
    description  : download file
    param_in     : item - file with absolute path,[path, fname]
    return_value : 
    author       : Chris Zhang
    ''' 
    def do_work(self, item):
        global files_cnt
        print ('downlaod.. do_work:')
        print (item)  #['/home/bruce/testdir/NDS_NETMAX_OUTPUT/2015-02-23/MR/2015-02-23_23-30-00', 'NetMAX_NDS_MR_201502232330_V2_104_1_Mre.zip']

        try:
            ldir = self.info['ldir']
            ld1 = ldir.decode(self.info['data_type']['Encoding'])
            ld2 = ld1.encode('UTF-8')
            if self.ftp.is_ok() == False:
                logger.log(logging.ERROR,  'FTP is unable' )
                self.connectServer()

            if self.info['datatype'] == 0:
                sfile = '%s/%s' % ( item[0], item[1] )
                dfile = '%s/%s' % (ldir, item[1] )
                dfile2 = '%s/%s' % (ld2, item[1] )
                dpartfile = dfile + '.part'
            elif self.info['datatype'] == 2:
                splitFmt = '&'
                dirlevel = item[0].split('/')
                date = dirlevel[len(dirlevel)-1]
                sfile = '%s/%s' % ( item[0], item[1] )
                dfile = '%s/%s%s%s' % (self.info['ldir'], date, splitFmt,item[1] )
                dfile2 = '%s/%s%s%s' % (ld2, date, splitFmt,item[1] )
                dpartfile = dfile + '.part'                
            else:
                splitFmt = '&'
                dirlevel = item[0].split('/')
                date = dirlevel[len(dirlevel)-3]
                filetype = dirlevel[len(dirlevel)-2]
                subdatedir = dirlevel[len(dirlevel)-1]
                sfile = '%s/%s' % ( item[0], item[1] )
                dfile = '%s/%s%s%s%s%s%s%s' % (self.info['ldir'], date, splitFmt, filetype, splitFmt,subdatedir, splitFmt, item[1] )
                dfile2 = '%s/%s%s%s%s%s%s%s' % (ld2, date, splitFmt, filetype, splitFmt, subdatedir, splitFmt,item[1] )
                dpartfile = dfile + '.part'

            #test log
            logger.log(logging.INFO, 'src file  : %s' % ( sfile ) )
            logger.log(logging.INFO, 'dest file : %s' % ( dfile ) )
            logger.log(logging.INFO, 'back file : %s' % ( dpartfile ) )
            
            # 如果临时文件夹存在
            #if the current file exists in tmp_index directory or not, if exist, do not download
            if ( os.path.exists( dfile ) == True ):
                logger.log(logging.INFO,  '%s has been existed in local dir' % dfile )
                return
                
            # delete local files and backup files
            if self.del_file(dpartfile) == False:
                logger.log(logging.ERROR,  'Fail to delete %s' % dpartfile )
                return
            
            # download
            try_cnt = 0
            while ( try_cnt <= 3 ):
                IPdir = self.info['backdir'] + os.sep + self.info['ftp']['ip'] + "_" + str(self.info['ftp']['port'])
                if True:
                    if self.info['ftp']['downloadtype'].lower() == 'ftp':    
                        file_handler = open(dpartfile, 'wb')
                        success = self.ftp.retrbinary("RETR %s"%(sfile), file_handler.write)
                        file_handler.close()
                    elif self.info['ftp']['downloadtype'].lower()=='sftp':
                        success = self.ftp.retrbinary(sfile,dpartfile)
                    else:
                         logger.log(logging.ERROR,  self.info['ftp']['downloadtype'] + ' invalid! ' )
                         return
                        
                    if success == True:
                        if ( os.path.exists( dfile ) == True ):
                            self.del_file(dfile)
                        f1 = dfile2.decode('UTF-8')
                        f2 = f1.encode(self.info['data_type']['Encoding'])
                        os.rename(dpartfile, f2)
                        #self.record_downloaded(item, IPdir)
                        logger.log(logging.INFO,  'download %s successfully' % sfile )
                        break
                    else:
                        self.del_file(dpartfile)
                        try_cnt += 1
                else:
                    break
            # 尝试三次连接失败 打错误 log
            if try_cnt > 3:
                logger.log(logging.ERROR,  'Fail to download %s' % sfile )
        except Exception, msg:
            logger.log(logging.ERROR,  'do_work : %s' % (str(msg[0]) + " " +dpartfile))
            pass

'''
func_name    : dowload_from_nds
description  : Function entry
param_in     : 
return_value : 
'''   
def dowload_from_nds(ip, port, user, passwd, datatype, backdir, rdir, ldir, day_start, day_end, downloadtype, maxfiles, File_Standard, File_Regex, Date_Regex, Date_Format, Encoding):
    # 删除过去几天的log日志
    suit_day1 = datetime.now() - timedelta(days=5)
    suit_day2 = datetime.now() - timedelta(days=6)
    suit_day3 = datetime.now() - timedelta(days=7)
    pastfilename1 = backdir + "/../../logs/dowload_from_ftp_" + suit_day1.strftime('%Y%m%d') + ".log"
    pastfilename2 = backdir + "/../../logs/dowload_from_ftp_" + suit_day2.strftime('%Y%m%d') + ".log"
    pastfilename3 = backdir + "/../../logs/dowload_from_ftp_" + suit_day3.strftime('%Y%m%d') + ".log"
    if os.path.exists(pastfilename1) == True:
        os.remove(pastfilename1)
    if os.path.exists(pastfilename2) == True:
        os.remove(pastfilename2)
    if os.path.exists(pastfilename3) == True:
        os.remove(pastfilename3)
    
    # 全局的 logger.
    global logger
    logfile = backdir + "/../../logs/dowload_from_ftp_" + datetime.now().strftime('%Y%m%d') + ".log"
    # 设置 logger 文件的 logger 地址.
    logger = Logger.Logger(logfile, logging.INFO)
    # make local directory to save downloaded files
    # 传参 ldir 为保存文件的临时文件夹路径
    logger.log( logging.INFO, 'create local dir : %s' % ( ldir ) )
    try:
        # backdir 为备份目录
        if os.path.exists(backdir) == False:
            os.makedirs(backdir)
        if os.path.exists(backdir + os.sep + ip + "_" + port) == False:
            # 创建备份目录下以下载ip_port为名的文件夹.
            os.makedirs(backdir + os.sep + ip + "_" + port)
        if os.path.exists(ldir) == False:
            os.makedirs(ldir)
    except Exception, msg:
        logger.log( logging.ERROR, 'dowload_from_ftp : %s' % ( msg[0] ))
        return -1

    # type convertion 对传参进行类型转换
    logger.log( logging.DEBUG, 'para type convertion' )
    try:
        port          = (int)(port)
        datatype      = (int)(datatype)
        dayStart      = day_start.split(";")
        dayEnd        = day_end.split(";")
        maxfiles      = (int)(maxfiles)
    except Exception, msg:
        logger.log( logging.ERROR, 'dowload_from_nds : %s' % ( msg[0] ))
        return -2

    # get the effective days
    logger.log( logging.INFO, 'calculate valid datetime ' )
    if(len(dayStart)!=len(dayEnd)):
        logger.log( logging.ERROR, 'startTime,endTime invalid ,do not have the same num')
        return -5
    try:
        valid_day  = []
        # include today and all day_interval days
        for i in range(len(dayStart)):
            d = CTimeUtil.getndaysfromlocalday(dayStart[i],0)
            logger.log(logging.ERROR,'d: %s' % ( d ))
            logger.log(logging.ERROR,'dayend: %s' % ( dayEnd[i] ))
            j = 0
            while (datetime.strptime(dayEnd[i], '%Y-%m-%d').date()-datetime.strptime(d, '%Y-%m-%d').date()).days >=0:
                valid_day.append(d)
                j = j + 1
                d = CTimeUtil.getndaysfromlocalday(dayStart[i],j)
    except Exception, msg:
        logger.log( logging.ERROR, 'calculate valid date : %s' % ( msg[0] ))
        return -3
    logger.log( logging.ERROR, valid_day )

    # queue format  [r_dir, filename]
    queue = Queue()
    # 封装了一些信息对象
    ftp_info = { 'ip'     : ip,
                 'port'   : port,
                 'user'   : user,
                 'passwd' : passwd,
                 'downloadtype' : downloadtype }
    data_type = { 'File_Standard' : File_Standard,
                  'File_Regex' : File_Regex,
                  'Date_Regex' : Date_Regex,
                  'Date_Format' : Date_Format,
                  'dayStart' : dayStart,
                  'dayEnd'  : dayEnd,
                  'Encoding' : Encoding,
                  'valid_day'  : valid_day}
    proceduer_info = { 'ftp'        : ftp_info,
                       'rdir'       : rdir,
                       'ldir'       : ldir,
                       'backdir'    : backdir,
                       'valid_day'  : valid_day,
                       'datatype'   : datatype,
                       'maxfiles'   : maxfiles,
                       'data_type' : data_type}
    consumer_info = { 'ftp'      : ftp_info,
                      'backdir'  : backdir,
                      'ldir'     : ldir,
                      'datatype' : datatype,
                      'maxfiles' : maxfiles,
                      'data_type' : data_type}

    # create and start producer
    logger.log( logging.INFO, 'Create producers' )
    try:
        producer = CProducerThread('producer', proceduer_info, queue)
        # 启动线程
        producer.start()
    except Exception, msg:
        logger.log( logging.ERROR, 'dowload_from_nds : %s' % ( msg[0] ))
        return -4

    # create and start consumers
    logger.log( logging.INFO, 'Create consumers' )
    for i in range(1, consumer_cnt + 1):
        name = 'consumer_%d' % ( i )
        consumer = CConsumerThread(name, consumer_info, queue)
        consumer.setDaemon(True)
        # 启动线程
        consumer.start()

    # wait for stop
    logger.log( logging.INFO, 'Wait for stop' )
    producer.join()
    queue.join()
    return 0


# // 定义一些前端模块.
def download_file():
    ip            = os.sys.argv[1]
    port          = os.sys.argv[2]
    user          = os.sys.argv[3]
    passwd        = os.sys.argv[4]
    datatype      = os.sys.argv[5]
    backdir       = os.sys.argv[6].replace('*',' ')
    rdir          = os.sys.argv[7].replace('*',' ')
    ldir          = os.sys.argv[8].replace('*',' ')
    day_start     = os.sys.argv[9]
    day_end       = os.sys.argv[10]
    downloadtype  = os.sys.argv[11]
    maxfiles      = os.sys.argv[12]
    File_Standard = os.sys.argv[13]
    File_Regex    = os.sys.argv[14]
    
    if len( os.sys.argv ) >= 17 :
        Date_Regex    = os.sys.argv[15]
        Date_Format   = os.sys.argv[16]
        Encoding      = os.sys.argv[17]
    else:
        Date_Regex    = ''
        Date_Format   = ''
        Encoding      = 'UTF-8'
    # 设置文件夹编码 uft-8    
    rdir = unicode(rdir, Encoding)
    rdir = rdir.encode('utf-8')
    # 记录开始时间
    btime = time.time()
    # 调用方法从nds下载
    dowload_from_nds(ip, port, user, passwd, datatype, backdir,rdir, ldir, day_start, day_end, downloadtype,
                      maxfiles, File_Standard, File_Regex, Date_Regex, Date_Format, Encoding)
    # 记录结束时间
    etime = time.time()
    # 记录总的消耗时间
    result = ( (int)((etime - btime) * 1000))
    # 打印消耗时间
    logger.log( logging.INFO,"total time is : " + str(result) + " unit: ms")

# 执行函数
if __name__ == '__main__':
    download_file()
