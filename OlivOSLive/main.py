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

class Event(object):

    def init(plugin_event, Proc):
        pass

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

class MyThread(threading.Thread):
    def __init__(self, Proc):
        super().__init__()
        self.Proc = Proc

    def run(self):
        global text
        while True:
            with lock:
                with open(save_live_path + 'Live_room.txt', 'r+', encoding='utf-8') as live_text:
                    lives = eval(live_text.read())
                    for live_index in lives:
                        try:
                            hug = requests.get(live_url + live_index)
                            hugjs = json.loads(hug.text)
                        except:
                            time.sleep(5)
                            continue
                        if hugjs['msg'] == 'success' and hugjs['message'] == 'success':
                            if hugjs['data'][live_index]['live_status'] == 1 and lives[live_index] == 0:
                                tmp_live_reply1 = text.format(id=hugjs['data'][live_index]['uname'],
                                                              url=hugjs['data'][live_index]['room_id'])
                                tmp_live_reply1 += "\n直播名称：" + hugjs['data'][live_index]['title'] + '\n直播封面：\n'
                                tmp_live_reply1 += '[OP:image,file=' + hugjs['data'][live_index]['cover_from_user'] + ']'
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
                                lives[live_index] = 1
                            elif hugjs['data'][live_index]['live_status'] == 2 or hugjs['data'][live_index]['live_status'] == 0:
                                lives[live_index] = 0
                        rad_sleep = random.randint(30, 90)
                        time.sleep(rad_sleep)
                    live_text.seek(0)
                    live_text.truncate()
                    live_text.write(str(lives))
            time.sleep(random.randint(5, 10))

def unity_reply(plugin_event, Proc):
    command_list = OlivOSReply.msgReply.deleteBlank(plugin_event.data.message)
    if command_list[0] == '直播添加':
        with lock:
            with open(save_live_path + 'Live_room.txt', 'r+', encoding='utf-8') as f_live:
                dic = eval(f_live.read())
                dic[command_list[1]] = 0
                f_live.seek(0)
                f_live.truncate()
                f_live.write(str(dic))
        plugin_event.reply(command_list[1] + '已添加到直播监听列表喵')

