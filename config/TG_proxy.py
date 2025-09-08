# coding=utf-8
import base64
import requests
import re
import time
import os
import random, string
import chardet
from bs4 import BeautifulSoup

# 试用机场链接
url_try = "https://raw.githubusercontent.com/PangTouY00/aggregator/refs/heads/main/data/valid-domains.txt"

# 获取订阅源地址
response = requests.get(url_try)
if response.status_code == 200:
    home_urls = response.text.splitlines()
else:
    home_urls = (
        'https://ch.louwangzhiyu.xyz',
        'https://dashuai.us',
        'https://xiaofeiyun7.top',
        'https://vt.louwangzhiyu.xyz',
        'https://sulink.pro',
        'https://lanmaoyun.icu',
        'https://xueyejiasu.com',
        'https://metacloud.eu.org',
        'https://free.colacloud.free.hr',
        'https://needss.link',
        'https://qingyun.zybs.eu.org',
        'https://vpn.127414.xyz',
        'https://hy-2.com',
        'https://666666222.xyz',
        'https://xiaofeiyun3.cfd',
    )

# 文件路径
update_path = "./sub/"
end_list_clash = []
end_list_v2ray = []
end_bas64 = []
e_sub = [
    'https://sub.789.st/sub?target=v2ray&url=https://raw.githubusercontent.com/go4sharing/sub/main/sub.yaml&sort=true&_=1710174203726',
    'https://raw.githubusercontent.com/yaney01/Yaney01/main/temporary',
    'https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub',
    'https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub',
    'https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2',
    "https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.txt"
]
plane_sub = ['https://www.prop.cf/?name=paimon&client=base64']
try_sub = []
end_try = []


def jiemi_base64(data):
    decoded_bytes = base64.b64decode(data)
    encoding = chardet.detect(decoded_bytes)['encoding']
    decoded_str = decoded_bytes.decode(encoding)
    return decoded_str


def write_document():
    if not e_sub and not try_sub:
        print("订阅为空请检查！")
        return

    # 永久订阅
    random.shuffle(e_sub)
    for e in e_sub:
        try:
            res = requests.get(e)
            proxys = jiemi_base64(res.text)
            end_bas64.extend(proxys.splitlines())
        except:
            print(e, "永久订阅出现错误❌跳过")
    print('永久订阅更新完毕')

    # 试用订阅
    random.shuffle(try_sub)
    for t in try_sub:
        try:
            res = requests.get(t)
            proxys = jiemi_base64(res.text)
            end_try.extend(proxys.splitlines())
        except Exception as er:
            print(t, "试用订阅出现错误❌跳过", er)
    print('试用订阅更新完毕', try_sub)

    # 去重
    end_bas64_A = list(set(end_bas64))
    print("去重完毕！！去除", len(end_bas64) - len(end_bas64_A), "个重复节点")

    bas64 = '\n'.join(end_bas64_A).replace('\n\n', "\n")
    bas64_try = '\n'.join(end_try).replace('\n\n', "\n")

    # 命名文件
    t = time.localtime()
    date = time.strftime('%y%m', t)
    date_day = time.strftime('%y%m%d', t)

    try:
        os.mkdir(f'{update_path}{date}')
    except FileExistsError:
        pass

    txt_dir = update_path + date + '/' + date_day + '.txt'
    with open(txt_dir, 'w', encoding='utf-8') as file:
        file.write(bas64)

    # 分片写入长期订阅
    r = 1
    length = len(end_bas64_A)
    m = 8
    step = int(length / m) + 1
    for i in range(0, length, step):
        zhengli = '\n'.join(end_bas64_A[i: i + step]).replace('\n\n', "\n")
        obj = base64.b64encode(zhengli.encode())
        plaintext_result = obj.decode()
        with open("Long_term_subscription" + str(r), 'w', encoding='utf-8') as f:
            f.write(plaintext_result)
        r += 1

    # 总长期订阅
    obj = base64.b64encode(bas64.encode())
    plaintext_result = obj.decode()
    with open("Long_term_subscription_num", 'w', encoding='utf-8') as f:
        f.write(plaintext_result)

    # 试用订阅
    obj_try = base64.b64encode(bas64_try.encode())
    plaintext_result_try = obj_try.decode()
    with open("Long_term_subscription_try", 'w', encoding='utf-8') as f:
        f.write(plaintext_result_try)

    print("合并完成✅")
    try:
        numbers = sum(1 for _ in open(txt_dir))
        print("共获取到", numbers, "节点")
    except:
        print("出现错误！")

    return


