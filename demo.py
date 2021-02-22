###############################################################
# 江西高校支付宝校园防疫批量自动签到程序
###############################################################
# @Author JetXi
# @Create 2021-02-22
# @Email  ShengJieXi233@gmail.com
###############################################################
# 程序无需作任何配置，将信息填入info.csv后运行代码即可
# 请在使用程序前仔细阅读代码注释，请不要将此程序用于学习交流以外的任何用途，否则由此引发的一切后果由使用者本人承担。
# 可以在Windows设定计划任务定时执行，也可在Linux使用crontab定时执行
# 腾讯云的云函数也很香
###############################################################


import csv
import json
import requests

with open('./info.csv', encoding='gbk') as info:
    reader = csv.reader(info)
    for stu in reader:
        if stu[0] != '学校代码':
            # 登录页面，提交学校代码和学号，用于获取cookie，直接get请求
            loginurl = f'https://fxgl.jx.edu.cn/{stu[0]}/public/homeQd?loginName={stu[1]}&loginType=0'
            # 签到页面，需要使用cookie登录，post一系列参数实现签到
            signinurl = f'https://fxgl.jx.edu.cn/{stu[0]}/studentQd/saveStu'
            # 请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'
            }
            # 使用session会话保持技术，可跨请求保留cookie
            session = requests.session()
            # 访问登陆界面，获取到用户的cookie，保持于session会话中
            session.get(loginurl, headers=headers)
            # 需要post的数据
            data = {
                'province': stu[2],      # 省份
                'city': stu[3],          # 市
                'district': stu[4],      # 区/县
                'street': stu[5],        # 具体地址
                'xszt': 0,
                'jkzk': 0,               # 健康状况 0:健康 1:异常
                'jkzkxq': '',            # 异常原因
                'sfgl': 1,               # 是否隔离 0:隔离 1:未隔离
                'gldd': '',
                'mqtw': 0,
                'mqtwxq': '',
                'zddlwz': stu[2]+stu[3]+stu[4],    # 省市区
                'sddlwz': '',
                'bprovince': stu[2],
                'bcity': stu[3],
                'bdistrict': stu[4],
                'bstreet': stu[5],
                'sprovince': stu[2],
                'scity': stu[3],
                'sdistrict': stu[4],
                'lng': stu[6],          # 经度
                'lat': stu[7],           # 纬度
                'sfby': 1                  # 是否为毕业生 0:是 1:否
            }
            result = session.post(url=signinurl, data=data, headers=headers).text
            # 访问接口返回的数据是json字符串，使用loads方法转换为python字典
            statusCode = json.loads(result)['code']
            # 根据状态码判断签到状态
            if statusCode == 1001: print(f"学号为{stu[1]}的同学签到成功")
            elif statusCode == 1002: print(f"学号为{stu[1]}的同学今日已签")
            else: print(f"学号为{stu[1]}的同学签到状态异常，请尝试重新运行程序")