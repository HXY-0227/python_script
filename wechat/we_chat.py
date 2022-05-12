import requests
import itchat
import os

needAutoAnswer = []

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://robot.ownthink.com/',
}

# 机器人配置
def get_data(text): 
    data = {
        "appid": "65fd2a411625b81e5fab3cf4c885c760",
        "userid": "1473706220@qq.com",
        "spoken": text,
    }
    return data

def readAutoAnswerList():
    global needAutoAnswer

    file_path = os.getcwd() + '\\自动回复.txt'
    file = open(file_path,"r", encoding="utf-8")
    needAutoAnswer = [line.strip('\n') for line in file.readlines()]
    file.close()

def get_answer(text):
    data = get_data(text)
    url = 'https://api.ownthink.com/bot'
    response = requests.post(url=url, data=data, headers=headers) 
    response.encoding = 'utf-8'
    result = response.json()
    answer = result['data']['info']['text']
    return answer

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    friend = msg['User']['RemarkName']
    content = msg['Content']
    print('%s: %s' % (friend, content))

    if friend in needAutoAnswer:
        answer = get_answer(content)
        itchat.send(answer, msg['FromUserName'])
        print('我：%s' % answer)

if __name__ == "__main__":
    readAutoAnswerList()
    itchat.auto_login(hotReload=True)
    itchat.run()