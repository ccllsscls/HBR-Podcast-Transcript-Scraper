# HBR-Podcast-Transcript-Scraper
A Python web scraping toolkit for collecting and organizing publicly available podcast transcripts from Harvard Business Review's "Coaching Real Leaders" series for personal learning and leadership development study.

🎯 **Project Purpose**  
This project demonstrates:  
**Technical Skills**: Web scraping, data extraction, and content organization using Python  
**Personal Development**: Deep interest in leadership development and executive coaching  
**Learning Application**: Creating a searchable corpus for studying leadership scenarios and coaching techniques

🛠️ **Technical Features**  
Core Capabilities  
**RSS Feed Integration**: Automated episode discovery from HBR's podcast feed  
**Intelligent Web Scraping**: Robust HTML parsing with BeautifulSoup4  
**Error Handling**: Retry mechanisms and graceful failure handling  
**Data Organization**: Automatic grouping by season/year with structured output  
**Rate Limiting**: Respectful scraping with request throttling  

**Key Technologies**
- requests - HTTP requests and session management
- BeautifulSoup4 - HTML/XML parsing
- feedparser - RSS feed processing
- re - Pattern matching for data extraction
- pathlib - Modern file system operations

🚀 **Usage**  
**Step 1: Discover Episodes**  
python step1_discover_episodes.py  
This script:  
- Fetches the complete episode list from HBR's RSS feed
- Organizes episodes by year and season
- Generates episodes_urls.json with structured metadata
- Creates episodes_by_season.txt for manual review

**Step 2: Extract Transcripts**  
python step2_extract_transcripts.py  
This script:  
- Reads episode URLs from the JSON file
- Extracts publicly available transcripts from each episode page
- Organizes content by season with episode metadata
- Saves consolidated text files per season

📊** What I've Learned**  
**Technical Insights**  
- Web Scraping Best Practices: Implementing retry logic, respecting rate limits, and handling various HTML structures
- Data Pipeline Design: Two-stage process separating discovery from extraction for better modularity
- Error Resilience: Graceful degradation when elements are missing or pages fail to load

**Leadership Development Journey**  
Through analyzing these transcripts, I'm studying:
- Real-world coaching scenarios and interventions
- Leadership challenges across different organizational contexts
- Communication strategies for difficult conversations
- Decision-making frameworks under uncertainty
- Emotional intelligence in leadership

🎓 **Use Cases**  
This corpus enables:
- Thematic Analysis: Identifying recurring leadership patterns
- Case Study Review: Deep-diving into specific coaching scenarios
- Searchable Reference: Quick lookup of relevant episodes by topic
- Personal Reflection: Comparing challenges with my own leadership experiences

⚖️ **Legal & Ethical Notes**
Content Source: All transcripts are publicly available on HBR.org
Personal Use: This tool is for personal learning and educational purposes only
No Redistribution: Scraped content is not redistributed or published
Respect: Implements rate limiting to avoid server strain

🤝 **Contributing**  
While this is a personal learning project, suggestions for improving the scraping logic or data organization are welcome!

📬 Contact  
Interested in discussing leadership development or Python web scraping? Feel free to reach out!

Note: This project is intended for personal educational use. Please review HBR's terms of service and respect copyright when using any web scraping tool.
