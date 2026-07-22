import os
import json
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

import trafilatura
from PIL import Image
from io import BytesIO

from googlenewsdecoder import new_decoderv1


# ==========================
# SETTINGS
# ==========================

SOURCE_FILE = "news_sources.json"

OUTPUT_DIR = "output"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "articles.json"
)


HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


os.makedirs(
    IMAGE_DIR,
    exist_ok=True
)


# ==========================
# LOAD SOURCES
# ==========================

def load_sources():

    with open(
        SOURCE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================
# GOOGLE NEWS URL DECODER
# ==========================

def decode_google_url(url):

    try:

        result = new_decoderv1(
            url
        )

        if result.get("status"):

            return result["decoded_url"]

    except Exception as e:

        print(
            "Decoder error:",
            e
        )

    return None


# ==========================
# DOWNLOAD IMAGE
# ==========================

def download_image(
        image_url,
        filename
):

    try:

        response = requests.get(
            image_url,
            headers=HEADERS,
            timeout=20
        )

        img = Image.open(
            BytesIO(response.content)
        )

        path = os.path.join(
            IMAGE_DIR,
            filename
        )

        img.save(
            path
        )

        return path

    except Exception:

        return None


# ==========================
# EXTRACT ARTICLE IMAGE
# ==========================

def find_image(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # OpenGraph image
        image = soup.find(
            "meta",
            property="og:image"
        )

        if image:

            return image.get(
                "content"
            )

        # fallback
        img = soup.find(
            "img"
        )

        if img:

            return img.get(
                "src"
            )

    except Exception:

        pass

    return None


# ==========================
# EXTRACT ARTICLE CONTENT
# ==========================

def scrape_article(url):

    print(
        "\nScraping:",
        url
    )

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        html = response.text

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        title = None

        if soup.title:

            title = soup.title.text.strip()

        content = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        image = find_image(
            url
        )

        return {

            "title": title,

            "url": url,

            "content": content,

            "image_url": image,

        }

    except Exception as e:

        print(
            "Failed:",
            e
        )

        return None


# ==========================
# MAIN
# ==========================


def main():

    sources = load_sources()

    articles = []

    for index, item in enumerate(
        sources,
        start=1
    ):

        google_url = item["link"]

        print(
            f"\n[{index}/{len(sources)}]"
        )

        real_url = decode_google_url(
            google_url
        )

        if not real_url:

            print(
                "Could not decode"
            )

            continue

        article = scrape_article(
            real_url
        )

        if not article:

            continue

        # Download image

        if article["image_url"]:

            ext = ".jpg"

            filename = (
                f"article_{index}"
                + ext
            )

            saved = download_image(
                article["image_url"],
                filename
            )

            article["image"] = saved

        articles.append(
            article
        )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            articles,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        "\nCompleted"
    )

    print(
        f"Saved {len(articles)} articles"
    )


if __name__ == "__main__":

    main()
