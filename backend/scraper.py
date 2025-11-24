import json
import time
import warnings
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

warnings.filterwarnings("ignore")

# ------------------------------------------------------
# PATHS (auto-resolve)
# ------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "dataset" / "Gen_AI_Dataset.xlsx"
INDEX_DIR = Path(__file__).resolve().parents[1] / "../indexes"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSONL = INDEX_DIR / "metadata.jsonl"

BASE_URL = "https://www.shl.com"

# ------------------------------------------------------
# LOAD DATASET (Excel)
# ------------------------------------------------------
def load_dataset():
    try:
        df = pd.read_excel(DATASET_PATH)
        print(f"📘 Loaded dataset rows: {len(df)}")
        return df
    except Exception as e:
        print(f"⚠ Dataset load failed: {e}")
        return None

# ------------------------------------------------------
# ALL PAGINATION URLS (TYPE=1 ONLY)
# ------------------------------------------------------
def get_catalog_urls():
    urls = [
        f"https://www.shl.com/solutions/products/product-catalog/?start={i}&type=1"
        for i in range(0, 373, 12)
    ]
    urls.insert(0, "https://www.shl.com/solutions/products/product-catalog/")
    return urls

# ------------------------------------------------------
# CLEAN REQUEST GETTER
# ------------------------------------------------------
def get_soup(url):
    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

# ------------------------------------------------------
# SCRAPE FULL DESCRIPTION FROM PRODUCT PAGE
# ------------------------------------------------------
def scrape_details(page_url):
    try:
        soup = get_soup(page_url)

        # Default structure
        details = {
            "description": "No description found",
            "duration": None,
            "languages": [],
            "job_level": None,
            "remote_testing": None,
            "test_type": None,
        }

        # Extract meaningful description
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            txt = p.get_text(" ", strip=True)
            if len(txt) > 60 and "assessment" in txt.lower():
                details["description"] = txt
                break

        # Duration (loose search)
        for tag in soup.find_all(["p", "li", "span"]):
            text = tag.get_text(" ", strip=True).lower()
            if "minute" in text or "hour" in text:
                details["duration"] = tag.get_text(" ", strip=True)
                break

        return details

    except Exception as e:
        return {"description": f"ERROR: {e}"}

# ------------------------------------------------------
# SCRAPE MAIN CATALOG TABLES
# ------------------------------------------------------
def scrape_catalog():
    catalog_urls = get_catalog_urls()
    all_items = []
    visited_urls = set()

    print(f"📌 Total tabs to scrape: {len(catalog_urls)}")

    for tab_index, url in enumerate(catalog_urls, 1):

        try:
            print(f"\n🔄 Scraping Tab {tab_index}/{len(catalog_urls)} → {url}")
            soup = get_soup(url)

            rows = soup.select("table tr")[1:]
            print(f"   → Found {len(rows)} items in table")

            for i, row in enumerate(rows, 1):
                cols = row.select("td")
                if not cols:
                    continue

                link = cols[0].find("a")
                if not link:
                    continue

                product_url = urljoin(BASE_URL, link["href"])

                # Avoid duplicates
                if product_url in visited_urls:
                    continue
                visited_urls.add(product_url)

                print(f"   📄 ({i}/{len(rows)}) Fetching details: {product_url}")

                details = scrape_details(product_url)

                item = {
                    "name": link.get_text(strip=True),
                    "url": product_url,
                    "description": details["description"],
                    "duration": details["duration"],
                    "languages": details["languages"],
                    "job_level": details["job_level"],
                    "remote_testing": details["remote_testing"],
                    "test_type": details["test_type"],
                    "source_tab": tab_index
                }

                all_items.append(item)

                time.sleep(1.2)

        except Exception as e:
            print(f"❌ Failed Tab {tab_index}: {e}")
            continue

    print(f"\n🚀 TOTAL SCRAPED ITEMS: {len(all_items)}")
    return all_items

# ------------------------------------------------------
# WRITE TO metadata.jsonl
# ------------------------------------------------------
def write_jsonl(records):
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"📄 Saved {len(records)} items → {OUTPUT_JSONL}")

# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
def main():
    load_dataset()  # Not used yet, but RAG will use it later
    records = scrape_catalog()
    write_jsonl(records)

if __name__ == "__main__":
    main()
