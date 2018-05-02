#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: betta

'''
netease music api
'''

from api import NetEase
import MySQLdb
import time
import json
import sys
import threading


joker = NetEase()
user_info = {}
local_account = 'betta551@163.com'
local_password = 'c7236970bfc8e9f7aa83ad3d6d14d59a'

#login_info = joker.login(local_account, local_password)
#print login_info

def save2sql(conn, data):
    cur = conn.cursor()
    try:
        sql = (
            "INSERT INTO netease_music_users (user_id, nick_name, signature, user_type, gender, follows, followeds, province, city, avatar_url, background_url, level, listen_songs, vip_type, expert_tags, people_can_see_playrecord, birthday) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        if data['profile']['birthday'] > 0:
            time_tmp = time.localtime(data['profile']['birthday']/1000)
            birthday = time.strftime("%Y-%m-%d %H:%M:%S", time_tmp)
        else:
            birthday = "1970-01-02 00:00:00"
        if data['profile']['expertTags']:
            expert_tags = '-'.join(data['profile']['expertTags'])
        else:
            expert_tags = ''
        sql_data = (data['profile']['userId'], data['profile']['nickname'], data['profile']['signature'], data['profile']['userType'], data['profile']['gender'], data['profile']['follows'],\
        data['profile']['followeds'], data['profile']['province'], data['profile']['city'], data['profile']['avatarUrl'], data['profile']['backgroundUrl'],\
        data['level'], data['listenSongs'], data['profile']['vipType'], expert_tags, data['peopleCanSeeMyPlayRecord'], birthday)
        cur.execute(sql, sql_data)
        conn.commit()
    except Exception, e:
        print Exception, ":", e

def craw(start, limit):
    conn = MySQLdb.Connect(host = '127.0.0.1',
                        user = 'root',
                        passwd = 'root',
                        db = 'netease',
                        charset = 'utf8')
    # #sql = "SELECT song_id from netease_music_songs where id > (select song_id from netease_music_comments order by id desc limit 1)"
    # sql = "SELECT song_id from netease_music_songs where id > 186664 order by id "
    # cur.execute(sql)
    # result=cur.fetchall()

    for s in range(start, start+limit):
        print "user_id %s" % (s)
        detail = joker.user_detail(s)
        print detail
        if detail:
            save2sql(conn, detail)
        else:
            print "no detail %s" % (s)
        time.sleep(0.5)

    conn.close()

# class MyThread(threading.Thread):
#     """
#     属性:
#     target: 传入外部函数, 用户线程调用
#     args: 函数参数
#     """
#     def __init__(self, target, args):
#         super(MyThread, self).__init__()  #调用父类的构造函数 
#         self.target = target
#         self.args = args

#     def run(self) :
#         self.target(self.args)

def main():
    start_number = int(sys.argv[1])
    limit_number = int(sys.argv[2])
    
    for i in range(10):
        my_thread = threading.Thread(target=craw,
            args=(start_number+i*limit_number, limit_number))
        my_thread.start()
        my_thread.join()

if __name__ == '__main__':
    main()

