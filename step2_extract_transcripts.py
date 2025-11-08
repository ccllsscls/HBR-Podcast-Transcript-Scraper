import requests
from bs4 import BeautifulSoup
import re
import json
import time
from pathlib import Path

def extract_episode_info(soup, url):
    """提取单个 episode 的信息"""
    
    # 提取季数和集数
    season_num = "Unknown"
    episode_num = "Unknown"
    
    # 在页面中查找 "Season X, Episode Y" 格式
    for tag in soup.find_all(string=re.compile(r"Season\s+\d+")):
        match = re.search(r'Season\s+(\d+).*?Episode\s+(\d+)', tag, re.IGNORECASE)
        if match:
            season_num = match.group(1)
            episode_num = match.group(2)
            break
    
    # 如果没找到，尝试只查找 Episode
    if episode_num == "Unknown":
        for tag in soup.find_all(string=re.compile(r"Episode\s+\d+")):
            match = re.search(r'Episode\s+(\d+)', tag)
            if match:
                episode_num = match.group(1)
                break
    
    # 提取年份
    date_tag = soup.find("span", class_="podcast-details__date")
    year = date_tag.text.split()[-1] if date_tag else "Unknown"
    
    # 提取标题
    title_tag = soup.title
    if title_tag:
        # 尝试多种模式
        patterns = [
            r'- (.*?) - Women at Work',
            r'- (.*?) - Coaching Real Leaders',
            r': (.*?) \|',
        ]
        episode_title = None
        for pattern in patterns:
            match = re.search(pattern, title_tag.text)
            if match:
                episode_title = match.group(1).strip()
                break
        if not episode_title:
            episode_title = title_tag.text.strip()
    else:
        episode_title = "Unknown Title"
    
    # 提取 Transcript
    transcript_section = soup.find("section", id="transcript-section")
    if not transcript_section:
        # 尝试其他可能的选择器
        transcript_section = soup.find("div", class_="transcript")
    
    transcript_text = ""
    if transcript_section:
        transcript_text = transcript_section.get_text(separator="\n", strip=True)
    
    return {
        "season": season_num,
        "episode": episode_num,
        "year": year,
        "title": episode_title,
        "transcript": transcript_text
    }

def fetch_episode(url, retry=3):
    """获取单个episode，带重试机制"""
    for attempt in range(retry):
        try:
            response = requests.get(url, verify=False, timeout=30)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            else:
                print(f"    状态码：{response.status_code}")
        except Exception as e:
            print(f"    尝试 {attempt+1}/{retry} 失败：{e}")
            if attempt < retry - 1:
                time.sleep(2)
    return None

def process_season(season_name, episode_urls, output_dir="output"):
    """处理一个季度的所有episodes"""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"开始处理：{season_name}")
    print(f"{'='*80}")
    
    episodes_data = []
    
    for i, url in enumerate(episode_urls, 1):
        print(f"\n[{i}/{len(episode_urls)}] 处理中...")
        print(f"  URL: {url}")
        
        soup = fetch_episode(url)
        if not soup:
            print(f"  ✗ 获取失败")
            continue
        
        info = extract_episode_info(soup, url)
        
        if info["transcript"]:
            episodes_data.append(info)
            print(f"  ✓ Episode {info['episode']}: {info['title'][:50]}...")
            print(f"    Transcript 长度: {len(info['transcript'])} 字符")
        else:
            print(f"  ✗ 未找到 transcript")
        
        # 避免请求过快
        time.sleep(1)
    
    # 保存合并文件
    if episodes_data:
        # 按 episode 编号排序
        try:
            episodes_data.sort(key=lambda x: int(x["episode"]) if x["episode"].isdigit() else 999)
        except:
            pass
        
        output_filename = f"{output_dir}/{season_name}.txt"
        
        with open(output_filename, "w", encoding="utf-8") as f:
            for ep in episodes_data:
                # 写入分隔符和标题
                f.write(f"\n{'='*80}\n")
                f.write(f"Episode {ep['episode']}: {ep['title']}\n")
                f.write(f"Year: {ep['year']}\n")
                f.write(f"{'='*80}\n\n")
                f.write(ep['transcript'])
                f.write("\n\n")
        
        print(f"\n✓✓✓ 已保存：{output_filename}")
        print(f"    共 {len(episodes_data)} 个 episodes")
        return True
    else:
        print(f"\n✗✗✗ {season_name} 没有有效内容")
        return False

def main():
    """主函数"""
    
    # 方式1：从JSON文件读取（如果你运行了步骤1）
    try:
        with open("episodes_urls.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            by_year = data.get("by_year", {})
        
        if by_year:
            print("从 episodes_urls.json 读取链接...")
            # 按年份处理
            for year in sorted(by_year.keys()):
                if by_year[year]:
                    # 假设每年对应一个season（你可能需要调整）
                    season_name = f"S{int(year)-2020}_{year}"  # 2021=S1, 2022=S2...
                    process_season(season_name, by_year[year])
            return
    except FileNotFoundError:
        print("未找到 episodes_urls.json")
    
    # 方式2：手动指定URLs（如果没有JSON文件）
    print("\n使用手动指定的URLs...")
    
    episodes_by_season = {
        "S10_2024": [
            "https://hbr.org/podcast/2025/11/how-do-i-handle-so-much-organizational-uncertainty",
            "https://hbr.org/podcast/2025/10/how-do-i-lead-when-i-dont-feel-like-i-belong-at-the-table",
            # 在这里添加更多URLs
        ],
        # 添加更多季度...
    }
    
    for season_name, urls in episodes_by_season.items():
        if urls:
            process_season(season_name, urls)
    
    print("\n" + "="*80)
    print("所有处理完成！")
    print("="*80)

if __name__ == "__main__":
    main()