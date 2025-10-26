# collector.py
import feedparser
import requests
from config import GNEWS_API_KEY

def collect_rss(feeds, limit=5):
    """Collect latest articles from a list of RSS feeds."""
    articles = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": getattr(entry, "summary", ""),
                "source": feed.feed.get("title", "Unknown Source")
            })
    return articles


def collect_gnews(topic, limit=5):
    """Collect articles from GNews API for a given topic."""
    url = f"https://gnews.io/api/v4/search?q={topic}&lang=vi&max={limit}&token={GNEWS_API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        print(f"[GNews] Failed to fetch articles: {r.status_code}")
        return []

    data = r.json()
    if "articles" not in data:
        print("[GNews] Unexpected response format")
        return []

    articles = []
    for a in data["articles"]:
        articles.append({
            "title": a.get("title", ""),
            "link": a.get("url", ""),
            "summary": a.get("description", ""),
            "source": a.get("source", {}).get("name", "GNews")
        })
    return articles


def collect_all(topic, limit=5):
    """Collect articles from both RSS feeds and GNews API."""
    rss_feeds = [
        "https://vnexpress.net/rss/tin-moi-nhat.rss",
        "https://tuoitre.vn/rss/tin-moi-nhat.rss",
        "https://vietnamnews.vn/rss/general.rss",
        "https://thanhnien.vn/rss/home.rss",
        "https://nhandan.vn/rss/home.rss"
    ]

    rss_articles = collect_rss(rss_feeds, limit)
    gnews_articles = collect_gnews(topic, limit)
    articles = rss_articles + gnews_articles

    print(f"[Collector] Collected {len(articles)} articles total")
    return articles
