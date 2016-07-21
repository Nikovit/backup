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

#Логирование
# импортируем модуль
import logging
# создаём объект с именем модуля
logger = logging.getLogger(__name__)
# задаём уровень логгирования
logger.setLevel(logging.INFO)
# создаём обрабочтик файла лога
handler = logging.FileHandler('backup.log')
# задаём уровень логгирования
handler.setLevel(logging.INFO)
# форматируем записи
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# устанавливаем формат для обработчика
handler.setFormatter(formatter)
# добавляем обработчик к логгеру
logger.addHandler(handler)


#Создание дампов PostgreSQL
#database = ['trade', 'buh2bd', 'salary']
database = ['template0']
backupdir='/home/garbage/backup/'
date = time.strftime('%Y-%m-%d')

for backup in database:
    subprocess.call('cd %s | pg_dump -U postgres %s | gzip -9 -c > %s/%s-%s.gz' % (backupdir, backup, backupdir, date, backup), shell=True)
    #filename = '%s%s-%s.gz' % (backupdir, date, backup) - не помню зачем мне это нужно
    logger.info(backup + ' дамп создан и заархивирован')
else:
    logger.error(backup + ' дамп не создан')



# Удаление старых копий
removal_period=timedelta(days=30)

onlyfiles = [f for f in listdir(backupdir) if isfile(join(backupdir, f))]

for filename in onlyfiles:
    how_long_ago_creation_date = datetime.now()-datetime.fromtimestamp(os.path.getctime(backupdir+filename))
    print(filename+" created "+str(how_long_ago_creation_date)+" ago")
    if (how_long_ago_creation_date>removal_period):
        print("Delete file: "+filename)
        os.remove(backupdir+filename)


#####Синхронизация с FTP######

# # #Настройки FTP
# host = '192.168.0.26'
# ftp_user = 'buuser'
# ftp_password = 'buuserpwd'
# REMOTE_FOLDER = '1C8'
# LOCAL_FOLDER = '/home/garbage/backup/'
#
#
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
#     server.storbinary('STOR ' + local_file, open(local_file, 'rb'))
#
# #закрываем соединение с сервером
# server.close()

from ftpsync.targets import FsTarget
from ftpsync.ftp_target import FtpTarget
from ftpsync.synchronizers import BiDirSynchronizer

local = FsTarget("/home/garbage/backup/")
user ="buuser"
passwd = "buuserpwd"
remote = FtpTarget("1C8", "192.168.0.26", user, passwd, tls=True)
opts = {"resolve": "skip", "verbose": 1, "dry_run" : False}
s = BiDirSynchronizer(local, remote, opts)
s.run()












