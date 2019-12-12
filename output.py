#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 23:23:07 2019

@author: hankyang
"""
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import threading
import time
import DAN

ServerURL = 'https://6.iottalk.tw' #with SSL connection
Reg_addr = 'hank23020111154641' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='L0858605'
DAN.profile['df_list']=['Line_Out']

DAN.device_registration_with_retry(ServerURL, Reg_addr)
while True:
    try:
        msg=DAN.pull('Line_Out')
        print(msg)
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    time.sleep(5)