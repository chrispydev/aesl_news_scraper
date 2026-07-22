import json
import math
import os

# ==========================
# CONFIG
# ==========================
INPUT_FILE = "output/final_aesl_articles.json"
OUTPUT_FOLDER = "output/split_articles"
ARTICLES_PER_FILE = 5

# ==========================
# CREATE OUTPUT FOLDER
# ==========================
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================
# LOAD JSON
# ==========================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

total_articles = len(articles)
total_files = math.ceil(total_articles / ARTICLES_PER_FILE)

print(f"Total Articles : {total_articles}")
print(f"Files to Create: {total_files}")
print()

# ==========================
# SPLIT FILES
# ==========================
for i in range(total_files):
    start = i * ARTICLES_PER_FILE
    end = start + ARTICLES_PER_FILE

    chunk = articles[start:end]

    filename = os.path.join(
        OUTPUT_FOLDER,
        f"articles_{i + 1:03}.json"
    )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chunk, f, indent=4, ensure_ascii=False)

    print(f"✓ Saved {filename} ({len(chunk)} articles)")

print("\nDone!")
