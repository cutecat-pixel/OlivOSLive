# -*- encoding: utf-8 -*-
'''
   ____     __    _           ____    _____    __     _
  / __ \   / /   (_) _   __  / __ \  / ___/   / /    (_) _   __  ___
 / / / /  / /   / / | | / / / / / /  \__ \   / /    / / | | / / / _ \
/ /_/ /  / /   / /  | |/ / / /_/ /  ___/ /  / /___ / /  | |/ / /  __/
\____/  /_/   /_/   |___/  \____/  /____/  /_____//_/   |___/  \___/
@File      :   OlivOSLive.main.py
@Author    :   Cute_CAT
@Contact   :   2971504919@qq.com
'''
import json
import random
import threading
import time
import OlivOS
import OlivOSLive
import OlivOSReply
import requests
import os
import time
import errno
import multiprocessing
import pymysql

DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = '123456'
DBNAME = 'Live_rooms'

class Event(object):

    def init(plugin_event, Proc):
        while True:
            try:
                sql_base = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
                cur = sql_base.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS Lives(room_id VARCHAR(20), live_Sta INT)')
                sql_base.close()
                break
            except pymysql.Error as e:
                print(str(e))


    def init_after(plugin_event, Proc):
        live = MyThread(Proc)
        live.start()

    def private_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)
        pass

    def group_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)
        pass

    def save(plugin_event, Proc):
        pass


text = '收到大喵服务器直播推送：\n群关注的up{id}开播辣！\n直播间id：{url}'
save_live_path = './plugin/data/OlivOSLive/'
live_url = 'http://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids?uids[]='
botHash = '72126548d1abab2012c697a3301cb881'
lock = multiprocessing.Lock()
lives = {}
hugjs = {}

def deleteBlank(str):
    str_list = list(filter(None,str.split(" ")))
    return str_list

class MyThread(threading.Thread):
    def __init__(self, Proc):
        super().__init__()
        self.Proc = Proc

    def run(self):
        global text
        while True:
            with lock:
                try:
                    sql_base = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
                    cur = sql_base.cursor()
                    sqlSer = "SELECT * FROM Lives"
                    cur.execute(sqlSer)
                    lives = cur.fetchall()
                    if lives[0] == None:
                        continue
                    for live_index in lives:
                        hug = requests.get(live_url + live_index[0])
                        hugjs = json.loads(hug.text)
                        try:
                            if hugjs['msg'] == 'success' and hugjs['message'] == 'success':
                                if hugjs['data'][live_index[0]]['live_status'] == 1 and live_index[1] == 0:
                                    tmp_live_reply1 = text.format(id=hugjs['data'][live_index[0]]['uname'],
                                                                  url=hugjs['data'][live_index[0]]['room_id'])
                                    tmp_live_reply1 += "\n直播名称：" + hugjs['data'][live_index[0]]['title'] + '\n直播封面：\n'
                                    tmp_live_reply1 += '[OP:image,file=' + hugjs['data'][live_index[0]]['cover_from_user'] + ']'
                                    plugin_event = OlivOS.API.Event(
                                        OlivOS.contentAPI.fake_sdk_event(
                                            bot_info=self.Proc.Proc_data['bot_info_dict'][botHash],
                                            fakename='OlivOSLive'
                                        ),
                                        self.Proc.log
                                    )
                                    plugin_event.send('group', 765947729, tmp_live_reply1)
                                    plugin_event.send('group', 754041375, tmp_live_reply1)
                                    plugin_event.send('group', 252994683, tmp_live_reply1)
                                    try:
                                        sqlCha = "UPDATE Lives SET Live_Sta=%s WHERE room_id=%s"
                                        val = (1, live_index[0])
                                        cur.execute(sqlCha, val)
                                        sql_base.commit()
                                    except pymysql.Error as e:
                                        print(str(e))
                                        sql_base.rollback()
                                elif hugjs['data'][live_index[0]]['live_status'] == 0 or hugjs['data'][live_index[0]]['live_status'] == 2:
                                    try:
                                        sqlCha = "UPDATE Lives SET Live_Sta=%s WHERE room_id=%s"
                                        val = (0, live_index[0])
                                        cur.execute(sqlCha, val)
                                        sql_base.commit()
                                    except pymysql.Error as e:
                                        print(str(e))
                                        sql_base.rollback()
                            rad_sleep = random.randint(10, 30)
                            time.sleep(rad_sleep)
                        except:
                            time.sleep(10)
                            continue
                    sql_base.close()
                except pymysql.Error as e:
                    print(str(e))
                    time.sleep(0.1)
                    continue
            time.sleep(random.randint(5, 10))

def unity_reply(plugin_event, Proc):
    command_list = deleteBlank(plugin_event.data.message)
    if command_list[0] == '直播添加':
        with lock:
            try:
                sql_base = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
                cur = sql_base.cursor()
                sqlQuery = 'INSERT INTO Lives (room_id, Live_Sta) VALUE (%s,%s) '
                value = (command_list[1], 0)
                cur.execute(sqlQuery, value)
                sql_base.commit()
                sql_base.close()
            except pymysql.Error as e:
                print(str(e))
        plugin_event.reply(command_list[1] + '已添加到直播监听列表喵')

