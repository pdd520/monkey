import requests
import time
import re

# ========================================
# 分类关键词配置
# ========================================
category_keywords = {
    "影视": [
        "MV", "上傳", "Video", "影音", "片", "mv", "录像", "电影", "劇集",
        "电视剧", "短剧", "微电影", "预告片", "花絮", "幕后", "高清", "4K", 
        "蓝光", "1080p", "美剧", "韩剧", "日剧", "泰剧", "陆剧", "台剧", "港剧",
        "英剧", "电视剧全集", "追剧", "连载", "更新", "大结局", "完结", 
        "网飞", "Netflix", "Disney+", "HBO", "动作片", "喜剧片",
        "爱情片", "悬疑片", "科幻片", "恐怖片", "动画电影", "纪录片"
    ], 

    "综艺": [
        "综艺", "大會", "秀", "娛樂", "歡", "Music", ".Broadcast", "娛", "综艺台",
        "真人秀", "脱口秀", "访谈", "晚会", "春晚", "选秀", "偶像练习生", "创造营",
        "跑男", "王牌对王牌", "向往的生活", "中餐厅", "快乐大本营", "天天向上",
        "吐槽大会", "脱口秀大会", "奇葩说", "非诚勿扰", "我们相爱吧", "乘风破浪"
    ], 

    "新闻": [
        "新聞", "新闻台", "Daily", "News", "資訊", "iNEWS", "Live", "Live News",
        "早间新闻", "晚间新闻", "环球新闻", "时事", "热点", "快讯", "突发",
        "CCTV新闻", "焦点访谈", "新闻联播", "朝闻天下", "国际新闻", "国内新闻",
        "财经新闻", "科技新闻", "军事新闻", "社会新闻", "结果显示", "独家"
    ], 

    "体育": [
        "體育", "運動", "SPORTS", "体育频道", "体育类", "sports", "直播", "赛事",
        "足球", "篮球", "NBA", "CBA", "中超", "英超", "西甲", "欧冠", "世界杯",
        "奥运会", "亚运会", "网球", "羽毛球", "乒乓球", "F1", "赛车", "搏击", "拳击",
        "电竞", "英雄联盟", "LOL", "王者荣耀", "和平精英", "LPL", "KPL", "解说", 
        "集锦", "进球"
    ], 

    "成人": [
        "成人", "裸聊", "成人影片", "色情", "性", "SEX", "Erotic", "18", "18禁", "成年",
        "AV", "情色", "限制级", "R18", "成人直播", "成人视频", "无码", "有码",
        "自慰", "潮吹", "SM", "角色扮演", "丝袜", "制服", "诱惑", "偷拍", "自拍"
    ], 

    "经典": [
        "經典", "经典台", "经典内容", "回顾", "经典节目", "回首", "怀旧", "老电影",
        "黑白电影", "港片黄金时代", "周星驰", "成龙", "李小龙", "张国荣", "梅艳芳",
        "Beyond", "邓丽君", "老歌", "经典老剧", "还珠格格", "西游记", "红楼梦",
        "射雕英雄传", "神雕侠侣", "天龙八部", "鹿鼎记", "经典重温", "童年回忆"
    ], 

    "综合": [
        "綜合", "综合台", "综合内容", "综合类", "生活", "搞笑", "段子", "沙雕", "美食",
        "探店", "Vlog", "日常", "开箱", "测评", "种草", "拔草", "教程", "美妆", "穿搭", 
        "健身", "瑜伽", "舞蹈", "翻唱", "cover", "街头", "挑战", "反应", "短视频"
    ], 

    "动画动漫": [
        "动漫", "动画", "番剧", "新番", "国漫", "日漫", "漫威", "DC", "海贼王", 
        "火影忍者", "死神", "进击的巨人", "鬼灭之刃", "咒术回战", "哆啦A梦", 
        "名侦探柯南", "蜡笔小新", "熊出没", "喜羊羊", "奥特曼", "动画电影",
        "番剧更新", "OVA", "剧场版", "MAD", "AMV", "手书", "MMD"
    ], 

    "纪录片": [
        "纪录片", "纪实", "探索", "发现", "BBC", "国家地理", "野生动物",
        "历史", "文明", "考古", "宇宙", "星空", "海洋", "地球", "人文",
        "人物传记", "战争", "科技前沿", "自然", "动物世界", "航拍中国"
    ], 

    "游戏电竞": [
        "游戏", "实况", "解说", "攻略", "通关", "速通", "开荒", "主播",
        "英雄联盟", "LOL", "王者荣耀", "和平精英", "原神", "崩坏", "第五人格",
        "Minecraft", "我的世界", "GTA", "赛博朋克", "塞尔达", "任天堂", "PS5",
        "Steam", "Epic", "实况解说", "搞笑配音", "整活", "bug集锦"
    ], 

    "音乐": [
        "音乐", "MV", "演唱会", "Live", "现场", "歌会", "音乐节", "KTV",
        "华语", "粤语", "国语", "流行", "摇滚", "民谣", "电音", "DJ", "Remix",
        "翻唱", "cover", "钢琴", "吉他", "和声", "合唱", "歌单", "排行榜"
    ], 

    "短视频生活": [
        "抖音", "快手", "短视频", "15秒", "30秒", "1分钟", "搞笑", "宠物",
        "猫猫", "狗狗", "萌宠", "宝宝", "小孩", "街拍", "风景", "旅行", 
        "航拍", "云养猫", "沙雕动画", "表情包", "鬼畜", "整活", "反应视频"
    ]
}

