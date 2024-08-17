import time
import requests
import json
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import re
import csv
import schedule


def mail(remain_power, my_sender, my_pass, my_receiver):
    ret_bool = True
    try:
        time_now = time.localtime()
        print(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, time_now.tm_hour, time_now.tm_min)

        message_text = f"当前是:{time_now.tm_year}年{time_now.tm_mon}月{time_now.tm_mday}日{time_now.tm_hour}点{time_now.tm_min}分\n" + f"房间剩余电量：{remain_power}"

        msg = MIMEText(message_text, 'plain', 'utf-8')
        msg['From'] = formataddr(["myDesktop", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["User", my_receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "电费余量警告"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret_bool = False
    return ret_bool


def inquiry():
    # 读取查询信息
    with open("inquiry_settings.json", "rb") as memory_file:
        js = json.loads(memory_file.read())  # 读取并解析JSON文件
        account = js["account"]  # 获取校园卡账号
        building = js["building"]  # 获取建筑信息
        room = js["room"]  # 获取房间号
        sender = js["sender"]  # 获取邮箱发送方
        password = js["password"]  # 获取邮箱发送方密钥
        receiver = js["receiver"]  # 获取邮箱接收方
    # print(f"查询 {building} {room}")

    session = requests.session()  # 创建一个会话对象
    # 设置请求头，Content-Type是必要的
    header = {
        "User-Agent": """Mozilla/5.0 (Linux; Android 10; SM-G9600 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36""",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    data = ""
    json_data = '''
    {
	    "query_elec_roominfo": {
		    "aid": "0030000000002505",
	    	"account": "000000",
	    	"room": {
		    	"roomid": "B999",
			    "room": "B999"
		    },
		    "floor": {
			    "floorid": "",
			    "floor": ""
    		},
    		"area": {
	    		"area": "青岛校区",
		    	"areaname": "青岛校区"
	    	},
		    "building": {
			    "buildingid": "1503975890",
			    "building": "S2从文书院"
		    }
    	}
    }
    '''
    js = json.loads(json_data)  # 将JSON字符串转换为Python对象

    # 更新请求数据
    js["query_elec_roominfo"]["account"] = account
    js["query_elec_roominfo"]["room"]["roomid"] = room
    js["query_elec_roominfo"]["room"]["room"] = room
    js["query_elec_roominfo"]["building"] = building

    js = json.dumps(js, ensure_ascii=False)  # 将Python对象转换为JSON字符串
    # print(js)

    js = urllib.parse.quote(js)  # 对JSON字符串进行URL编码
    data += js

    # 构建请求数据
    data = "jsondata=" + data + "&funname=synjones.onecard.query.elec.roominfo&json=true"
    # print(data)
    # 发送POST请求
    res = session.post(url="http://10.100.1.24:8988/web/Common/Tsm.html", headers=header, data=data)
    # print("res!!!!!!!!!!!!!!!")
    # print(res.text)
    js = json.loads(res.text)  # 解析响应内容
    time_now = time.localtime()
    print(time_now.tm_year, time_now.tm_mon, time_now.tm_mday, time_now.tm_hour, time_now.tm_min)
    print(f"{js['query_elec_roominfo']['errmsg']} {js['query_elec_roominfo']['building']['building']} {js['query_elec_roominfo']['room']['room']}")

    # 使用正则表达式提取数字部分
    match = re.search(r"\d+\.\d+", js['query_elec_roominfo']['errmsg'])
    if match:
        # 将提取到的数字部分转换为浮点数
        remaining_power = float(match.group())
        if remaining_power <= 10:
            ret = mail(remaining_power, sender, password, receiver)
            if ret:
                print("邮件发送成功")
            else:
                print("邮件发送失败")
            # print(remaining_power)
        # 将当前时间和剩余电量写入 CSV 文件
        t = time.localtime()
        csv_filename = f"{building['building']}_{room}_电量.csv"
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([f"{t.tm_year}-{t.tm_mon}-{t.tm_mday} {t.tm_hour}:{t.tm_min}", remaining_power])
    else:
        print("未找到数字部分")


def schedule_tasks():
    # Schedule the task to run at every hour and half-hour
    schedule.every().hour.at(":00").do(inquiry)
    schedule.every().hour.at(":30").do(inquiry)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    inquiry()
    schedule_tasks()
