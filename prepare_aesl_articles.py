import json
import os
from urllib.parse import urlparse


INPUT_FILE = "output/final_aesl_articles.json"
OUTPUT_FILE = "output/aesl_ready_articles.json"


def get_source(url):

    if not url:
        return "Unknown"

    domain = urlparse(url).netloc

    return (
        domain
        .replace("www.", "")
        .split(".")[0]
        .title()
    )


def get_category(text):

    text = text.lower()

    if any(word in text for word in [
        "project",
        "construction",
        "facility",
        "building",
        "infrastructure",
        "consultant"
    ]):
        return "Projects & Infrastructure"

    if any(word in text for word in [
        "board",
        "minister",
        "management",
        "appointed",
        "director"
    ]):
        return "Company News"

    if any(word in text for word in [
        "engineering",
        "architecture",
        "survey",
        "industry"
    ]):
        return "Industry News"

    return "Corporate Updates"


def generate_tags(text):

    keywords = [
        "AESL",
        "Architecture",
        "Engineering",
        "Construction",
        "Infrastructure",
        "Consultancy",
        "Ghana",
        "Projects"
    ]

    tags = []

    text = text.lower()

    for word in keywords:

        if word.lower() in text:
            tags.append(word)

    return tags


def create_excerpt(content):

    if not content:
        return ""

    content = content.replace("\n", " ")

    return content[:300]


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    prepared = []

    for article in articles:

        title = article.get("title") or ""
        content = article.get("content") or ""
        url = article.get("url") or ""

        combined = title + " " + content

        prepared.append({

            "title": title,

            "category": get_category(combined),

            "tags": generate_tags(combined),

            "excerpt": create_excerpt(content),

            "content": content,

            "source": get_source(url),

            "source_url": url,

            "image": article.get("image")

        })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            prepared,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("==============================")
    print("AESL PREPARATION COMPLETE")
    print("==============================")
    print("Articles:", len(prepared))
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
