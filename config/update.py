import requests
import time
import re  # 用于解析 #EXTINF 中的标题

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

                        # 过滤无效行（保持原逻辑，但不过滤 #EXTINF）
                        if any(keyword in line for keyword in ['更新时间', time.strftime("%Y%m%d"), '关于', '公众号', '软件库']):
                            i += 1
                            continue

                        # 处理 #EXTINF 行：提取标题
                        if line.startswith('#EXTINF'):
                            # 用正则提取标题：匹配 , 后的内容，直到结束
                            title_match = re.search(r',(.+)$', line)
                            title = title_match.group(1).strip() if title_match else "未知频道"
                            i += 1  # 跳到下一行（URL）
                            if i < len(lines):
                                url_line = lines[i].strip()
                                if url_line and not url_line.startswith('#'):  # 假设是 URL
                                    processed_url = url_line.replace('_', '')  # 去下划线
                                    if processed_url not in seen_urls:
                                        seen_urls.add(processed_url)
                                        all_entries.append((processed_url, title))
                        else:
                            # 非 M3U 行：视为纯 URL，标题用默认
                            if line and not line.startswith('#') and '#genre#' not in line.lower():
                                processed_url = line.replace('_', '')
                                if processed_url not in seen_urls:
                                    seen_urls.add(processed_url)
                                    all_entries.append((processed_url, "未知频道"))

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

    # 输出 1: 原格式 my02.txt（纯 URL 列表 + notice）
    notice = f"注意事项,#genre#\n仅供测试自用如有侵权请通知,https://codeberg.org/alantang/photo/raw/branch/main/Robot.mp4\n"
    with open('my02.txt', 'w', encoding='UTF-8') as file:
        file.write(notice)
        for url, _ in all_entries:
            file.write(url + '\n')

    # 输出 2: M3U 格式 my02.m3u（标准播放列表）
    m3u_header = f'#EXTM3U\n#EXT-X-VERSION:3\n#PLAYLIST-TYPE:VOD\n'  # M3U8 兼容头
    with open('my02.m3u', 'w', encoding='UTF-8') as file:
        file.write(m3u_header)
        for url, title in all_entries:
            file.write(f'#EXTINF:-1 tvg-name="{title}" group-title="默认组",{title}\n')
            file.write(f'{url}\n')

    print(f"Generated {len(all_entries)} unique entries. Files: my02.txt and my02.m3u")

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