# ========================================
# 番号正则（已修复转义）
# ========================================
anime_id_patterns = [
    r"\b([A-Z]{2,6}-?\d{2,5})\b",
    r"\b([A-Z]{2,6}[_-]?\d{3,5})\b",
    r"\b([A-Z]{3,6}-?\d{2,4})\b",
    r"\b(200GANA|SIRO|300NTK|300MAAN|345SIMM|259LUXU)-?\d{3,5}\b",
    r"\bFC2-?PPV-?\d{6,8}\b",
    r"\bheyzo.?\d{4}\b",
    r"\b\d{5,6}-\d{3}\b",
    r"\b1pon.?\d{6}_\d{3}\b",
    r"\b\d{6}_\d{2}\b",
    r"\b[NK]\d{4}\b",
    r"\b(?:S1|SSIS|SONE|IPX|IPZZ|STARS|ADN|ATID|SHKD|REBD|MIDE|TEKS|OFJE)\b",
    r"\b(?:MIDV|MIDE|MIAA|MDBK|MDYD)\b",
    r"\b(?:ABW|ABF|CHN|DIC|SGA|LXVS|PPX)\b",
    r"\b(?:SDAB|SDDE|SDMM|SDMT|START)\b"
]

# ========================================
# 辅助函数
# ========================================
def filter_bad_words(title):
    bad_words = ["奶爸", "最(J)熱 NBVe", "如泥当"]
    return not any(word in title for word in bad_words)

def extract_id_from_title(title):
    text = title.upper()
    for pattern in anime_id_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None

def is_in_category(title, category):
    if title.startswith('#'):
        return False
    keywords = category_keywords.get(category, [])
    return any(keyword in title for keyword in keywords)

