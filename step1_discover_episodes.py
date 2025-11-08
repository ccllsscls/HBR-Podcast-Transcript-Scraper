import requests
from bs4 import BeautifulSoup
import re
import json
import feedparser
from collections import defaultdict

def get_episodes_from_rss():
    """从RSS feed获取所有episodes"""
    
    print("正在从RSS feed获取episodes...")
    
    rss_url = "http://feeds.harvardbusiness.org/harvardbusiness/coaching-real-leaders"
    
    try:
        feed = feedparser.parse(rss_url)
        
        if not feed.entries:
            print("RSS feed 中没有找到任何内容")
            return [], {}
        
        print(f"找到 {len(feed.entries)} 个 episodes\n")
        
        episodes = []
        by_season = defaultdict(list)
        by_year = defaultdict(list)
        
        for entry in feed.entries:
            # 获取链接
            url = entry.link
            
            # 获取标题
            title = entry.title
            
            # 获取发布日期
            published = entry.get('published', '')
            
            # 提取年份
            year_match = re.search(r'\d{4}', published)
            year = year_match.group(0) if year_match else "Unknown"
            
            # 尝试从标题或URL提取 Season 和 Episode 信息
            season = "Unknown"
            episode = "Unknown"
            
            # 从URL提取年份（更可靠）
            url_year_match = re.search(r'/(\d{4})/', url)
            if url_year_match:
                year = url_year_match.group(1)
            
            episode_info = {
                "url": url,
                "title": title,
                "year": year,
                "published": published,
                "season": season,
                "episode": episode
            }
            
            episodes.append(episode_info)
            
            # 按年份分组
            by_year[year].append(url)
        
        # 按年份映射到季度（假设每年一个season）
        # 你可以根据实际情况调整这个映射
        season_map = {
            "2021": "S1",
            "2022": "S2", 
            "2023": "S3",
            "2024": "S4",
            "2025": "S5",
        }
        
        for year, urls in by_year.items():
            season_name = season_map.get(year, f"S{year}")
            by_season[f"{season_name}_{year}"] = urls
        
        # 保存到文件
        with open("episodes_urls.json", "w", encoding="utf-8") as f:
            json.dump({
                "all_episodes": episodes,
                "by_year": dict(by_year),
                "by_season": dict(by_season)
            }, f, indent=2, ensure_ascii=False)
        
        print("✓ 已保存到 episodes_urls.json\n")
        
        # 输出统计信息
        print("按年份统计：")
        for year in sorted(by_year.keys()):
            print(f"  {year}: {len(by_year[year])} episodes")
        
        print("\n按季度分组：")
        for season in sorted(by_season.keys()):
            print(f"  {season}: {len(by_season[season])} episodes")
        
        # 输出前5个示例
        print("\n前5个episodes：")
        for i, ep in enumerate(episodes[:5], 1):
            print(f"{i}. [{ep['year']}] {ep['title'][:60]}...")
            print(f"   {ep['url']}")
        
        return episodes, dict(by_season)
        
    except Exception as e:
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()
        return [], {}

def create_url_list_file(by_season):
    """创建一个易于编辑的URL列表文件"""
    
    with open("episodes_by_season.txt", "w", encoding="utf-8") as f:
        f.write("# Coaching Real Leaders Episodes by Season\n")
        f.write("# 编辑此文件后，可以在主程序中使用\n\n")
        
        for season in sorted(by_season.keys()):
            f.write(f"\n{'='*80}\n")
            f.write(f"{season} ({len(by_season[season])} episodes)\n")
            f.write(f"{'='*80}\n")
            for url in by_season[season]:
                f.write(f"{url}\n")
    
    print("\n✓ 已创建 episodes_by_season.txt - 你可以手动编辑这个文件")

if __name__ == "__main__":
    print("="*80)
    print("从 RSS Feed 获取 Coaching Real Leaders 所有 Episodes")
    print("="*80 + "\n")
    
    episodes, by_season = get_episodes_from_rss()
    
    if episodes:
        create_url_list_file(by_season)
        print("\n" + "="*80)
        print("完成！现在你可以运行步骤2来抓取transcripts")
        print("="*80)
    else:
        print("\n未能获取episodes，请检查网络连接或尝试手动方法")