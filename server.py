from socket import socket
import re
import os 
import pandas as pd
import requests as rs
from bs4 import BeautifulSoup as bs
import threading
import time



def get_user_data(data):
    data = data.split('\n')
    user = data[-1].split('&')
    user = [user[0].split('=')[1]]+[user[1].split('=')[1]]
    return user

def HandleUser(s1,addr, users_db):
        
            request = s1.recv(1024).decode()
            print(request)
            
            pattern_get = r'GET /(.*?\.(.*)) HTTP/1.1'
            pattern_post = r'POST /.* HTTP/1.1'
            pattern_origin = r'Referer: .*/(.*)\.(.*)'
            file_data = re.search(pattern_get, request)
            post_data = re.search(pattern_post, request)
            
            if (file_data is not None):
                if os.path.isfile(os.getcwd()+'\\'+file_data.groups(0)[0]):
                    if file_data.groups(0)[1] not in ['png','jpg','ico']:
                        file_name = file_data.groups(0)[0]
                        file = open(file_name).read()
                        header = f'HTTP/1.1 200 OK\r\n\r\n'
                        header2 = 'Content-Length:{len(file)}\r\nContent-Type:text/html; charset=utf-8\r\n\r\n'
                        s1.send((header+file).encode())
                    else:
                        file_name = file_data.groups(0)[0]
                        file = open(file_name, 'rb').read()
                        header = f'HTTP/1.1 200 OK\r\n\r\n'
                        header2 = 'Content-Length:{len(file)}\r\nContent-Type:image/jpg\r\n\r\n'
                        s1.send(header+file)
            elif 'GET / HTTP/1.1' in request:
                s1.send(('HTTP/1.1 200 OK\r\n\r\n'+(home_page)).encode())

            if post_data is not None:
                post_origin = re.search(pattern_origin, request)
                print(post_origin.groups(2)[0])
                file= open('user_page.html').read()
                header = f'HTTP/1.1 200 OK\r\n\r\n'
                header2 ='Content-Length:{len(file)}\r\nContent-Type:text/html; charset=utf-8\r\n\r\n'
                user = get_user_data(request)
                if post_origin.groups(2)[0]=='login_page':
                    if ((users_db['username']==user[0]) & (users_db['password']==user[1])).any():
                        s1.send((header+file).encode())
                    else:
                        page = open('login_error.html').read()
                        s1.send((header+page).encode())

                elif post_origin.groups(2)[0]=='signup':
                    s1.send((header+file).encode())
                    time.sleep(0.5)
                    users_db.loc[len(users_db)] = [user[0], user[1]]
                    #user = {'username': user[0], 'password': user[1]}
                    #users_db = users_db._append(pd.Series(user, index = columns), ignore_index = True)
                    
                    print(users_db)
                    users_db.to_csv('users.csv')
    
    


SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
soc = socket()
soc.bind((SERVER_IP, SERVER_PORT))
home_page = open('home_page.html').read()
soc.listen(2)
users_db = pd.read_csv('users.csv',header=0,index_col=0)
while True:
    s1, addr =soc.accept()
    t=threading.Thread(target=HandleUser,args=(s1,addr, users_db))
    t.start()
    

'''
while True:
    s1, addr =soc.accept()
    request = s1.recv(1024).decode()
    print(request)
    s1.send(('HTTP/1.1 200 OK\r\n\r\n'+(home_page)).encode())
    pattern_get = r'GET /(.*\.(.*)) HTTP/1.1'
    pattern_post = r'POST /.* HTTP/1.1'
    file_data = re.search(pattern_get, request)
    post_data = re.search(pattern_post, request)
    
    if file_data is not None:
        if os.path.isfile(os.getcwd()+'\\'+file_data.groups(0)[0]):
            if file_data.groups(0)[1] not in ['png','jpg']:
                file_name = file_data.groups(0)[0]
                file = open(file_name).read()
                header = f'HTTP/1.1 200 OK\r\n\r\nContent-Length:{len(file)}\r\nContent-Type:text/html; charset=utf-8\r\n\r\n'
                s1.send((file).encode())
            else:
                file_name = file_data.groups(0)[0]
                file = open(file_name, 'rb').read()
                header = f'HTTP/1.1 200 OK\r\n\r\nContent-Length:{len(file)}\r\nContent-Type:image/jpg\r\n\r\n'
                s1.send(file)
    if post_data is not None:
        user = get_user(post_data)
        print(user)
        file= open('user_page.html').read()
        header = f'HTTP/1.1 200 OK\r\n\r\nContent-Length:{len(file)}\r\nContent-Type:text/html; charset=utf-8\r\n\r\n'
        s1.send((header+file).encode())
        #users_db['username'] = [user[0]]
        #users_db['password'] = [user[1]]
        #print(users_db)
        #users_db.to_csv('users.csv')
        
    

    
    
'''