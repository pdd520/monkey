import requests
import time
import os

def fetch_and_replace(urls):
    all_processed = []  # 存储 (标题, URL)
    seen_urls = set()

    for url in urls:
        try:
            # 请求内容
            response = requests.get(url, timeout=15)
            print(f"已获取：{url}")

            if response.status_code == 200:
                content = response.text
                lines = content.splitlines()

                # 假设你的原始数据格式是：标题,URL（未包含`#EXTINF`）
                for line in lines:
                    if '更新时间' in line or '关于' in line or '公众号' in line or '软件库' in line:
                        continue  # 忽略这些行

                    # 分割成标题和 URL
                    if ',' in line:
                        title, url = line.split(',', 1)
                        all_processed.append((title.strip(), url.strip()))
                    else:
                        continue  # 忽略格式不正确的行

        except requests.exceptions.Timeout:
            print(f"请求 {url} 超时。")
        except requests.exceptions.RequestException as e:
            print(f"请求 {url} 出现错误：{e}")

    # 最终生成 my02.txt 文件（我们不需要 img 关联）
    with open('my02.txt', 'w', encoding='UTF-8') as f:
        f.write(f"注意事项,#genre#\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 仅供测试自用如有侵权请通知,https://codeberg.org/alantang/photo/raw/branch/main/Robot.mp4\n")
        for title, url in all_processed:
            f.write(f"{title},{url}\n")

    # 生成 my02.m3u 文件，支持播放器
    m3u_header = f"""#EXTM3U
#Created by GitHub Actions: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Asia/Shanghai
#Source: iptv
"""

    m3u_lines = [m3u_header]

    for title, url in all_processed:
        # 每个频道写入一个 M3U 行，不带 Logo，仅标题和链接
        m3u_lines.append(f'#EXTINF:-1 tvg-name="{title}" group-title="默认组",{title}')
        m3u_lines.append(f'{url}\n')

    # 保存为 `.m3u`（覆盖同名文件）
    with open('my02.m3u', 'w', encoding='UTF-8') as f:
        f.write('\n'.join(m3u_lines).rstrip('\n'))  # 去除最后多余的换行符

    print(f"已生成 {len(all_processed)} 条记录，保存为 my02.txt 和 my02.m3u。")

if __name__ == "__main__":
    urls = [
        'https://raw.githubusercontent.com/SSM0415/apptest/main/TVonline.txt',
        'https://raw.githubusercontent.com/jack2713/my/refs/heads/main/TMP/temp1.txt',
        'https://raw.githubusercontent.com/jack2713/my/refs/heads/main/TMP/TMP.txt',
        'https://raw.githubusercontent.com/sublime2025/IPTV/refs/heads/main/adult',
        'https://raw.githubusercontent.com/SSM0415/apptest/refs/heads/main/TVbox2livefomi243.txt',
        'https://raw.githubusercontent.com/alenin-zhang/IPTV/4e8e4812168164ea11acc0617b814a7948b632f5/av',
    ]

    fetch_and_replace(urls)
