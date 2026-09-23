import json
import re

INPUT_FILE = "/home/seer/aesl_news_scraper/output/all_news.json"
OUTPUT_FILE = "/home/seer/aesl_news_scraper/output/news_updated.json"


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)


for article in articles:
    content = article.get("content", "")
    source_url = article.get("source_url")

    if not source_url:
        continue

    # Remove existing Source paragraph
    content = re.sub(
        r"<p><strong>Source:</strong>.*?</p>", "", content, flags=re.DOTALL
    )

    # Add new source link
    content += f"""
    <p>
        <strong>Source:</strong>
        <a href="{source_url}" target="_blank">
            {source_url}
        </a>
    </p>
    """

    article["content"] = content


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=4, ensure_ascii=False)


print("Source URLs updated successfully")
