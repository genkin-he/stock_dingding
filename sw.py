#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'genkin'


import datetime
import time 
import requests
import tushare as ts
import json
PUSH_INTERVAL = 10
REMIND_INTERVAL = 5
KEYWORD="Genkin: "
DING_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=XXXXX"

def handle(all_list = []):
    stock_symbol_list = []
    price_low_list = []
    price_high_list = []
    for i in range(int(len(all_list) / 3)):
        stock_symbol_list.append(all_list[3 * i])
        price_low_list.append(all_list[3 * i + 1])
        price_high_list.append(all_list[3 * i + 2])
    return stock_symbol_list, price_low_list, price_high_list


def get_push(all_list = []):
    if not trading_period():
        return
    stock_symbol_list, price_low_list, price_high_list = handle(all_list)
    localtime = datetime.datetime.now()    # 获取当前时间
    now = localtime.strftime('%H:%M:%S')
    data = ts.get_realtime_quotes(stock_symbol_list)    # 获取股票信息
    price_list = data['price']
    print(now)

    for i in range(int(len(all_list) / 3)):
        content = stock_symbol_list[i] + ' 当前价格为 ' + price_list[i] + '\n'
        if float(price_list[i]) <=  float(price_low_list[i]):
            dingmsg(content + '低于最低预警价格')
            print(content + '低于最低预警价格')
        elif float(price_list[i]) >=  float(price_high_list[i]):
            dingmsg(content + '高于最高预警价格')
            print(content + '高于最高预警价格')
        else:
            dingmsg(content + '价格正常')
            print(content + '价格正常')
    print('***** end *****\n')


def get_remind(all_list = []):
    if not trading_period():
        return
    stock_symbol_list, price_low_list, price_high_list = handle(all_list)
    localtime = datetime.datetime.now()    # 获取当前时间
    now = localtime.strftime('%H:%M:%S')
    data = ts.get_realtime_quotes(stock_symbol_list)    # 获取股票信息
    price_list = data['price']
    print(now)

    for i in range(int(len(all_list) / 3)):
        content = stock_symbol_list[i] + ' 当前价格为 ' + price_list[i] + '\n'
        if float(price_list[i]) <=  float(price_low_list[i]):
            dingmsg(content + '低于最低预警价格')
            print(content + '低于最低预警价格')
        elif float(price_list[i]) >=  float(price_high_list[i]):
            dingmsg(content + '高于最高预警价格')
            print(content + '高于最高预警价格')
        else:
            print(content + '价格正常')
    print('***** end *****\n')


def push(all_list = []):
    print('Stock_DingDing 已开始执行！')
    while True:
        try:
            get_push(all_list)
            time.sleep(PUSH_INTERVAL)
        except KeyboardInterrupt:
            dingmsg('Stock_DingDing 已执行完毕！')
            print('Stock_DingDing 已执行完毕！')
            break


def remind(all_list = []):
    dingmsg('Stock_DingDing 已开始执行！')
    print('Stock_DingDing 已开始执行！')
    while True:
        try:
            get_remind(all_list)
            time.sleep(REMIND_INTERVAL)
        except KeyboardInterrupt:
            dingmsg('Stock_DingDing 已执行完毕！')
            print('Stock_DingDing 已执行完毕！')
            break

def dingmsg(result):
    if not trading_period():
        return
    # 构建请求头
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    message = {
        "msgtype": "text",
        "text": {
            "content": KEYWORD + result
        },
        "at": {
            "isAtAll": True
        }
    }
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=DING_WEBHOOK, data=message_json, headers=header)
    # 打印返回
    print(info.text)


def trading_period():
    open_at = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:29', '%Y-%m-%d%H:%M')
    close_at =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'15:00', '%Y-%m-%d%H:%M')
    return (datetime.datetime.now() >= open_at and datetime.datetime.now() <= close_at)

remind(['000908', 4.86, 5.10]);
