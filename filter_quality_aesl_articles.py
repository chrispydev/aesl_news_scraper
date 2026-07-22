import json
import os


INPUT_FILE = "output/aesl_articles.json"
OUTPUT_FILE = "output/final_aesl_articles.json"


POSITIVE_KEYWORDS = [
    "project",
    "appointed",
    "consultant",
    "consultancy",
    "construction",
    "infrastructure",
    "board",
    "minister",
    "design",
    "engineering",
    "architecture",
    "survey",
    "contract",
    "development",
    "facility",
    "award",
]


NEGATIVE_KEYWORDS = [
    "strike",
    "salary arrears",
    "unpaid salaries",
    "workers protest",
    "lawsuit",
    "court",
    "accused",
    "fraud",
    "corruption",
]


def clean_text(article):

    title = article.get("title") or ""
    content = article.get("content") or ""

    return (
        title + " " + content
    ).lower()


def is_relevant(article):

    text = clean_text(article)

    # Must mention AESL
    if (
        "aesl" not in text
        and
        "architectural and engineering services limited" not in text
    ):
        return False

    # Remove negative news
    for word in NEGATIVE_KEYWORDS:
        if word in text:
            return False

    # Must have business relevance
    for word in POSITIVE_KEYWORDS:
        if word in text:
            return True

    return False


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        articles = json.load(f)

    final_articles = []

    for article in articles:

        if is_relevant(article):
            final_articles.append(article)

    os.makedirs("output", exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            final_articles,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("==============================")
    print("AESL QUALITY FILTER COMPLETE")
    print("==============================")
    print("Input:", len(articles))
    print("Kept:", len(final_articles))
    print("Removed:", len(articles) - len(final_articles))
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
