#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import json
import vk
import random

#group_id = input("Input group ID: ")#152573807#45627034

friendcode = open('step\mfriend_code.txt').read() # друзья
followecode = open('step\mfoll_code.txt').read() # подприсчики
failfillowecode = open('step\mfail_foll_code.txt').read() # подписчик
strcode = open('step\member_code.txt').read() # участники


def get_token():
    with open("mtoken.txt") as f:
        return f.read()

#объединение получанных результатов в один список
def union_req_data( req ):
    data_list =[]
    #проверка на случай если заблочен акаунт (None)
    try:
        for part in req:
            data_list.extend(part)
    except :
        return data_list

    return data_list

#объединение получанных результатов в один список
def union_user_req_data( req ):
    users_data_list =[]
    #последние всегда фиксированные
    fails = req[len(req)-1:]
    index = fails[len(fails)-1]
    #проверка на случай если заблочен акаунт (None)
    for i in range(len(req)-1): #без последнего - он информационный
        try:
            users_data_list.append([])
            for part in req[i]:
               users_data_list[i].extend(part) 
        except : continue
    return  (users_data_list, fails[0],index)


#вспомогательное
def write_to_file(post_list, file_name): 
    file = open(file_name,'w')
    for el in post_list:
        file.write(str(el) + ';' )
    file.close()  

def write_to_file_adj(post_dict, file_name): 
    file = open(file_name,'w')
    for key in post_dict:
        file.write('\n')
        if(len(post_dict[key])>0):
            file.writelines(str(key) + ' '+ str(post_dict[key]) + ';' )
    file.close()  

def get_id_into_file(name):
    with open(name) as f:
        return [int(x) for x in f.read()[:-1].split()] 
    

def parse_vk(status, group_id):
    #  получить токен
    api_token = get_token()
    # создать сессию
    session = vk.Session(access_token=api_token)
    api = vk.API(session)
    # получить подписчиков
    # mem_list = get_id_into_file (str(group_id)+'mem.txt')
    mem_list = get_mem_list(api, group_id)
    write_to_file(mem_list, str(group_id)+'mem.txt')

    # создаем список смежности (пока пустая)
    adjacency_list = dict()
    for mem in mem_list: adjacency_list[mem] = set()

    #добавиь друзей и подписчиков в список
    gather_followers(status, api,adjacency_list,mem_list)
    gather_friends(status, api,adjacency_list,mem_list) 
    #запись в файл
    write_to_file_adj(adjacency_list, str(group_id)+'adj.txt')
   

def gather_followers(status, api,adjacency_list,mem_list):
    in_index = 0 #из вксрипта
    ex_index = 0 #здесь
    fail_list = []
    #пока не посмотрели все непроблемные продолжаем
    while(ex_index < (len(mem_list)-len(fail_list))):
      first_foll_string = 'var gid =  '+ str(mem_list[ex_index: ex_index+21])+';' 
      folls_lists , fail , in_index = execute_querie(api, first_foll_string, followecode)
      fail_list.extend([mem_list[ex_index+id_f] for id_f in fail[:-1] ])#[:-1] - пробел
      for i in range(len(folls_lists)): #Для каждого списка
        for foll in folls_lists[i]: #для каждого подписчика
          if foll in adjacency_list: #если он в группе состоит
            adjacency_list[mem_list[ex_index + i]].add(foll)
      ex_index += in_index[0]+len(fail) #новый индекс - сколько прошли плюс кол-во ошибок
      #print(ex_index)
      status.value+= int(in_index[0])
      #print(fail)

    #fail_list = [517356333]
    for fail_id in fail_list:
        foll_list = get_big_follower_list(api, fail_id)
        for foll in foll_list: #для каждого подписчика
            if foll in adjacency_list: #если он в группе состоит
                adjacency_list[fail_id].add(foll)



def gather_friends(status, api,adjacency_list,mem_list):
    in_index = 0 #из вксрипта
    ex_index = 0 #здесь
    while(ex_index < len(mem_list)):
      first_foll_string = 'var gid =  '+ str(mem_list[ex_index: ex_index+21])+';' 
      friend_lists , fail , in_index = execute_querie(api, first_foll_string, friendcode)
      for i in range(len(friend_lists)): #Для каждого списка
        for friend in friend_lists[i]: #для каждого подписчика
          if friend in adjacency_list: #если он в группе состоит
            adjacency_list[mem_list[ex_index + i]].add(friend)
            adjacency_list[friend].add(mem_list[ex_index + i])
      ex_index += in_index#новый индекс - сколько прошли плюс кол-во ошибок
      #print(ex_index)
      status.value+= int(in_index)
      #print(fail)   


MAX_NUM = 22000
#получение всех участников вне зависимости от размера сообщества
def get_mem_list(api,group_id):
    mem_list = []
    #выяснить размеры группы
    req = api.groups.getMembers(group_id = group_id, count = 1, offset = 0, v = 5.124)
    time.sleep(0.333)
    numbers = int(req['count'])
    #получить всех участников группы (не дает больше MAX_NUM - ТЕКСТ !)
    for big_step in range(0,numbers,MAX_NUM):
        if (big_step % 154000 == 0):  time.sleep(1)
        first_string = 'var step = '+str(big_step) +', gid =  '+ str(group_id)+';'
        mem_list.extend(execute_querie(api , first_string, strcode))
        #print(big_step)
    return mem_list

#получение всех подписчиков вне зависимости от размера сообщества
def get_big_follower_list(api, user_id):
    fol_list = []
    #выяснить размеры группы
    req = api.users.getFollowers(user_id = user_id, count = 1, offset = 0, v = 5.124)
    time.sleep(0.333)
    numbers = int(req['count'])
    #получить всех участников группы (не дает больше MAX_NUM - ТЕКСТ !)
    for big_step in range(0,numbers,MAX_NUM):
        if (big_step % 154000 == 0):  time.sleep(1)
        first_string = 'var step = '+str(big_step) +', gid =  '+ str(user_id)+';'
        fol_list.extend(execute_querie(api , first_string, failfillowecode))
        #print(big_step)
    return fol_list

def execute_querie(api, first_string, text_code):

    repeat = False # повтор запроса (ош 13) 
    fool_code = first_string + text_code
    try:
        req = api.execute(code = fool_code, v = 5.126 )
    # except requests.exceptions.ReadTimeout:
    except : #vk.exceptions.VkAPIError:
        time.sleep(1.5)
        repeat =True
    #выждать и повторить
    if repeat:
        try:
            req = api.execute(code = fool_code, v = 5.126 )
        except:
            time.sleep(3)
            req = api.execute(code = fool_code, v = 5.126 )
    
    # вызов обьединения
    if(first_string[:5] == 'var g'):
        return  union_user_req_data(req)
    else: return union_req_data(req)

def get_info_about_group(status, id):
    group_id = str(id)
    try:
        parse_vk(status, group_id)
        return 0
    except:
        return -1

def get_count(id):
    api_token = get_token()
    # создать сессию
    session = vk.Session(access_token=api_token)
    api = vk.API(session)
    req = api.groups.getMembers(group_id = id, count = 1, offset = 0, v = 5.124)
    time.sleep(0.333)
    numbers = int(req['count'])
    return numbers

def main():
    get_info_about_group(0, 152573807)
    print()

if __name__ == "__main__":
    main()