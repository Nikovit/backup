#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import logging
import sys
import datetime
import stat
from os import listdir
from os.path import isfile, join
from datetime import timedelta, datetime
import os.path, time
import ftplib

#Настройки FTP
host = '192.168.0.26'
ftp_user = 'buuser'
ftp_password = 'buuserpwd'
REMOTE_FOLDER = '1C8'
LOCAL_FOLDER = '/home/garbage/backup/'

#Создание дампов PostgreSQL
#database = ['trade', 'buh2bd', 'salary']
database = ['salary']
backupdir='/home/garbage/backup/'
date = time.strftime('%Y-%m-%d')

for backup in database:
    subprocess.call('cd %s | pg_dump -U postgres %s | gzip -9 -c > %s/%s-%s.gz' % (backupdir, backup, backupdir, date, backup), shell=True)
    filename = '%s%s-%s.gz' % (backupdir, date, database)


# Удаление старых копий
removal_period=timedelta(days=30)

onlyfiles = [f for f in listdir(backupdir) if isfile(join(backupdir, f))]

for filename in onlyfiles:
    how_long_ago_creation_date = datetime.now()-datetime.fromtimestamp(os.path.getctime(backupdir+filename))
    print(filename+" created "+str(how_long_ago_creation_date)+" ago")
    if (how_long_ago_creation_date>removal_period):
        print("Delete file: "+filename)
        os.remove(backupdir+filename)

# #Загрузка на FTP
    # #соединяемся с сервером
    # server = ftplib.FTP(host)
    # server.login(ftp_user, ftp_password)
    #
    # #делаем текущими папки для синхронизации
    # server.cwd(REMOTE_FOLDER)
    # os.chdir(LOCAL_FOLDER)
    #
    # #получаем список файлов с синхронизируемых папках
    # remote_files = set(server.nlst())
    # local_files = set(os.listdir(os.curdir))
    #
    # #загружаем недостающие файлы на ftp
    # for local_file in local_files - remote_files:
    #     server.storbinary('STOR ' + local_file, open(local_file, 'r'))
    #
    # #закрываем соединение с сервером
    # server.close()