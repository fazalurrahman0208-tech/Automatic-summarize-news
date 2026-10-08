import datetime
import json
import urllib.error
import urllib.parse
import urllib.request

API_KEY = "d3faacc7d17546cf8ddce6b3d7264343"
BASE_URL = "https://newsapi.org/v2/top-headlines"
OUTPUT_FILE = "headlines_summary.txt"


def sanitize_input(category: str) -> str:
    return category.strip().lower()


def fetch_news(category: str, country: str = "in") -> dict:
    query_params = urllib.parse.urlencode(
        {"country": country, "category": category, "apiKey": API_KEY}
    )
    full_url = f"{BASE_URL}?{query_params}"
    request = urllib.request.Request(
        full_url, headers={"User-Agent": "NewsAggregatorApp/1.0"}
    )

    try:
        with urllib.request.urlopen(request) as response:
            print(f"Status: {response.getcode()} OK. Fetching data...")
            raw_data = response.read().decode("utf-8")
            return json.loads(raw_data)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("Error 401: Unauthorized API Key.")
        else:
            print(f"HTTP Error {e.code}: {e.reason}")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}


def process_and_save_articles(articles: list, category: str):
    if not articles:
        print("No articles found to save.")
        return False

    current_date = datetime.date.today().strftime("%Y-%m-%d")
    header_title = f"LATEST {category.upper()} NEWS - {current_date}"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(f"{header_title}\n")
        file.write("-" * len(header_title) + "\n\n")

        for idx, article in enumerate(articles[:5], start=1):
            title = article.get("title") or "NO TITLE AVAILABLE"
            source_name = (article.get("source") or {}).get(
                "name", "Unknown Source"
            )
            summary = article.get("description") or "No description provided."

            file.write(f"{idx}. {title.upper()}\n")
            file.write(f"Source: {source_name}\n")
            file.write(f"Summary: {summary}\n")
            file.write("-" * 45 + "\n\n")
    return True


def main():
    print("--- Live News Aggregator ---")
    user_input = input("Enter Category (sports/technology/business): ")
    category = sanitize_input(user_input)

    data = fetch_news(category=category, country="in")

    if not data or not data.get("articles"):
        print(f"No news articles found for '{category}'.")
        return

    articles = data["articles"]
    if process_and_save_articles(articles, category):
        print(
            f"Success! Top {min(len(articles), 5)} {category} headlines saved to {OUTPUT_FILE}."
        )


if __name__ == "__main__":
    main()
