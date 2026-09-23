import json

INPUT_FILE = "output/articles.json"
OUTPUT_FILE = "output/aesl_articles.json"


KEYWORDS = [
    "AESL",
    "Architectural and Engineering Services Limited",
    "Architectural & Engineering Services Limited",
]


def contains_aesl(article):

    title = article.get("title") or ""
    content = article.get("content") or ""

    text = (str(title) + " " + str(content)).lower()

    for keyword in KEYWORDS:
        if keyword.lower() in text:
            return True

    return False


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        articles = json.load(file)

    filtered_articles = []

    for article in articles:
        if contains_aesl(article):
            filtered_articles.append(article)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(filtered_articles, file, indent=4, ensure_ascii=False)

    print("==============================")
    print("AESL FILTER COMPLETE")
    print("==============================")
    print(f"Total articles: {len(articles)}")
    print(f"AESL articles kept: {len(filtered_articles)}")
    print(f"Removed: {len(articles) - len(filtered_articles)}")
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