# ========================================
# 主函数
# ========================================
def fetch_and_replace(urls):
    all_processed = []
    seen_urls = set()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            print(f"成功请求 {url}")

            if response.status_code != 200:
                print(f"获取 {url} 失败，状态码为 {response.status_code}。")
                continue

            content = response.text
            lines = content.splitlines()

            for line in lines:
                # 跳过无用行
                if any(skip in line for skip in ['更新时间', '关于', '公众号', '软件库', '#EXTM3U']):
                    continue
                if ',' not in line or line.startswith('#EXTINF'):
                    continue

                try:
                    title, url_part = line.split(',', 1)
                    title = title.strip()
                    url_part = url_part.strip()

                    if not url_part or url_part in seen_urls:
                        continue

                    if not filter_bad_words(title):
                        continue

                    seen_urls.add(url_part)
                    all_processed.append((title, url_part))

                except ValueError:
                    continue

        except requests.exceptions.Timeout:
            print(f"请求 {url} 超时，跳过。")
        except requests.exceptions.RequestException as e:
            print(f"请求 {url} 出现错误：{e}")
        except Exception as e:
            print(f"处理行时出错：{e}")

    # 生成 my02.txt
    with open('my02.txt', 'w', encoding='UTF-8') as f:
        f.write(f"注意事项,#genre#\n{current_time} 仅供测试自用如有侵权请通知,https://codeberg.org/alantang/photo/raw/branch/main/Robot.mp4\n")
        for title, url in all_processed:
            f.write(f"{title},{url}\n")

    # 分组逻辑
    grouped_entries = {
        "影视": [], "综艺": [], "新闻": [], "体育": [],
        "成人": [], "经典": [], "综合": [], "动画": [],
        "纪录片": [], "游戏": [], "音乐": [], "短视频": []
    }

    category_mapping = {
        "影视": "影视", "综艺": "综艺", "新闻": "新闻", "体育": "体育",
        "成人": "成人", "经典": "经典", "综合": "综合",
        "动画动漫": "动画", "纪录片": "纪录片", "游戏电竞": "游戏",
        "音乐": "音乐", "短视频生活": "短视频"
    }

    for title, url in all_processed:
        matched = False
        for src_cat, keywords in category_keywords.items():
            if any(kw in title for kw in keywords):
                target_cat = category_mapping.get(src_cat, "综合")
                grouped_entries[target_cat].append((title, url))
                matched = True
                break
        if not matched:
            grouped_entries["综合"].append((title, url))

    # 生成 M3U
    m3u_header = f"""#EXTM3U
# Created by GitHub Actions: {current_time} Asia/Shanghai
# Source: IPTV
"""
    m3u_lines = [m3u_header]

    icon_map = {
        "影视": "🎬", "综艺": "🎤", "新闻": "📰", "体育": "🏅",
        "成人": "🔞", "经典": "🎞", "综合": "📌", "动画": "🌸",
        "纪录片": "🎬", "游戏": "🎮", "音乐": "🎵", "短视频": "📱"
    }

    for cat, entries in grouped_entries.items():
        if not entries:
            continue
        group_name = f"{icon_map.get(cat, '📺')} {cat}"
        for title, url in entries:
            m3u_lines.append(f'#EXTINF:-1 tvg-name="{title}" group-title="{group_name}",{title}')
            m3u_lines.append(f'{url}\n')

    with open('my02.m3u', 'w', encoding='UTF-8') as f:
        f.write('\n'.join(m3u_lines).rstrip('\n'))

    print(f"已生成 {len(all_processed)} 条资源，归类后保存为 my02.txt 和 my02.m3u。")

# ========================================
# 入口
# ========================================
if __name__ == "__main__":
    urls = [
        'https://raw.githubusercontent.com/SSM0415/apptest/main/TVonline.txt',
        'https://raw.githubusercontent.com/jack2713/my/refs/heads/main/TMP/temp1.txt',
        'https://raw.githubusercontent.com/jack2713/my/refs/heads/main/TMP/TMP.txt',
        'https://raw.githubusercontent.com/sublime2025/IPTV/refs/heads/main/adult',
        'https://raw.githubusercontent.com/SSM0415/apptest/refs/heads/main/TVbox2livefomi243.txt',
        'https://raw.githubusercontent.com/alenin-zhang/IPTV/4e8e4812168164ea11acc0617b814a7948b632f5/av'
    ]
    fetch_and_replace(urls)
