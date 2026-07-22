import json
import os

# ==========================
# CONFIG
# ==========================
INPUT_FILE = "output/final_aesl_articles.json"
OUTPUT_FOLDER = "output/manual_articles"

# ==========================
# CREATE FOLDER
# ==========================
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================
# LOAD ARTICLES
# ==========================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)


# ==========================
# CREATE ONE FILE PER ARTICLE
# ==========================
for index, article in enumerate(articles, start=1):

    filename = os.path.join(
        OUTPUT_FOLDER,
        f"article_{index:03}.json"
    )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            article,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Created: {filename}")


print("\nAll articles exported successfully.")