def get_yaml():
    print("开始获取clsah订阅")
    urls = [
        "https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/PangTouY00/Auto_proxy/main/Long_term_subscription_try&insert=false&config=https://raw.githubusercontent.com/PangTouY00/fetchProxy/main/config/provider/rxconfig.ini&emoji=true",
        "https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/PangTouY00/Auto_proxy/main/Long_term_subscription2&insert=false&config=https://raw.githubusercontent.com/PangTouY00/fetchProxy/main/config/provider/rxconfig.ini&emoji=true",
        "https://api.dler.io//sub?target=clash&url=https://raw.githubusercontent.com/PangTouY00/Auto_proxy/main/Long_term_subscription3&insert=false&config=https://raw.githubusercontent.com/PangTouY00/fetchProxy/main/config/provider/rxconfig.ini&emoji=true"
    ]
    n = 1
    for i in urls:
        response = requests.get(i)
        with open("Long_term_subscription" + str(n) + ".yaml", 'w', encoding='utf-8') as f:
            f.write(response.text)
        n += 1
    print("clash订阅获取完成！")


def get_sub_url():
    V2B_REG_REL_URL = '/api/v1/passport/auth/register'
    times = 1
    for current_url in home_urls:
        i = 0
        while i < times:
            header = {
                'Referer': current_url,
                'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            form_data = {
                'email': ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(12))+'@gmail.com',
                'password': 'autosub_v2b',
                'invite_code': '',
                'email_code': ''
            }
            try:
                response = requests.post(current_url+V2B_REG_REL_URL, data=form_data, headers=header)
                subscription_url = f'{current_url}/api/v1/client/subscribe?token={response.json()["data"]["token"]}'
                try_sub.append(subscription_url)
                print("add:"+subscription_url)
            except Exception as e:
                print("获取订阅失败", e)
            i += 1


def get_cfmem():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get("https://www.cfmem.com/search/label/free", headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        target_h2 = soup.find('h2', class_='entry-title')
        if target_h2:
            article_url = target_h2.find('a')['href']
            res = requests.get(article_url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            target_span = soup.find('span', style="background-color:#fff;color:#111;font-size:15px")
            if target_span:
                sub_url = re.search(r'https://fs\.v2rayse\.com/share/\d{8}/\w+\.txt', target_span.text).group()
                print(sub_url)
                try_sub.append(sub_url)
                e_sub.append(sub_url)
                print("获取cfmem.com完成！")
            else:
                print("未找到订阅地址")
        else:
            print("未找到目标 h2")
    except Exception as e:
        print("获取cfmem.com失败！", e)


def get_v2rayshare():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get("https://v2rayshare.com/", headers=headers)
        article_url = re.search(r'https://v2rayshare.com/p/\d+\.html', res.text).group()
        res = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        target_p = soup.find('p', string=re.compile(r'https://v2rayshare.githubrowcontent.com/\d{4}/\d{2}/\d{8}\.txt'))
        if target_p:
            sub_url = target_p.text.strip()
            print(sub_url)
            try_sub.append(sub_url)
            e_sub.append(sub_url)
            print("获取v2rayshare.com完成！")
        else:
            print("未找到目标 p 标签")
    except Exception as e:
        print("获取v2rayshare.com失败！", e)


def get_nodefree():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get("https://nodefree.org/", headers=headers)
        article_url = re.search(r'https://nodefree.org/p/\d+\.html', res.text).group()
        res = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        target_p = soup.find('p', string=re.compile(r'https://nodefree.githubrowcontent.com/\d{4}/\d{2}/\d{8}\.txt'))
        if target_p:
            sub_url = target_p.text.strip()
            print(sub_url)
            try_sub.append(sub_url)
            e_sub.append(sub_url)
            print("获取nodefree.org完成！")
        else:
            print("未找到目标 p 标签")
    except Exception as e:
        print("获取nodefree.org失败！", e)


if __name__ == '__main__':
    print("========== 开始获取机场订阅链接 ==========")
    get_sub_url()
    print("========== 开始获取网站订阅链接 ==========")
    get_cfmem()
    get_v2rayshare()
    get_nodefree()
    print("========== 准备写入订阅 ==========")
    write_document()
    get_yaml()
    print("========== 写入完成任务结束 ==========")
