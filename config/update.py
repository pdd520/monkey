import requests
import time
import re

def fetch_and_replace(urls, max_retries=3):
    all_entries = []  # 用于存储 (url, title) 元组列表
    seen_urls = set()  # 用于跟踪 URL 去重（基于 URL）

    for url in urls:
        for attempt in range(max_retries):  # 重试机制
            try:
                start_time = time.time()
                response = requests.get(url, timeout=15)
                end_time = time.time()

                elapsed_time = end_time - start_time
                print(f"Request to {url} (attempt {attempt + 1}) took {elapsed_time:.2f} seconds.")

                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    content = response.text

                    lines = content.splitlines()
                    i = 0
                    while i < len(lines):
                        line = lines[i].strip()

                        # 过滤无效行
                        if any(keyword in line for keyword in ['更新时间', time.strftime("%Y%m%d"), '关于', '公众号', '软件库']):
                            i += 1
                            continue

                        # 处理 #EXTINF 行
                        if line.startswith('#EXTINF'):
                            # 提取标题：逗号后的内容直到行尾
                            if ',' in line:
                                # 找到第一个逗号后的内容作为标题
                                title_part = line.split(',', 1)[1].strip()
                                # 移除可能的 #genre# 标记
                                title = re.sub(r'#genre#', '', title_part).strip()
                            else:
                                title = "未知频道"
                            
                            i += 1  # 跳到下一行获取URL
                            if i < len(lines):
                                url_line = lines[i].strip()
                                if url_line and not url_line.startswith('#'):
                                    processed_url = url_line.replace('_', '')
                                    if processed_url not in seen_urls:
                                        seen_urls.add(processed_url)
                                        all_entries.append((processed_url, title))
                        else:
                            # 非 M3U 行：视为纯 URL，从行内容提取标题
                            if line and not line.startswith('#') and '#genre#' not in line.lower():
                                title = extract_title_from_url(line)
                                processed_url = line.replace('_', '')
                                if processed_url not in seen_urls:
                                    seen_urls.add(processed_url)
                                    all_entries.append((processed_url, title))
                            
                        i += 1

                    break  # 成功后跳出重试
                else:
                    print(f"Failed to retrieve {url} with status code {response.status_code}.")

            except requests.exceptions.Timeout:
                print(f"Request to {url} timed out (attempt {attempt + 1}).")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while requesting {url}: {e}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避：1s, 2s, 4s

    # 生成时间戳（保持原代码中的时间戳功能）
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # 输出 1: my02.txt（纯 URL 列表 + notice）
    notice = f"注意事项,#genre#\n仅供测试自用如有侵权请通知,https://codeberg.org/alantang/photo/raw/branch/main/Robot.mp4\n"
    with open('my02.txt', 'w', encoding='UTF-8') as file:
        file.write(notice)
        for url, _ in all_entries:
            file.write(url + '\n')
    
    print(f"Generated my02.txt with {len(all_entries)} entries")

    # 基于 TXT 文件生成 M3U 文件
    entries_from_txt = []
    seen_urls_txt = set()
    
    with open('my02.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        
        # 跳过 notice 行
        for line in lines[2:]:  # 前两行是注意事项
            url = line.strip()
            if url and url != '注意事项' and '#genre#' not in url:
                # 如果是 .m3u8 文件，提取基础 URL
                if url.endswith('.m3u8'):
                    processed_url = re.sub(r'/[^/]+\.m3u8$', '', url)
                else:
                    processed_url = url
                
                if processed_url not in seen_urls_txt:
                    seen_urls_txt.add(processed_url)
                    entries_from_txt.append((processed_url, "未知频道"))
    
    # 输出 2: M3U 格式 my02.m3u（标准播放列表）
    m3u_header = f'#EXTM3U\n#EXT-X-VERSION:3\n#PLAYLIST-TYPE:VOD\n'
    with open('my02.m3u', 'w', encoding='UTF-8') as file:
        file.write(m3u_header)
        for url, title in entries_from_txt:
            file.write(f'#EXTINF:-1 tvg-name="{title}" group-title="默认组",{title}\n')
            file.write(f'{url}\n')
    
    # 输出 3: 未知频道的 M3U 文件
    with open('my02_unknown.m3u', 'w', encoding='UTF-8') as file:
        file.write(m3u_header)
        for url, title in entries_from_txt:
            file.write(f'#EXTINF:-1 tvg-name="{title}" group-title="未知频道",{title}\n')
            file.write(f'{url}\n')
    
    print(f"Generated my02.m3u and my02_unknown.m3u with {len(entries_from_txt)} entries each")

def extract_title_from_url(url):
    """从 URL 中提取有意义的标题"""
    # 移除协议和www
    title = re.sub(r'https?://(www\.)?', '', url)
    # 移除路径查询参数
    title = re.sub(r'(/[^\?#]*)?.*', '', title)
    # 替换特殊字符为空格
    title = re.sub(r'[^\w\u4e00-\u9fa5]', ' ', title)
    # 去除多余空格
    title = ' '.join(title.split())
    
    # 如果提取的标题过短，使用默认值
    if len(title) < 2:
        return "未知频道"
    
    return title

if __name__ == "__main__":
    # 定义多个 URL（保持原样）
    urls = [
        'https://raw.githubusercontent.com/SSM0415/apptest/main/TVonline.txt',
        'https://raw.githubusercontent.com/jack2713/my/refs/heads/main/TMP/temp1.txt',
        'https://raw.githubusercontent.com/jack2713/my/refs/heads/main/TMP/TMP.txt',
        'https://raw.githubusercontent.com/sublime2025/IPTV/refs/heads/main/adult',
        'https://raw.githubusercontent.com/SSM0415/apptest/refs/heads/main/TVbox2livefomi243.txt',
        'https://raw.githubusercontent.com/alenin-zhang/IPTV/4e8e4812168164ea11acc0617b814a7948b632f5/av',
    ]

    fetch_and_replace(urls)
