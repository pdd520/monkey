import requests
import time
import re

# 你的分类设置（即你提供的 JSON 文件内容，简化成 Python 格式）
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

# 你提供的番号封面与标签正则表达式（整理进 Python 语法版）
anime_id_patterns = [
    r"\b([A-Z]{2,6}-?\\d{2,5})\b",
    r"\b([A-Z]{2,6}[_-]?\\d{3,5})\b",
    r"\b([A-Z]{3,6}-?\\d{2,4})\b",
    r"\b(200GANA|SIRO|300NTK|300MAAN|345SIMM|259LUXU)-?\\d{3,5}\b",
    r"\bFC2-?PPV-?\\d{6,8}\b",
    r"\bheyzo.?\\d{4}\b",
    r"\b\\d{5,6}-\\d{3}\b",
    r"\b1pon.?\\d{6}_\\d{3}\b",
    r"\b\\d{6}_\\d{2}\b",
    r"\b[nk]\\d{4}\b",
    r"\bS1|SSIS|SONE|IPX|IPZZ|STARS|ADN|ATID|SHKD|ADN|REBD|MIDE|TEKS|OFJE\b",
    r"\bMIDV|MIDE|MIAA|MDBK|MDYD\b",
    r"\bABW|ABF|CHN|DIC|SGA|LXVS|PPX\b",
    r"\bSDAB|SDDE|SDMM|SDMT|START\b"
]

# 女优关键词（可考虑多语言识别）
female_actress_keywords = [
    "三上悠亚", "Yua Mikami", "深田えいみ", "Eimi Fukada", "桥本有菜",
    "Ariana Hashimoto", "julia", "JULIA", "天使萌", "Tenshi Moe", 
    "相泽南", "Minami Aizawa", "桃乃木香奈", "松本一香", "Ichika Matsumoto",
    "河北彩花", "Saika Kawakita", "美谷朱里", "Airi Kijima", "波多野结衣", 
    "Yui Hatano", "葵司", "Tsukasa Aoi", "明里紬", "Tsumugi Akari", 
    "樱空桃", "Momo Sakura", "小仓由菜", "Yura Ogura", "白石茉莉奈", 
    "Marina Shiraishi"
]

# 场景/类型标签
scene_keywords = [
    "素人", "人妻", "OL", "女教师", "护士", "女仆", "泳装", "比基尼", 
    "温泉", "按摩", "出张", "偷情", "寝取られ", "中出し", "ぶっかけ", 
    "ごっくん", "痴女", "逆レイプ", "レズ", "3P", "4P", "乱交", "コスプレ",
    "VR", "4K", "高画質", "無修正", "流出"
]

# 以下为辅助整理转义字符和 Regex
# 编辑核心关键词去重、优化、初始化规则
def is_in_category(title, category, **kwargs):
    # 支持模糊匹配和区域匹配
    if title.startswith('#'):  # 忽略注释行
        return False
    keywords = category_keywords.get(category, [])
    return any(keyword in title for keyword in keywords)

def extract_id_from_title(title):
    for pattern in anime_id_patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(1)
    return None

def filter_bad_words(title):
    if any(word in title for word in ["奶爸", "最(J)熱 NBVe", "如泥当"]:
        return False
    return True

def fetch_and_replace(urls):
    all_processed = []  # 存储 (标题, URL)
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
                # 清洗 (过滤掉无价值行、注释行、格式错误行)
                if '更新时间' in line or '关于' in line or '公众号' in line or '软件库' in line:
                    continue
                if not ',' in line or line.startswith('#EXTINF'):
                    continue
                title, url = line.split(',', 1)
                title = title.strip()
                url = url.strip()

                # 去除标题中的番号部分（番号正则结构会提取 ID）
                raw_id = extract_id_from_title(title)

                # 增强清理（过滤敏感词、极少数国企内容）
                if not filter_bad_words(title):
                    continue

                # 判断 URL 是否重复（重要）
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                all_processed.append((title, url))

        except requests.exceptions.Timeout:
            print(f"请求 {url} 超时，跳过。")
        except requests.exceptions.RequestException as e:
            print(f"请求 {url} 出现错误：{e}")
            continue

    # 生成 my02.txt（保留原始标题和 URL + 注意事项）
    with open('my02.txt', 'w', encoding='UTF-8') as f:
        f.write(f"注意事项,#genre#\n{current_time} 仅供测试自用如有侵权请通知,https://codeberg.org/alantang/photo/raw/branch/main/Robot.mp4\n")
        for title, url in all_processed:
            f.write(f"{title},{url}\n")

    # 分组逻辑（打法内关键词匹配 + ID提取）
    grouped_entries = {
        "🎬 影视": [],  # 包含「影视剧」关键词的标题
        "🎤 综艺": [],   # 包含「综艺」相关内容
        "📰 新闻": [],    # 包含「新闻」「资讯」等关键词的标题
        "🏅 体育": [],    # 包含「体育」「赛事」「足球」等关键词
        "🔞 成人": [],     # 包含「成人」「色情」「情色」等关键词
        "🎞 经典": [],    # 包含「经典」「经典内容」等关键词
        "📌 综合": [],     # 包含「综合」「生活」「搞笑」等关键词
        "🌸 动画": [],    # 包含「动漫」「动画」等关键词的标题
        "🎬 纪录片": [],   # 包含「纪录片」「纪实」的标题
        "🎮 游戏": [],    # 包含「游戏」「电竞」「攻略」等关键词
        "🎵 音乐": [],     # 包含「音乐」「MV」「演唱会」等关键词的标题
        "📱 短视频": []     # 包含「短视频」「快手」「抖音」等关键词
    }

    # 判断格式是否匹配并归类
    for title, url in all_processed:
        # 使用关键词匹配进行初步分类
        categories = [
            key for key, value in category_keywords.items()
            if any(keyword in title for keyword in value)
        ]
        # 精确分类，避免模糊误判
        category = "📢 默认组"
        for c in categories:
            # 若含「影视」或「动画」或「纪录片」，优先归类为主
            if c == "影视":
                category = "🎬 影视"
            elif c == "综艺":
                category = "🎤 综艺"
            elif c == "新闻":
                category = "📰 新闻"
            elif c == "体育":
                category = "🏅 体育"
            elif c == "成人":
                category = "🔞 成人"
            elif c == "经典":
                category = "🎞 经典"
            elif c == "综合":
                category = "📌 综合"
            elif c == "动画动漫":
                category = "🌸 动画"
            elif c == "纪录片":
                category = "🎬 纪录片"
            elif c == "游戏电竞":
                category = "🎮 游戏"
            elif c == "音乐":
                category = "🎵 音乐"
            elif c == "短视频生活":
                category = "📱 短视频"
            break  # 只选一个匹配

        grouped_entries[category].append((title, url))

    # 拼接 M3U 内容，并预留空间让用户看封面/logo
    m3u_header = f"""#EXTM3U
# Created by GitHub Actions: {current_time} Asia/Shanghai
# Source: IPTV
"""

    m3u_lines = [m3u_header]

    for category, entries in grouped_entries.items():
        for title, url in entries:
            # 生成 M3U 格式
            m3u_lines.append(f'#EXTINF:-1 tvg-name="{title}" group-title="{category}",{title}')
            m3u_lines.append(f'{url}\n')

    with open('my02.m3u', 'w', encoding='UTF-8') as f:
        f.write('\n'.join(m3u_lines).rstrip('\n'))

    print(f"已生成 {len(all_processed)} 条资源，归类后保存为 my02.txt 和 my02.m3u。")

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
