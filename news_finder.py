import feedparser
import json
from urllib.parse import quote


SEARCH_TERMS = [
    "AESL Ghana",
    "Architectural and Engineering Services Limited",
    "AESL projects Ghana",
    "AESL consultancy Ghana",
]


def search_news(term):

    url = (
        "https://news.google.com/rss/search?q="
        + quote(term)
        + "&hl=en-GH&gl=GH&ceid=GH:en"
    )

    feed = feedparser.parse(url)

    results = []

    for item in feed.entries:

        results.append({
            "title": item.title,
            "link": item.link,
            "published": item.get(
                "published",
                ""
            ),
            "summary": item.get(
                "summary",
                ""
            )
        })

    return results


def main():

    articles = []

    for term in SEARCH_TERMS:

        print(
            f"Searching: {term}"
        )

        results = search_news(term)

        articles.extend(results)

    # remove duplicates
    unique = {}

    for article in articles:

        unique[article["link"]] = article

    final_results = list(
        unique.values()
    )

    with open(
        "news_sources.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            final_results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nFound {len(final_results)} articles"
    )


if __name__ == "__main__":
    main()
